from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from Component import NodeType
from Message import MessageOneA, Message, MessageOneB
from handlers.MessageHandler import MessageHandler

if TYPE_CHECKING:
    from Acceptor import Acceptor


class MessageOneAHandler(MessageHandler):

    @staticmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        return type is NodeType.Acceptor and isinstance(message, MessageOneA)

    @staticmethod
    def handle(node: Acceptor, message: MessageOneA) -> NoReturn:
        node.add_instance(message.c_round, message.instance)

        if message.c_round > node.state[message.instance].round:
            node.update_instance(message.c_round, message.instance)

            round, v_round, v_val, instance = node.get_instance(message.instance)

            message_one_b = MessageOneB(round, v_round, v_val, instance)
            node.send(NodeType.Proposer, message_one_b)

            node.log.debug('multicast message 1B to proposers - {}'.format(message_one_b))
