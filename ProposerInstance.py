from enum import Enum
from threading import Lock
from typing import TYPE_CHECKING, List, NoReturn, Set

from Message import MessageOneB, MessageTwoB

if TYPE_CHECKING:
    pass

lock_phase_one = Lock()
lock_phase_two = Lock()


class Phase(Enum):
    one = "PhaseOne - ️️🅰️"
    two = "PhaseTwo - ️🅱️️"


class ProposerInstance:

    def __init__(self, value: int, c_round: int, instance: int):
        self.instance: int = instance
        self.to_be_proposed: int = value
        self.c_round: int = c_round
        self.phase_one_b_messages: List = []
        self.phase_two_b_messages: List = []
        self.one_b_majority_reached: bool = False
        self.two_b_majority_reached: bool = False
        self.is_delivered: bool = False

    def add_message_one_b(self, message: MessageOneB) -> NoReturn:
        self.phase_one_b_messages.append(message)

    def add_message_two_b(self, message: MessageTwoB) -> NoReturn:
        self.phase_two_b_messages.append(message)

    def is_majority_one_b(self, c_round: int) -> bool:
        lock_phase_one.acquire()
        try:
            if len(list(filter(lambda msg: msg.round is c_round,
                               self.phase_one_b_messages))) > 1 and not self.one_b_majority_reached:
                self.one_b_majority_reached = True
                return True
            else:
                return False
        finally:
            lock_phase_one.release()

    def is_majority_two_b(self) -> bool:
        lock_phase_two.acquire()
        try:
            if len(list(filter(lambda msg: msg.v_round is self.c_round,
                               self.phase_two_b_messages))) > 1 and not self.two_b_majority_reached:
                self.two_b_majority_reached = True
                return True
            else:
                return False
        finally:
            lock_phase_two.release()

    def get_largest_v_round(self) -> int:
        return max([msg.v_round for msg in self.phase_one_b_messages])

    def get_v_set(self, k: int) -> Set:
        return set(filter(lambda msg: msg.v_round is k, self.phase_one_b_messages))
