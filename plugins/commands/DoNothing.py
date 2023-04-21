from plugins.BasePlugin import BasePlugin


class DoNothing(BasePlugin):
    def __init__(self, plugin_manager: object):
        self.command = "do_nothing"
        self.description = "Do Nothing"
        self.arguments = {"reason": "<reason>"}
        self.returns = None
        self.feed_back = False
        self.plugin_manager = plugin_manager

    def register(self):
        return self.command, self.description, self.arguments, self.returns, self.feed_back

    def run_plugin(self, arguments: dict[str, any]):
        self.plugin_manager.logger.info(f'Command {self.command} called, reason: {arguments["reason"]}')
        return None
