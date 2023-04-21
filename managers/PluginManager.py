import importlib.util
import os
from wryte import Wryte


class PluginManager:
    def __init__(self, agent, plugin_dir: str):
        self.agent = agent
        self.plugin_dir = plugin_dir
        self.plugins = {}
        self.logger = Wryte(name="PluginManager")

    def enumerate_plugins(self, plugin_type: str = "commands"):
        for plugin in os.listdir(os.path.join(self.plugin_dir, plugin_type)):
            if plugin.endswith('.py'):
                plugin_file_name = plugin[:-3]
                class_ = self._get_from_module(f"plugins.{plugin_type}.{plugin_file_name}", plugin_file_name)
                if class_ is not None:
                    plugin_ = class_(self)
                    command, description, arguments, returns, feed_back = plugin_.register()
                    self.plugins[command] = {"file_name": plugin_file_name,
                                             "module": f"plugins.{plugin_type}.{plugin_file_name}",
                                             "description": description, "arguments": arguments, "returns": returns,
                                             "feed_back": feed_back}
                    self.logger.info(f"plugins.{plugin_type}.{plugin_file_name} registered successfully")
                else:
                    self.logger.warning(f"Invalid {plugin_type} plugin: {plugin_file_name}!")

    def get_plugins(self):
        return self.plugins

    def run_plugin(self, command: str, arguments: dict[any]):
        if command not in self.plugins:
            self.logger.error(f"No plugin found for command {command}")
            return

        class_ = self._get_from_module(self.plugins[command]["module"], self.plugins[command]['file_name'])
        if class_ is not None:
            return class_(self).run_plugin(arguments)
        else:
            self.logger.error(f'Plugin {self.plugins["command"]["module"]} could not be run')
            return None

    def is_valid_response(self, command: str, response: any):
        if self.plugins[command]["returns"] is None and response is None:
            return True
        else:
            return isinstance(response, self.plugins[command]["returns"])

    def do_feed_back(self, command: str):
        print(command)
        return self.plugins[command]["feed_back"]

    @staticmethod
    def _get_from_module(module: str, attr_name: str):
        module = importlib.import_module(module)
        try:
            return getattr(module, attr_name)
        except AttributeError:
            return None
