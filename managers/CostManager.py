import json
import os
from wryte import Wryte


class CostManager:
    def __init__(self):
        self.total_cost = 0
        self.session_cost = 0
        self.load()
        self.logger = Wryte("CostManager")
        if not os.path.exists("etc"):
            os.mkdir("etc")

    def clear_total_cost(self) -> None:
        self.total_cost = 0

    def clear_session_cost(self) -> None:
        self.session_cost = 0

    def add_cost(self, cost: float) -> None:
        self.total_cost += cost
        self.session_cost += cost

    def get_total_cost(self) -> float:
        return self.total_cost

    def get_session_cost(self) -> float:
        return self.session_cost

    def save(self) -> None:
        with open("etc/costs.json", "w") as f:
            f.write(json.dumps({"total_cost": self.total_cost}, indent=4))

    def load(self) -> None:
        if os.path.isfile("etc/costs.json"):
            with open("etc/costs.json", "r") as f:
                json_ = f.read()
                data = json.loads(json_)
                self.total_cost = float(data["total_cost"])

    def print_cost_report(self) -> None:
        self.logger.info(f"Session cost: ${self.get_session_cost():.2f}")
        self.logger.info(f"Total cost: ${self.get_total_cost():.2f}")
