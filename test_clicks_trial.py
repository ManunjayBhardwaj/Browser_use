import asyncio
import json
import os
import pytest

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.dom.views import DOMBaseNode, DOMElementNode, DOMTextNode
from browser_use.utils import time_execution_sync


class ElementTreeSerializer:
    @staticmethod
    def dom_element_node_to_json(element_tree: DOMElementNode) -> dict:
        def node_to_dict(node: DOMBaseNode) -> dict:
            if isinstance(node, DOMTextNode):
                return {'type': 'text', 'text': node.text}
            elif isinstance(node, DOMElementNode):
                return {
                    'type': 'element',
                    'tag_name': node.tag_name,
                    'attributes': node.attributes,
                    'highlight_index': node.highlight_index,
                    'children': [node_to_dict(child) for child in node.children],
                }
            return {}

        return node_to_dict(element_tree)


@pytest.mark.asyncio
async def test_highlight_elements():
    browser = Browser(config=BrowserConfig(headless=False, disable_security=True))

    async with await browser.new_context() as context:
        page = await context.get_current_page()
        await page.goto('https://www.trivago.com')
        await asyncio.sleep(1)

        while True:
            try:
                state = await context.get_state(True)

                # Ensure ./tmp exists
                os.makedirs('./tmp', exist_ok=True)

                # Save DOM tree to JSON
                with open('./tmp/page.json', 'w') as f:
                    json.dump(
                        ElementTreeSerializer.dom_element_node_to_json(state.element_tree),
                        f,
                        indent=1
                    )
                print("✅ Saved DOM structure to ./tmp/page.json")

                # Build XPath stats
                xpath_counts = {}
                if not state.selector_map:
                    print("⚠️ No clickable elements found.")
                    continue

                for selector in state.selector_map.values():
                    xpath = selector.xpath
                    xpath_counts[xpath] = xpath_counts.get(xpath, 0) + 1

                print('\n🔁 Duplicate XPaths found:')
                for xpath, count in xpath_counts.items():
                    if count > 1:
                        print(f'XPath: {xpath} | Count: {count}')

                print('\n🔢 Selector map keys:')
                print(list(state.selector_map.keys()))

                print('\n🔘 Clickable elements:')
                print(state.element_tree.clickable_elements_to_string())

                # Wait for user to choose action
                action = input('🎯 Select next element index to click (Ctrl+C to quit): ')
                await time_execution_sync('remove_highlight_elements')(context.remove_highlights)()

                node_element = state.selector_map[int(action)]
                await context._click_element_node(node_element)
                await asyncio.sleep(1)

            except Exception as e:
                print(f"❌ Error: {e}")
