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

    def register(self) -> tuple:
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]) -> None:
        # This is a virtual command. It's catched by the main loop and is never executed.
        exit()
