from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from Component import NodeType
from Message import Message, MessageTwoA, MessageTwoB
from handlers.MessageHandler import MessageHandler

if TYPE_CHECKING:
    from Acceptor import Acceptor


class MessageTwoAHandler(MessageHandler):

    @staticmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        return type is NodeType.Acceptor and isinstance(message, MessageTwoA)

    @staticmethod
    def handle(node: Acceptor, message: MessageTwoA) -> NoReturn:
        instance = node.state[message.instance]
        node.log.debug('{} - {}'.format(message.c_round, instance.round))
        if message.c_round >= instance.round:
            instance.v_round = message.c_round
            instance.v_val = message.c_val
            phase_two_b_msg = MessageTwoB(instance.v_round, instance.v_val, instance.instance)
            node.log.debug('multicasting 2B to proposers - {}'.format(phase_two_b_msg))
            node.send(NodeType.Proposer, phase_two_b_msg)
        instance = node.state[message.instance]
