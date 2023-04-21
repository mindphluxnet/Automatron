from plugins.BasePlugin import BasePlugin
from dotenv import load_dotenv
import os


class AppendFile(BasePlugin):
    def __init__(self, plugin_manager: object):
        load_dotenv()
        self.command = "append_file"
        self.description = "Append text to a file"
        self.arguments = {"file_name": "<file name>", "content": "<the text to write>"}
        self.returns = str
        self.feed_back = True
        self.priority = 0
        self.plugin_manager = plugin_manager

    def register(self):
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]):
        self.plugin_manager.logger.info(f'Command {self.command} called with arguments: {arguments}')
        if os.path.isfile(os.path.join(os.environ["AGENT_WORKSPACE"], arguments["file_name"])):
            with open(os.path.join(os.environ["AGENT_WORKSPACE"], arguments["file_name"]), "a") as f:
                f.write(arguments["content"])
                return f'The file {arguments["file_name"]} has been appended to successfully.'

        return f'The file {arguments["file_name"]} does not exist in your workspace. You might want to use ' \
               f'the "write_file" command instead.'
