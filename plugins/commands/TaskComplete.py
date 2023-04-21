from plugins.BasePlugin import BasePlugin


class TaskComplete(BasePlugin):
    def __init__(self, plugin_manager: object):
        self.command = "task_complete"
        self.description = "Task Complete (Shutdown)"
        self.arguments = {"reason": "<reason>"}
        self.returns = None
        self.feed_back = False
        self.priority = -100
        self.plugin_manager = plugin_manager

    def register(self):
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]):
        self.plugin_manager.logger.info(f'Command {self.command} called, reason: {arguments["reason"]}')
        exit()
