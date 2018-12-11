from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from Component import NodeType
from Message import Message, MessageLearnerCatchUp
from handlers.MessageHandler import MessageHandler

if TYPE_CHECKING:
    from Component import Component


class MessageLearnerCatchUpHandler(MessageHandler):

    @staticmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        return (type is NodeType.Leaner or type is NodeType.Proposer) and isinstance(message, MessageLearnerCatchUp)

    @staticmethod
    def handle(node: Component, message: MessageLearnerCatchUp) -> NoReturn:
        if node.whoiam is NodeType.Proposer and node.is_leader():
            last_seen_instance = node.get_current_instance() - 1
            values = [node.state[instance].to_be_proposed for instance in node.state.keys() if instance > message.last_seen]

            message_learner_catch_up = MessageLearnerCatchUp(last_seen_instance, values)
            node.send(NodeType.Leaner, message_learner_catch_up)
        elif node.whoiam is NodeType.Leaner:
            node.log.debug("Learner is catching up ....")
            node.state.ordered_values = message.values + list(set(node.state.ordered_values) - (set(message.values)))

            for instance in node.state.waiting_instances.keys():
                if instance < message.last_seen:
                    node.state.waiting_instances.pop(instance)

            node.state.last_ordered_instance = message.last_seen
            for value in node.state.ordered_values: print(value)
            node.log.debug("Learner catch up done")
