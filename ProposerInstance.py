import threading
from enum import Enum
from typing import NoReturn, TYPE_CHECKING

from Message import MessageOneB, MessageTwoB
from util.ThreadTimer import ThreadTimer

if TYPE_CHECKING:
    pass

lock = threading.Lock()


class Phase(Enum):
    one = "PhaseOne - ️️🅰️"
    two = "PhaseTwo - ️🅱️️"


class ProposerInstance:

    def __init__(self, value: int, c_round: int, instance: int):
        self.instance = instance
        self.to_be_proposed = value
        self.c_round = c_round
        self.phase_one_b_messages = []
        self.phase_two_b_messages = []
        self.phase_one_a_timeout = None
        self.phase_two_a_timeout = None
        self.one_b_majority_reached: bool = False
        self.two_b_majority_reached: bool = False
        self.is_delivered = False

    def add_message_one_b(self, message: MessageOneB):
        self.phase_one_b_messages.append(message)

    def add_message_two_b(self, message: MessageTwoB):
        self.phase_two_b_messages.append(message)

    def is_majority_one_b(self, c_round: int) -> bool:

        if len(list(filter(lambda msg: msg.round is c_round,
                           self.phase_one_b_messages))) > 1 and not self.one_b_majority_reached:
            self.one_b_majority_reached = True
            return True
        else:
            return False

    def is_majority_two_b(self):
        if len(list(filter(lambda msg: msg.v_round is self.c_round,
                           self.phase_two_b_messages))) > 1 and not self.two_b_majority_reached:
            self.two_b_majority_reached = True
            return True
        else:
            return False

    def get_largest_v_round(self) -> int:
        return max([msg.v_round for msg in self.phase_one_b_messages])

    def get_v_set(self, k: int):
        return set(filter(lambda msg: msg.v_round is k, self.phase_one_b_messages))
