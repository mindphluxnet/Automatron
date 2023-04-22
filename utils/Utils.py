import time
from colorama import Style, Fore


def wait(seconds: int, reason: str) -> None:
    remaining_time = seconds
    while remaining_time > 0:
        if remaining_time == 1:
            plural = ""
        else:
            plural = "s"

        print(f'{reason}, waiting {Fore.YELLOW}{remaining_time}{Style.RESET_ALL} second{plural} before retrying. '
              f'Press {Fore.LIGHTBLUE_EX}Ctrl+C{Style.RESET_ALL} to abort.', end="\r")
        time.sleep(1)
        remaining_time -= 1


def is_true(value: str) -> bool:
    # Needed because environment variables are strings.
    return value == "Yes" or value == "True"
