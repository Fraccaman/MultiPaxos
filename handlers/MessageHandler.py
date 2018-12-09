from abc import abstractmethod, ABC

import Message
from Component import NodeType, Component


class MessageHandler(ABC):

    @staticmethod
    @abstractmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        raise Exception("Not Implemented!")

    @staticmethod
    @abstractmethod
    def handle(node: Component, message: Message) -> None:
        raise Exception("Not Implemented!")
