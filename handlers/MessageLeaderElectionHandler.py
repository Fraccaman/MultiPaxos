from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from Component import NodeType
from Message import Message, MessageLeaderElection
from handlers.MessageHandler import MessageHandler

if TYPE_CHECKING:
    from Proposer import Proposer


class MessageLeaderElectionHandler(MessageHandler):

    @staticmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        return type is NodeType.Proposer and isinstance(message, MessageLeaderElection)

    @staticmethod
    def handle(node: Proposer, message: MessageLeaderElection) -> NoReturn:
        node.ids.add(message.id, timeout=node.timeout_handler.LEADER_TIMEOUT + 1)
        leader_id = max(node.ids)

        if leader_id is node.id:
            node.log.debug('i am leader!')
            node.leader = True
        else:
            node.leader = False
