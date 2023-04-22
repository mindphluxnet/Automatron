import os

from agents.Agent import Agent
from colorama import init, Fore, Style
from halo import Halo
from utils.Utils import wait


def run_command(command: str, arguments: dict[str, any]):
    result_ = agent.plugin_manager.run_plugin(command, arguments)
    if result_:
        if agent.plugin_manager.is_valid_response(command, result_):
            return result_

    return None


if __name__ == "__main__":
    agent = Agent()
    init()
    keep_going = True
    round_count = 0
    rerun_query = None
    next_query = None

    if not os.path.exists(os.environ["AGENT_WORKSPACE"]):
        os.mkdir(os.environ["AGENT_WORKSPACE"])

    while keep_going:
        if not rerun_query and not next_query:
            query = input(f"[{Fore.YELLOW}${agent.cost_manager.get_session_cost():.2f}{Style.RESET_ALL}] "
                          f"Enter your question ({Fore.CYAN}[q]{Style.RESET_ALL} to quit): ")
            query = query.strip()
        elif rerun_query is not None:
            query = rerun_query
            rerun_query = None
        elif next_query is not None:
            do_continue = input(f"[{Fore.YELLOW}${agent.cost_manager.get_session_cost():.2f}{Style.RESET_ALL}] "
                                f"Agent wants to continue with the next query, press {Fore.CYAN}Enter{Style.RESET_ALL}"
                                f" or ({Fore.CYAN}[q]{Style.RESET_ALL} to quit): ")
            if do_continue.lower() == "q":
                exit()
            query = next_query
        # noinspection PyUnboundLocalVariable
        if query == "q":
            exit(0)
        else:
            with Halo(text='AI is thinking ...', spinner='dots'):
                result, wait_time, wait_reason = agent.query(query)

            if result:
                if "name" in result[0]["command"]:
                    print(f'[{Fore.YELLOW}${agent.cost_manager.get_session_cost():.2f}{Style.RESET_ALL}] '
                          f'{Fore.GREEN}Agent wants to execute command {Style.RESET_ALL}{Fore.CYAN}'
                          f'{result[0]["command"]["name"]}{Style.RESET_ALL}{Fore.GREEN} with params {Style.RESET_ALL}'
                          f'{Fore.YELLOW}{result[0]["command"]["args"]}{Style.RESET_ALL}')

                    command_to_run = result[0]["command"]["name"]
                    result = run_command(command_to_run, result[0]["command"]["args"])

                    if result is not None:
                        if agent.plugin_manager.do_feed_back(command_to_run):
                            next_query = result

                else:
                    print(f'[{Fore.YELLOW}${agent.cost_manager.get_session_cost():.2f}{Style.RESET_ALL}] '
                          f'{Fore.GREEN}Agent response:{Style.RESET_ALL} {result[0]["thoughts"]["text"]}')
            else:
                if wait_time > 0:
                    wait(wait_time, wait_reason)
                    rerun_query = query
