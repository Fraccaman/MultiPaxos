from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from Component import NodeType
from Message import Message, MessageClient, MessageOneA
from handlers.MessageHandler import MessageHandler

if TYPE_CHECKING:
    from Proposer import Proposer


class MessageClientHandler(MessageHandler):

    @staticmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        return type is NodeType.Proposer and isinstance(message, MessageClient)

    @staticmethod
    def handle(node: Proposer, message: MessageClient) -> NoReturn:
        if node.is_leader() and node.is_new_propose_message(message.uuid):
            node.processed_proposed.add(message.uuid)
            new_instance = node.add_instance(message.value)

            message_one_a = MessageOneA(new_instance.c_round, new_instance.instance)
            node.send(NodeType.Acceptor, message_one_a)

            node.log.debug('multi-casting 1A to acceptors - {}'.format(message_one_a))
            node.timeout_handler.add_timeout_one_instance(new_instance.instance)
