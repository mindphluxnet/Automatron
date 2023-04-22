from plugins.BasePlugin import BasePlugin
import os


class ListFiles(BasePlugin):
    def __init__(self, plugin_manager: object):
        self.plugin_manager = plugin_manager
        self.config_manager = self.plugin_manager.agent.config_manager
        self.command = "list_files"
        self.description = "List the files in your workspace"
        self.arguments = {}
        self.returns = str
        self.feed_back = True
        self.priority = 0
        self.plugin_manager = plugin_manager

    def register(self) -> tuple:
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]) -> str:
        if self.config_manager.verbose:
            self.plugin_manager.logger.info(f'Command {self.command} called with arguments {arguments}')

        files = os.listdir(self.config_manager.workspace_dir)

        output = "These are the files in your workspace:\n\n"
        for file in files:
            output += f"{file}\n"

        return output
