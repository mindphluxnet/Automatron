import json


class PromptGenerator:
    def __init__(self):
        self.constraints = []
        self.commands = []
        self.resources = []
        self.performance_evaluation = []
        self.response_format = {
            "thoughts": {
                "text": "thought",
                "reasoning": "reasoning",
                "plan": "- short bulleted\n- list that conveys\n- long-term plan",
                "criticism": "constructive self-criticism",
            },
            "command": {"name": "command name", "args": {"arg name": "value"}},
        }

    def add_constraint(self, constraint: str):
        self.constraints.append(constraint)

    def add_command(self, label: str, command: str, arguments=None):
        if arguments is None:
            arguments = {}

        command_args = {arg_key: arg_value for arg_key, arg_value in arguments.items()}

        command = {"label": label, "command": command, "arguments": command_args}

        self.commands.append(command)

    @staticmethod
    def _generate_command_string(command: dict[str, any]) -> str:
        """
        Generate a formatted string representation of a command.

        Args:
            command (dict): A dictionary containing command information.

        Returns:
            str: The formatted command string.
        """
        args_string = ", ".join(
            f'"{key}": "{value}"' for key, value in command["arguments"].items()
        )
        if args_string.strip() == "":
            return f'{command["label"]}: "{command["command"]}"'

        return f'{command["label"]}: "{command["command"]}", args: {args_string}'

    def add_resource(self, resource: str) -> None:
        """
        Add a resource to the resources list.

        Args:
            resource (str): The resource to be added.
        """
        self.resources.append(resource)

    def add_performance_evaluation(self, evaluation: str) -> None:
        """
        Add a performance evaluation item to the performance_evaluation list.

        Args:
            evaluation (str): The evaluation item to be added.
        """
        self.performance_evaluation.append(evaluation)

    def _generate_numbered_list(self, items: list[any], item_type="list") -> str:
        """
        Generate a numbered list from given items based on the item_type.

        Args:
            items (list): A list of items to be numbered.
            item_type (str, optional): The type of items in the list.
                Defaults to 'list'.

        Returns:
            str: The formatted numbered list.
        """
        if item_type == "command":
            return "\n".join(
                f"{i + 1}. {self._generate_command_string(item)}"
                for i, item in enumerate(items)
            )
        else:
            return "\n".join(f"{i + 1}. {item}" for i, item in enumerate(items))

    def generate_prompt_string(self) -> str:
        """
        Generate a prompt string based on the constraints, commands, resources,
            and performance evaluations.

        Returns:
            str: The generated prompt string.
        """
        formatted_response_format = json.dumps(self.response_format, indent=4).replace('{', '{{').replace('}', '}}')
        return (
            f"Constraints:\n{self._generate_numbered_list(self.constraints)}\n\n"
            "Commands:\n"
            f"{self._generate_numbered_list(self.commands, item_type='command')}\n\n"
            f"Resources:\n{self._generate_numbered_list(self.resources)}\n\n"
            "Performance Evaluation:\n"
            f"{self._generate_numbered_list(self.performance_evaluation)}\n\n"
            "You should only respond in JSON format as described below \nResponse"
            f" Format: \n{formatted_response_format} \nEnsure the response can be"
            " parsed by Python json.loads\n\n"
            "{question}"
        )
