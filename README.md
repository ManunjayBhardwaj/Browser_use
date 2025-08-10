
# Multi-Agent Browser Automation Projects

This repository contains three Python projects that combine browser automation with large language models to perform interactive browsing, autonomous shopping, and news extraction tasks.

---

## 1. Interactive Browser Element Clicker (`test_clicks_trial.py`)

### Features

- Loads a webpage in a browser (headless or visible)
- Extracts the DOM tree and saves it as JSON (`./tmp/page.json`)
- Lists clickable elements with their XPath
- Lets you select elements to click by typing their index
- Highlights clicked elements and updates the DOM continuously
- Handles invalid inputs and errors gracefully

### Requirements

- Python 3.8+
- `browser_use` library
- `pytest-asyncio` (if running tests)
- Any other dependencies as per your environment

### How to Run

1. Install dependencies:

   ```bash
   pip install browser_use pytest-asyncio
   ```

2. Run the interactive script with output capture disabled to allow input prompts:

   ```bash
   pytest -s test_clicks_trial.py
   ```

---

## 2. Autonomous Shopping Agent (`autonomous_shopping_agent.py`)

### Features

- Accepts natural language shopping queries
- Uses GPT-4.1 model via LangChain and `browser_use` for real browser automation
- Navigates ecommerce websites, searches, applies filters, selects items
- Handles login (with email/password), popups, out-of-stock items, and other errors
- Adds products to cart and provides a detailed shopping summary
- Does **not** proceed to payment for safety reasons

### Requirements

- Python 3.8+
- `langchain_openai`
- `browser_use`
- `python-dotenv`

### Setup

1. Create a `.env` file in your project root with your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. Install dependencies:

   ```bash
   pip install langchain_openai browser_use python-dotenv
   ```

### How to Run

```bash
python autonomous_shopping_agent.py
```

When prompted, enter your shopping query (e.g., “Buy a black cotton shirt from Myntra, size M, under ₹4000”).

---

## 3. News Extraction Agent (`news_extraction_agent.py`)

### Features

- Extracts structured recent news or articles from websites like Hacker News
- Uses GPT-4.1 model with LangChain and Pydantic for output validation
- Returns post titles, URLs, number of comments, and hours since posted
- Accepts user queries or defaults to "Show HN" posts if input is empty
- Outputs results formatted clearly in the terminal

### Requirements

- Python 3.8+
- `langchain_openai`
- `pydantic`
- `python-dotenv`

### Setup

1. Create a `.env` file with your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. Install dependencies:

   ```bash
   pip install langchain_openai pydantic python-dotenv
   ```

### How to Run

```bash
python news_extraction_agent.py
```

Enter your query or press Enter for default recent news.

---

## Common Notes

- All scripts require Python 3.8+ and an OpenAI API key.
- Use `.env` files to keep your API keys secure.
- Interactive scripts may require running with `-s` flag for pytest or from the terminal.
- Avoid hardcoding sensitive credentials in code.
- Adjust browser visibility (`headless` mode) in scripts for debugging.

---

## License

MIT License

---

Feel free to contribute, customize, or extend these projects for your automation and AI needs!
