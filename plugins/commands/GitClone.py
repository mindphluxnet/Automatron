from plugins.BasePlugin import BasePlugin
import dload
import os
from urllib.parse import urlparse


class GitClone(BasePlugin):
    def __init__(self, plugin_manager: object):
        self.plugin_manager = plugin_manager
        self.config_manager = self.plugin_manager.agent.config_manager
        self.command = "github_clone"
        self.description = "Clone a Github repository to your workspace directory"
        self.arguments = {"input": "name of github repository"}
        self.returns = str
        self.feed_back = True
        self.priority = 0

    def register(self) -> tuple:
        return self.command, self.description, self.arguments, self.returns, self.feed_back, self.priority

    def run_plugin(self, arguments: dict[str, any]) -> str:
        self.plugin_manager.logger.info(f'Command {self.command} called with arguments {arguments}')
        github_link = arguments["input"]
        parsed_link = urlparse(github_link)
        if parsed_link.hostname.lower() is not "github":
            return f'Invalid Github link: {github_link}'

        repo_name = parsed_link.path.split("/")[2]

        if os.path.exists(os.path.join(self.config_manager.workspace_dir, repo_name)):
            # ChatGPT doesn't have to know if the repository already existed to minimize the chance it freaks out.
            return f'The Github repository {repo_name} has been cloned successfully'
        else:
            result = dload.git_clone(git_url=github_link,
                                     clone_dir=os.path.join(self.config_manager.workspace_dir, repo_name))
            if result.strip() == "":
                if self.config_manager.verbose:
                    self.plugin_manager.logger.info(f'The Github repository {github_link} could'
                                                    f' not be cloned due to an error')
                return f"The Github repository {github_link} could not be cloned"

            if self.config_manager.verbose:
                self.plugin_manager.logger.info(f'The Github repository {github_link} has been cloned successfully')
            return f'The Github repository {repo_name} has been cloned successfully'
