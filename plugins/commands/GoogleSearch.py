from plugins.BasePlugin import BasePlugin
# noinspection PyPackageRequirements
from googleapiclient.discovery import build


class GoogleSearch(BasePlugin):
    def __init__(self, plugin_manager: object):
        self.plugin_manager = plugin_manager
        self.config_manager = self.plugin_manager.agent.config_manager
        self.command = "google"
        self.description = "Google Search"
        self.arguments = {"input": "<search>"}
        self.service = build("customsearch", "v1", developerKey=self.config_manager.google_cse_developer_key)
        self.returns = str
        self.feed_back = True
        self.priority = 0

    def register(self) -> tuple:
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]) -> str:
        self.plugin_manager.logger.info(f'Command {self.command} called with arguments {arguments}')
        res = (self.service.cse().list(q=arguments["input"], num=5, cx=self.config_manager.google_cse_cx).execute())
        if res:
            if "items" in res:
                search_results = f'The result of the Google search for "{arguments["input"]}" are as follows:\n\n'

                for item in res["items"]:
                    search_results += f'{item["title"]} ({item["link"]}): {item["snippet"]}\n'

                if self.config_manager.verbose:
                    self.plugin_manager.logger.info(f'{len(res["items"])} Google search results'
                                                    f' will be fed back on the next query')

                return search_results

        if self.config_manager.verbose:
            self.plugin_manager.logger.info("Google search returned no results.")

        return f'There were no results from the Google search for {arguments["input"]}.'
