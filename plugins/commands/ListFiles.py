from plugins.BasePlugin import BasePlugin
from dotenv import load_dotenv
import os


class ListFiles(BasePlugin):
    def __init__(self, plugin_manager: object):
        load_dotenv()
        self.command = "list_files"
        self.description = "List the files in your workspace"
        self.arguments = {}
        self.returns = str
        self.feed_back = True
        self.priority = 0
        self.plugin_manager = plugin_manager

    def register(self):
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]):
        self.plugin_manager.logger.info(f'Command {self.command} called with arguments: {arguments}')
        files = os.listdir(os.environ["AGENT_WORKSPACE"])

        output = "These are the files in your workspace:\n\n"
        for file in files:
            output += f"{file}\n"

        return output
