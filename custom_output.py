"""
Agent to extract structured news/article posts from sites like Hacker News.

@dev Ensure OPENAI_API_KEY is set in environment variables.
"""

import os
import sys
import asyncio

from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

# Local imports
from browser_use import Agent, Controller

# Load env vars
load_dotenv()

# ---- Define Output Schema ----

class Post(BaseModel):
	post_title: str
	post_url: str
	num_comments: int
	hours_since_post: int


class Posts(BaseModel):
	posts: list[Post]

# ---- Setup Controller with Schema ----

controller = Controller(output_model=Posts)


# ---- Main Runner ----

async def run_news_agent(query: str):
	task = f"{query}. Focus only on recent news or articles. Return titles, URLs, comments, and hours since posted."

	agent = Agent(
		task=task,
		llm=ChatOpenAI(model='gpt-4.1'),
		controller=controller
	)

	history = await agent.run()

	result = history.final_result()
	if result:
		parsed = Posts.model_validate_json(result)

		for post in parsed.posts:
			print('\n📰 -------------------------------')
			print(f'🧠 Title:            {post.post_title}')
			print(f'🌐 URL:              {post.post_url}')
			print(f'💬 Comments:         {post.num_comments}')
			print(f'⏰ Hours since post: {post.hours_since_post}')
	else:
		print('⚠️ No structured result returned')


if __name__ == '__main__':
	# Accept user query or use default
	user_query = input("🗞️ What kind of news/articles do you want? (Press Enter for 'Show HN')\n👉 ").strip()

	asyncio.run(run_news_agent(user_query))
