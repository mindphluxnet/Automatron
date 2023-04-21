from plugins.BasePlugin import BasePlugin
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os


class GoogleSearch(BasePlugin):
    def __init__(self, plugin_manager: object):
        load_dotenv()
        self.command = "google"
        self.description = "Google Search"
        self.arguments = {"input": "<search>"}
        self.service = build("customsearch", "v1", developerKey=os.environ["GOOGLE_CSE_DEVELOPER_KEY"])
        self.returns = str
        self.feed_back = True
        self.priority = 0
        self.plugin_manager = plugin_manager

    def register(self):
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]):
        self.plugin_manager.logger.info(f'Command {self.command} called, input: {arguments["input"]}')
        res = (self.service.cse().list(q=arguments["input"], num=5, cx=os.environ["GOOGLE_CSE_CX"]).execute())
        if res:
            if "items" in res:
                search_results = f'The result of the Google search for {arguments["input"]} are as follows:\n\n'

                for item in res["items"]:
                    search_results += f'{item["title"]} ({item["link"]}): {item["snippet"]}'

                return search_results

        return f'There were no results from the Google search for {arguments["input"]}.'
