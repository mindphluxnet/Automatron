from plugins.BasePlugin import BasePlugin
import os


class DeleteFile(BasePlugin):
    def __init__(self, plugin_manager: object):
        self.plugin_manager = plugin_manager
        self.config_manager = self.plugin_manager.agent.config_manager
        self.command = "delete_file"
        self.description = "Delete a file from your workspace"
        self.arguments = {"file_name": "<file name>"}
        self.returns = str
        self.feed_back = True
        self.priority = 0

    def register(self):
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]):
        if self.config_manager.verbose:
            self.plugin_manager.logger.info(f'Command {self.command} called with arguments: {arguments}')

        if os.path.isfile(os.path.join(self.config_manager.workspace_dir, arguments["file_name"])):
            os.remove(os.path.join(self.config_manager.workspace_dir, arguments["file_name"]))
            return f'The file {arguments["file_name"]} has been deleted successfully.'

        return f'The file {arguments["file_name"]} does not exist in your workspace.'
