class FixJSON:
    @staticmethod
    def fix(input_: str) -> str:
        tmp = input_.strip()
        if tmp == "":
            return ""

        tmp = FixJSON.fix_brackets(tmp)
        tmp = FixJSON.remove_leading_text(tmp)

        return tmp

    @staticmethod
    def fix_brackets(input_: str) -> str:
        return f"[{input_}]"

    @staticmethod
    def remove_leading_text(input_: str) -> str:
        output = input_.replace("[Response:", "[")
        output = output.replace("[Response Format:", "[")
        return output
