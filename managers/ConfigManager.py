import os

from dotenv import load_dotenv


class ConfigManager:
    def __init__(self, agent: object):
        load_dotenv()
        self.agent = agent
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.verbose = os.environ.get("AUTOMATRON_VERBOSE") == "Yes"
        self.workspace_dir = os.environ.get("AGENT_WORKSPACE") or "workspace"
        self.google_cse_developer_key = os.environ.get("GOOGLE_CSE_DEVELOPER_KEY")
        self.google_cse_cx = os.environ.get("GOOGLE_CSE_CX")

    # noinspection PyUnresolvedReferences
    def verify_config(self) -> bool:
        # Verifies if all required API keys have been edited by the user.
        if self.openai_api_key is None or self.openai_api_key == "<your OpenAI API key>":
            self.agent.logger.error("OPENAPI_API_KEY is not set in the .env file!")
            return False

        if self.google_cse_developer_key is None or \
                self.google_cse_developer_key == "<your Google Custom Search Engine developer key>":
            self.agent.logger.error("GOOGLE_CSE_API_KEY is not set in the .env file!")
            return False

        if self.google_cse_cx is None or self.google_cse_cx == "<your Google Custom Search Engine ID (called cx)>":
            self.agent.logger.error("GOOGLE_CSE_CX is not set in the .env file!")
            return False

        return True
