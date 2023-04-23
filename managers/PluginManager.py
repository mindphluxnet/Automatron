import importlib.util
import os
from wryte import Wryte


class PluginManager:
    def __init__(self, agent, plugin_dir: str):
        self.agent = agent
        self.plugin_dir = plugin_dir
        self.plugins = {}
        self.logger = Wryte(name="PluginManager")

    def enumerate_plugins(self, plugin_type: str = "commands") -> None:
        # Dynamically loads each plugin from the plugins directory and calls its register() method
        # to get all relevant information about the plugin.
        for plugin in os.listdir(os.path.join(self.plugin_dir, plugin_type)):
            if plugin.endswith('.py'):
                plugin_file_name = plugin[:-3]
                class_ = self._get_from_module(f"plugins.{plugin_type}.{plugin_file_name}", plugin_file_name)
                if class_ is not None:
                    plugin_ = class_(self)
                    command, description, arguments, returns, feed_back, priority = plugin_.register()
                    self.plugins[command] = {"file_name": plugin_file_name,
                                             "module": f"plugins.{plugin_type}.{plugin_file_name}",
                                             "description": description, "arguments": arguments, "returns": returns,
                                             "feed_back": feed_back, "priority": priority}

                    if self.agent.config_manager.verbose:
                        self.logger.info(f"registered plugins.{plugin_type}.{plugin_file_name}")
                else:
                    self.logger.warning(f"Invalid {plugin_type} plugin: {plugin_file_name}!")

        # Sort plugins by priority with order highest > lowest.
        self.plugins = dict(sorted(self.plugins.items(),
                                   key=lambda x: x[1]['priority'] if x[1]['priority'] != 0 else float('inf')))

    def get_plugins(self) -> dict:
        return self.plugins

    def run_plugin(self, command: str, arguments: dict[any]):
        # Dynamically loads the plugin script for the given command and calls the run_plugin() method with
        # the supplied arguments.
        if command not in self.plugins:
            self.logger.error(f"No plugin found for command {command}")
            return

        class_ = self._get_from_module(self.plugins[command]["module"], self.plugins[command]['file_name'])
        if class_ is not None:
            return class_(self).run_plugin(arguments)
        else:
            self.logger.error(f'Plugin {self.plugins["command"]["module"]} could not be run')
            return None

    def is_valid_response(self, command: str, response: any) -> bool:
        # Plugins with no return value should return None.
        if self.plugins[command]["returns"] is None and response is None:
            return True
        else:
            # True if the response return value is of the type advertised by the plugin.
            # TODO: This could be solved better by querying the arrow notation of the run_plugin() method.
            return isinstance(response, self.plugins[command]["returns"])

    def should_feed_back(self, command: str) -> bool:
        # If the plugin needs to send back data to ChatGPT (search results etc.) this needs
        # to be set to True.
        return self.plugins[command]["feed_back"]

    @staticmethod
    # https://stackoverflow.com/a/69648743
    def _get_from_module(module: str, attr_name: str):
        module = importlib.import_module(module)
        try:
            return getattr(module, attr_name)
        except AttributeError:
            return None
