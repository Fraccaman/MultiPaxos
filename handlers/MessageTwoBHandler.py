from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from Component import NodeType
from Message import Message, MessageTwoB, MessageDecision
from ProposerInstance import Phase
from handlers.MessageHandler import MessageHandler

if TYPE_CHECKING: from Proposer import Proposer


class MessageTwoBHandler(MessageHandler):

    @staticmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        return type is NodeType.Proposer and isinstance(message, MessageTwoB)

    @staticmethod
    def handle(node: Proposer, message: MessageTwoB) -> NoReturn:
        instance = node.state[message.instance]
        instance.add_message_two_b(message)

        if instance.is_majority_two_b():
            node.log.warning('received message 2B from acceptors - {}'.format(message))
            # instance.stop_timeout(Phase.two)
            node.timeout_handler.remove_timeout_two_instance(instance.instance)

            decision_msg = MessageDecision(message.v_val, message.instance)
            node.send(NodeType.Leaner, decision_msg)
            node.send(NodeType.Proposer, decision_msg)

            node.state[message.instance].phase_two_a_timeout.stop()
