from typing import Dict, List


class LearnerInstance:

    def __init__(self):
        self.waiting_instances: Dict[int, int] = {}
        self.ordered_values: List = []
        self.last_ordered_instance = -1
        self.catch_up: Dict[str, List] = {}
        self.catch_up_size: Dict[str, (int, int)] = {}
        self.is_catching_up: int = True

    def add_instance(self, instance: int, value: int):
        if instance == 0:
            self.is_catching_up = False
        if self.last_ordered_instance + 1 == instance:
            self.ordered_values.append(value)
            self.last_ordered_instance = instance

            while self.last_ordered_instance + 1 in self.waiting_instances:
                self.ordered_values.append(self.waiting_instances.get(self.last_ordered_instance + 1))
                del self.waiting_instances[self.last_ordered_instance + 1]
                self.last_ordered_instance = self.last_ordered_instance + 1

            return self.ordered_values[instance:]
        else:
            self.waiting_instances[instance] = value
