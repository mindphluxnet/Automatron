from langchain import PromptTemplate, LLMChain
from langchain.callbacks import get_openai_callback

from langchain.llms import OpenAI
from wryte import Wryte
import json

from managers.ConfigManager import ConfigManager
from managers.CostManager import CostManager
from managers.PluginManager import PluginManager
from prompts.PromptBuilder import PromptBuilder
from utils.FixJSON import FixJSON


class Agent:
    def __init__(self):
        self.logger = Wryte("Agent")
        self.config_manager = ConfigManager(self)

        if not self.config_manager.verify_config():
            exit()
        else:
            if self.config_manager.verbose:
                self.logger.info("Config loaded and verified")

        self.plugin_manager = PluginManager(self, "plugins")
        self.plugin_manager.enumerate_plugins()
        self.prompt_builder = PromptBuilder(self)
        self.cost_manager = CostManager()
        self.wait_time = 0

    def query(self, question: str) -> str:
        template = self.prompt_builder.build()
        prompt = PromptTemplate(template=template, input_variables=["question"])

        if self.config_manager.verbose:
            print(prompt)

        llm = OpenAI()
        llm.openai_api_key = self.config_manager.openai_api_key

        llm_chain = LLMChain(prompt=prompt, llm=llm)
        with get_openai_callback() as cb:
            response = llm_chain.run(question)
            self.cost_manager.add_cost(cb.total_cost)
            self.cost_manager.save()

            # Fix some common errors in JSON responses.
            response_ = FixJSON().fix(response)
            if not response_ == "":
                try:
                    json_ = json.loads(response_, strict=False)

                    if self.config_manager.verbose:
                        from pprint import pprint
                        pprint(json_)

                    # API is returning data, reset wait_time
                    self.wait_time = 0
                    return json_, self.wait_time, ""
                except json.JSONDecodeError:
                    self.wait_time += 10
                    return False, self.wait_time, "Invalid JSON returned by ChatGPT"

            self.wait_time += 10
            return False, self.wait_time, "Empty response returned by ChatGPT"
