from langchain.callbacks import get_openai_callback

from managers.CostManager import CostManager
from managers.PluginManager import PluginManager
from prompts.PromptBuilder import PromptBuilder
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from dotenv import load_dotenv
import json
from wryte import Wryte
from utils.FixJSON import FixJSON


class Agent:
    def __init__(self):
        self.plugin_manager = PluginManager(self, "plugins")
        self.plugin_manager.enumerate_plugins()

        self.prompt_builder = PromptBuilder(self)
        self.cost_manager = CostManager()
        self.logger = Wryte("Agent")
        self.wait_time = 0

        load_dotenv()

    def query(self, question: str) -> str:
        template = self.prompt_builder.build()
        prompt = PromptTemplate(template=template, input_variables=["question"])

        llm = OpenAI()
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        with get_openai_callback() as cb:
            response = llm_chain.run(question)
            self.cost_manager.add_cost(cb.total_cost)
            self.cost_manager.save()
            print(response)
            response_ = FixJSON().fix(response)
            if not response_ == "":
                try:
                    json_ = json.loads(response_, strict=False)
                    return json_, 0, ""
                except json.JSONDecodeError:
                    self.wait_time += 10
                    return False, self.wait_time, "Invalid JSON returned by ChatGPT"

            self.wait_time += 10
            return False, self.wait_time, "Empty response returned by ChatGPT"
