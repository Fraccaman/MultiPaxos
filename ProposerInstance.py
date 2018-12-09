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

    def start_timeout(self, timeout_type: Phase, f, *args, timeout: int = 3) -> NoReturn:
        timer = ThreadTimer(timeout, f, args[0], args[1])
        if timeout_type is Phase.one and self.phase_one_a_timeout is None:
            # print('t1 start {}'.format(self.phase_one_a_timeout))
            self.phase_one_a_timeout = timer
        elif timeout_type is Phase.two and self.phase_two_a_timeout is None:
            # print('t2 start {}'.format(self.phase_two_a_timeout))
            self.phase_two_a_timeout = timer

    def stop_timeout(self, timeout_type: Phase) -> NoReturn:
        if timeout_type is Phase.one and self.phase_one_a_timeout is not None:
            # print('t1 stop {} - {}'.format(self.phase_one_a_timeout, self.instance))
            self.phase_one_a_timeout.stop()
            del self.phase_one_a_timeout
            self.phase_one_a_timeout = None
        elif timeout_type is Phase.two and self.phase_two_a_timeout is not None:
            # print('t2 stop {} - {}'.format(self.phase_two_a_timeout, self.instance))
            self.phase_two_a_timeout.stop()
            del self.phase_two_a_timeout
            self.phase_two_a_timeout = None

    def get_largest_v_round(self) -> int:
        return max([msg.v_round for msg in self.phase_one_b_messages])

    def get_v_set(self, k: int):
        return set(filter(lambda msg: msg.v_round is k, self.phase_one_b_messages))
