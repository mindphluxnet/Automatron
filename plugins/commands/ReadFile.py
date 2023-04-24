from plugins.BasePlugin import BasePlugin
import os


class ReadFile(BasePlugin):
    # noinspection PyUnresolvedReferences
    def __init__(self, plugin_manager: object):
        self.plugin_manager = plugin_manager
        self.config_manager = self.plugin_manager.agent.config_manager
        self.command = "read_file"
        self.description = "Read text from a file"
        self.arguments = {"file_name": "<file name>"}
        self.returns = str
        self.feed_back = True
        self.priority = 0

    def register(self) -> tuple:
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    # noinspection PyUnresolvedReferences
    def run_plugin(self, arguments: dict[str, any]) -> str:
        if self.config_manager.verbose:
            self.plugin_manager.logger.info(f'Command {self.command} called with arguments {arguments}')

        if os.path.isfile(os.path.join(self.config_manager.workspace_dir, arguments["file_name"])):
            with open(os.path.join(self.config_manager.workspace_dir, arguments["file_name"]), "r") as f:
                contents = f.read()
                return f'The contents of the file {arguments["file_name"]} are:\n\n{contents}'

        return f'The file {arguments["file_name"]} does not exist in your workspace.'
