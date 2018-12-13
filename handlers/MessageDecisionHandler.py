from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from ProposerInstance import ProposerInstance
from Component import NodeType
from Message import Message, MessageDecision
from handlers.MessageHandler import MessageHandler

if TYPE_CHECKING:
    from Component import Component


class MessageDecisionHandler(MessageHandler):

    @staticmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        return (type is NodeType.Leaner or type is NodeType.Proposer) and isinstance(message, MessageDecision)

    @staticmethod
    def handle(node: Component, message: MessageDecision) -> NoReturn:
        if node.whoiam is NodeType.Leaner:
            # node.log.info('I have received: {}'.format(message))
            ordered_values = node.state.add_instance(message.instance, message.value)
            # print(ordered_values, l, waiting)
            for value in ordered_values:
                print(value, flush=True)
        elif node.whoiam is NodeType.Proposer and not node.is_leader():
            node.state[message.instance] = ProposerInstance(message.value, 0, message.instance)
            node.log.debug('Added instance {} with value {}'.format(message.instance, message.value))
