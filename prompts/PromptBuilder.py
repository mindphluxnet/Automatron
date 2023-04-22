from prompts.PromptGenerator import PromptGenerator


class PromptBuilder:
    def __init__(self, agent) -> str:
        self.agent = agent
        self.prompt_generator = PromptGenerator()

        self.prompt_generator.add_constraint(
            "~4000 word limit for short term memory. Your short term memory is short, so"
            " immediately save important information to files."
        )
        self.prompt_generator.add_constraint("No user assistance")
        self.prompt_generator.add_constraint(
            'Exclusively use the commands listed in double quotes e.g. "command name"'
        )
        self.prompt_generator.add_constraint(
            "Use subprocesses for commands that will not terminate within a few minutes"
        )
        self.prompt_generator.add_constraint("Do not use Google search if you already have the answer.")

        commands = []
        commands_ = self.agent.plugin_manager.get_plugins()
        for key, value in commands_.items():
            commands.append((value["description"], key, value["arguments"]))

        for command_label, command_name, args in commands:
            self.prompt_generator.add_command(command_label, command_name, args)

        self.prompt_generator.add_resource(
            "Internet access for searches and information gathering."
        )
        self.prompt_generator.add_resource("Long Term memory management.")
        self.prompt_generator.add_resource(
            "GPT-3.5 powered Agents for delegation of simple tasks."
        )
        self.prompt_generator.add_resource("File output.")

        self.prompt_generator.add_performance_evaluation(
            "Continuously review and analyze your actions to ensure you are performing to"
            " the best of your abilities."
        )
        self.prompt_generator.add_performance_evaluation(
            "Constructively self-criticize your big-picture behavior constantly."
        )
        self.prompt_generator.add_performance_evaluation(
            "Reflect on past decisions and strategies to refine your approach."
        )
        self.prompt_generator.add_performance_evaluation(
            "Every command has a cost, so be smart and efficient. Aim to complete tasks in"
            " the least number of steps."
        )

    def build(self) -> str:
        return self.prompt_generator.generate_prompt_string()
