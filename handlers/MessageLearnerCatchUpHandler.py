from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from Component import NodeType
from Message import Message, MessageLearnerCatchUp
from handlers.MessageHandler import MessageHandler

if TYPE_CHECKING:
    from Component import Component
    from Learner import Learner


class MessageLearnerCatchUpHandler(MessageHandler):

    @staticmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        return (type is NodeType.Leaner or type is NodeType.Proposer) and isinstance(message, MessageLearnerCatchUp)

    @staticmethod
    def handle(node: Learner, message: MessageLearnerCatchUp) -> NoReturn:
        if node.whoiam is NodeType.Proposer and node.is_leader():
            print(message)
            from_instance = message.from_instance
            to_instance = message.to_instance

            if from_instance == -1 and to_instance == -1:
                values = [node.state[instance].to_be_proposed for instance in node.state.keys()]
            else:
                values = [node.state[instance].to_be_proposed for instance in node.state.keys() if
                          message.from_instance < instance < to_instance]

            # compute the number of batches
            n_of_instances_needed = (from_instance - to_instance) if from_instance < to_instance else len(values)
            n_of_batches = len(values) // message.batch_size
            rest_batches = len(values) % message.batch_size
            total_n_of_batches = n_of_batches + (0 if rest_batches == 0 else 1)

            # send in batch
            for batch_number in range(n_of_batches):
                batch_from = batch_number * message.batch_size
                batch_to = batch_number * message.batch_size + message.batch_size
                message_learners_catch_up = MessageLearnerCatchUp(batch_from, batch_to, message.batch_size,
                                                                  total_n_of_batches, batch_number, values[batch_from:batch_to])
                node.send(NodeType.Leaner, message_learners_catch_up)
            if rest_batches != 0:
                batch_from = n_of_batches * message.batch_size
                batch_to = n_of_batches * message.batch_size + rest_batches
                message_learners_catch_up = MessageLearnerCatchUp(batch_from, batch_to, message.batch_size,
                                                                  total_n_of_batches, total_n_of_batches,
                                                                  values[batch_from:batch_to])
                node.send(NodeType.Leaner, message_learners_catch_up)
            if total_n_of_batches == 0:
                node.send(NodeType.Leaner, MessageLearnerCatchUp(-1, -1, 0, 0, 0, []))
        elif node.whoiam is NodeType.Leaner:
            if message.number_of_batch == 0:
                node.state.is_catching_up = False
            if node.state.is_catching_up is False:
                return
            if message.batch_id not in node.state.catch_up:
                node.state.catch_up_size[message.batch_id] = (message.number_of_batch, 0)
                node.state.catch_up[message.batch_id] = [None] * message.batch_size * message.number_of_batch

            for instance in range(0, message.to_instance - message.from_instance):
                node.state.catch_up[message.batch_id][message.from_instance + instance] = message.values[instance]

            node.state.catch_up_size[message.batch_id] = (node.state.catch_up_size[message.batch_id][0],
                                                          node.state.catch_up_size[message.batch_id][1] + 1)

            if node.state.catch_up_size[message.batch_id][0] == node.state.catch_up_size[message.batch_id][1]:
                values = node.state.catch_up[message.batch_id]
                tmp = list(filter(lambda val: val is not None, values + list(set(node.state.ordered_values) - (set(values)))))
                last_value = tmp.pop()
                node.state.ordered_values = tmp
                node.state.last_ordered_instance = len(tmp) - 1
                for value in node.state.ordered_values:
                    print(value)
                node.state.add_instance(message.to_instance, last_value)
                node.state.is_catching_up = False
