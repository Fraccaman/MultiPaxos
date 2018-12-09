from typing import Dict, List


class LeanerInstance:

    def __init__(self):
        self.waiting_instances: Dict[int, int] = {}
        self.ordered_values: List = []
        self.last_ordered_instance = -1

    def add_instance(self, test, instance: int, value: int):
        if self.last_ordered_instance + 1 == instance:
            self.ordered_values.append(value)
            self.last_ordered_instance = instance

            # test.log.debug("yes {}".format(self.last_ordered_instance))

            while self.waiting_instances and self.last_ordered_instance + 1 in self.waiting_instances:
                # test.log.debug("yes 2")
                self.ordered_values.append(self.waiting_instances.get(self.last_ordered_instance + 1))
                del self.waiting_instances[self.last_ordered_instance + 1]
                self.last_ordered_instance = self.last_ordered_instance + 1

            return self.ordered_values[instance:]
        else:
            # test.log.debug("not")
            self.waiting_instances[instance] = value
