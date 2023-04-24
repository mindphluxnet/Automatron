from plugins.BasePlugin import BasePlugin
import sys
import subprocess
# noinspection PyDeprecation
import pkg_resources


class PythonInstallModule(BasePlugin):
    # noinspection PyUnresolvedReferences
    def __init__(self, plugin_manager: object):
        self.plugin_manager = plugin_manager
        self.config_manager = self.plugin_manager.agent.config_manager
        self.command = "install_python_module"
        self.description = "Install a Python module"
        self.arguments = {"input": "<module name>"}
        self.returns = str
        self.feed_back = True
        self.priority = 0

    def register(self) -> tuple:
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    # noinspection PyUnresolvedReferences
    def run_plugin(self, arguments: dict[str, any]) -> str:
        self.plugin_manager.logger.info(f'Command {self.command} called with arguments {arguments}')
        # noinspection PyDeprecation
        installed_modules = {pkg.key for pkg in pkg_resources.working_set}
        if not arguments["input"] in installed_modules:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", arguments["input"]],
                                      stdout=subprocess.DEVNULL)
                if self.config_manager.verbose:
                    self.plugin_manager.logger.info(f'Python module {arguments["input"]} installed successfully')

                return f'The Python module {arguments["input"]} has been installed successfully.'
            except subprocess.CalledProcessError:
                if self.config_manager.verbose:
                    self.plugin_manager.logger.info(f'Python module {arguments["input"]} could not be installed due'
                                                    f' to an error')
                return f'The Python module {arguments["input"]} could not be installed due to an error.'
        else:
            if self.config_manager.verbose:
                self.plugin_manager.logger.info(f'Python module {arguments["input"]} was already installed')
            # Claim it has been installed even if it already was before so ChatGPT doesn't freak out.
            return f'The Python module {arguments["input"]} has been installed successfully.'
