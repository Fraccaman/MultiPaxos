import pickle
import uuid
from enum import Enum


class MessageType(Enum):
    oneA = "Prepare - 1A - 1️🅰️"
    oneB = "Promise - 1B - 1️🅱️"
    twoA = "Accept - 2A - 2️🅰️"
    twoB = "Accepted - 2B - 2️🅱️"
    client = "Propose - 🔢"
    leader = "Leader - 👑"
    hearthbeat = "Hearthbeat - ❤️"
    decision = "Decision - 🔨"


class Message:

    def __init__(self, msg_type: MessageType):
        self.msg_type: MessageType = msg_type

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(message):
        return pickle.loads(message)


class MessageOneA(Message):

    def __init__(self, c_round: int, instance: int):
        super().__init__(MessageType.oneA)
        self.c_round: int = c_round
        self.instance: int = instance

    def __str__(self):
        return "{} - c_round: {}, instance: {}".format(self.msg_type, self.c_round, self.instance)


class MessageOneB(Message):

    def __init__(self, round: int, v_round: int, v_val: int, instance: int):
        super().__init__(MessageType.oneB)
        self.round: int = round
        self.v_round: int = v_round
        self.v_val: int = v_val
        self.instance: int = instance

    def __str__(self):
        return "{} - round: {}, v_round: {}, v_val: {}, instance: {}".format(self.msg_type, self.round, self.v_round,
                                                                             self.v_val, self.instance)


class MessageTwoA(Message):

    def __init__(self, c_round: int, c_val: int, instance: int):
        super().__init__(MessageType.twoA)
        self.c_round: int = c_round
        self.c_val: int = c_val
        self.instance: int = instance

    def __str__(self):
        return "{} - c_round: {}, c_val: {}, instance: {}".format(self.msg_type, self.c_round, self.c_val,
                                                                  self.instance)


class MessageTwoB(Message):

    def __init__(self, v_round: int, v_val: int, instance: int):
        super().__init__(MessageType.twoB)
        self.v_round: int = v_round
        self.v_val: int = v_val
        self.instance: int = instance

    def __str__(self):
        return "{} - v_round: {}, v_val: {}".format(self.msg_type, self.v_round, self.v_val)


class MessageClient(Message):

    def __init__(self, value: int):
        super().__init__(MessageType.client)
        self.value: int = value
        self.uuid: str = uuid.uuid4().hex

    def __str__(self):
        return "{} - value: {}, random: {}".format(self.msg_type, self.value, self.uuid)


class MessageDecision(Message):

    def __init__(self, value: int, instance: int):
        super().__init__(MessageType.decision)
        self.value = value
        self.instance = instance

    def __str__(self):
        return "{} - value: {}".format(self.msg_type, self.value)


class MessageLeaderElection(Message):

    def __init__(self, id: int):
        super().__init__(MessageType.leader)
        self.id: int = id

    def __str__(self):
        return "{} - proposer id: {}".format(self.msg_type, self.id)
