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
    catchup = "CatchUp - 🧗"


class Message:

    def __init__(self, msg_type: MessageType):
        self.msg_type: MessageType = msg_type

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(message):
        return pickle.loads(message)


    def __str__(self):
        return str(self.__class__) + '\n' + '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


class MessageOneA(Message):

    def __init__(self, c_round: int, instance: int):
        super().__init__(MessageType.oneA)
        self.c_round: int = c_round
        self.instance: int = instance


class MessageOneB(Message):

    def __init__(self, round: int, v_round: int, v_val: int, instance: int):
        super().__init__(MessageType.oneB)
        self.round: int = round
        self.v_round: int = v_round
        self.v_val: int = v_val
        self.instance: int = instance


class MessageTwoA(Message):

    def __init__(self, c_round: int, c_val: int, instance: int):
        super().__init__(MessageType.twoA)
        self.c_round: int = c_round
        self.c_val: int = c_val
        self.instance: int = instance


class MessageTwoB(Message):

    def __init__(self, v_round: int, v_val: int, instance: int):
        super().__init__(MessageType.twoB)
        self.v_round: int = v_round
        self.v_val: int = v_val
        self.instance: int = instance


class MessageClient(Message):

    def __init__(self, value: int):
        super().__init__(MessageType.client)
        self.value: int = value
        self.uuid: str = uuid.uuid4().hex


class MessageDecision(Message):

    def __init__(self, value: int, instance: int):
        super().__init__(MessageType.decision)
        self.value = value
        self.instance = instance


class MessageLeaderElection(Message):

    def __init__(self, id: int):
        super().__init__(MessageType.leader)
        self.id: int = id


class MessageLearnerCatchUp(Message):

    MAX_BUFFER_SIZE = 50

    def __init__(self, from_instance: int, to_instance: int, batch_size: int=0, number_of_batch: int=0, batch_number: int=0, values=[], batch_id=uuid.uuid4()):
        super().__init__(MessageType.catchup)
        self.batch_size: int = self.MAX_BUFFER_SIZE if batch_size == 0 else batch_size
        self.from_instance = from_instance
        self.to_instance = to_instance
        self.number_of_batch = number_of_batch
        self.batch_number = batch_number
        self.values = values
        self.batch_id = batch_id
