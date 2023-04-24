import time
from colorama import Style, Fore
import subprocess


class Utils:
    def __init__(self, agent: object):
        self.agent = agent

    # noinspection PyUnresolvedReferences
    def wait(self, seconds: int, reason: str) -> None:
        remaining_time = seconds
        while remaining_time > 0:
            if remaining_time == 1:
                plural = ""
            else:
                plural = "s"

            print(f'[{Fore.YELLOW}${self.agent.cost_manager.get_session_cost():.2f}{Style.RESET_ALL}] {reason},'
                  f' waiting {Fore.YELLOW}{remaining_time}{Style.RESET_ALL} second{plural} before retrying. '
                  f'Press {Fore.LIGHTBLUE_EX}Ctrl+C{Style.RESET_ALL} to abort.', end="\r")
            time.sleep(1)
            remaining_time -= 1

    @staticmethod
    def is_git_installed() -> bool:
        try:
            result = subprocess.check_output(["git", "--version"]).decode("utf-8")
            if "git version" in result:
                return True
        except subprocess.CalledProcessError:
            pass

        return False
