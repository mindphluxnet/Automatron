from plugins.BasePlugin import BasePlugin
from dotenv import load_dotenv
import os


class WriteFile(BasePlugin):
    def __init__(self, plugin_manager: object):
        load_dotenv()
        self.command = "write_file"
        self.description = "Write text to a file"
        self.arguments = {"file_name": "<file name>", "content": "<the text to write>"}
        self.returns = str
        self.feed_back = True
        self.priority = 0
        self.plugin_manager = plugin_manager

    def register(self):
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]):
        # noinspection PyUnresolvedReferences
        self.plugin_manager.logger.info(f'Command {self.command} called with arguments {arguments}')
        if not os.path.isfile(os.path.join(self.plugin_manager.agent.config_manager.workspace_dir, arguments["file_name"])):
            with open(os.path.join(self.plugin_manager.agent.config_manager.workspace_dir, arguments["file_name"]), "w") as f:
                f.write(arguments["content"])
                return f'The file {arguments["file_name"]} has been written successfully.'

        return f'The file {arguments["file_name"]} already existed in your workspace. You might want to use ' \
               f'the "append_file" command instead.'
