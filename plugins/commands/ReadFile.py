from plugins.BasePlugin import BasePlugin
from dotenv import load_dotenv
import os


class ReadFile(BasePlugin):
    def __init__(self, plugin_manager: object):
        load_dotenv()
        self.command = "read_file"
        self.description = "Read text from a file"
        self.arguments = {"file_name": "<file name>"}
        self.returns = str
        self.feed_back = True
        self.plugin_manager = plugin_manager

    def register(self):
        return self.command, self.description, self.arguments, self.returns, self.feed_back

    def run_plugin(self, arguments: dict[str, any]):
        self.plugin_manager.logger.info(f'Command {self.command} called with argument: {arguments["file_name"]}')
        if os.path.isfile(os.path.join(os.environ["AGENT_WORKSPACE"], arguments["file_name"])):
            with open(os.path.join(os.environ["AGENT_WORKSPACE"], arguments["file_name"]), "r") as f:
                contents = f.read()
                return f'The contents of the file {arguments["file_name"]} are:\n\n{contents}'

        return f'The file {arguments["file_name"]} does not exist in your workspace.'
