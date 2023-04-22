from plugins.BasePlugin import BasePlugin
import requests
from bs4 import BeautifulSoup


class WikipediaSearch(BasePlugin):
    def __init__(self, plugin_manager: object):
        self.command = "wikipedia"
        self.description = "Search Wikipedia"
        self.arguments = {"input": "<search>"}
        self.returns = str
        self.feed_back = True
        self.priority = 0
        self.plugin_manager = plugin_manager

    def register(self) -> tuple:
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]) -> str:
        session = requests.Session()
        # Custom User-Agent header as required by Wikimedia (https://meta.wikimedia.org/wiki/User-Agent_policy)
        headers = {"User-Agent": "Automatron Bot for ChatGPT (https://https://github.com/mindphluxnet/Automatron)"}
        try:
            data = session.get(url="https://en.wikipedia.org/w/api.php", params={"action": "query", "format": "json",
                                                                                 "list": "search",
                                                                                 "srsearch": arguments["input"]},
                               headers=headers).json()
        except requests.exceptions.JSONDecodeError:
            self.plugin_manager.logger.error("Wikipedia search returned invalid JSON")
            return "Wikipedia search failed: invalid JSON response. Please try again."

        if data:
            results = "Wikipedia search results:\n\n"
            for result in data["query"]["search"]:
                title = result["title"]
                snippet = result["snippet"]
                # We only want the plain text without HTML tags.
                soup = BeautifulSoup(snippet, "html.parser")
                snippet = soup.get_text()
                page = f'https://en.wikipedia.com/wiki/{title.replace(" ", "_")}'
                results += f"{page} - {title} - {snippet}\n"

            return results
        else:
            return "Wikipedia search returned no results."
