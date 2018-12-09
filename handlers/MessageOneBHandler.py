from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from Component import NodeType
from Message import MessageOneB, Message, MessageTwoA, MessageOneA
from ProposerInstance import Phase
from handlers.MessageHandler import MessageHandler

if TYPE_CHECKING:
    from Proposer import Proposer


class MessageOneBHandler(MessageHandler):

    @staticmethod
    def is_valid_handler_for(type: NodeType, message: Message) -> bool:
        return type is NodeType.Proposer and isinstance(message, MessageOneB)

    @staticmethod
    def handle(node: Proposer, message: MessageOneB) -> NoReturn:
        if message.instance not in node.state: pass

        instance = node.state[message.instance]

        instance.add_message_one_b(message)
        if node.is_leader() and instance.is_majority_one_b(instance.c_round):
            # instance.stop_timeout(Phase.one)
            node.timeout_handler.remove_timeout_one_instance(instance.instance)
            k = instance.get_largest_v_round()
            v = instance.get_v_set(k)
            if k is not 0:
                # TODO: proposer catch-up
                new_instance = node.add_instance(instance.to_be_proposed)

                message_one_a = MessageOneA(new_instance.c_round, new_instance.instance)
                node.send(NodeType.Acceptor, message_one_a)

                node.log.debug('catching up - {}'.format(message_one_a))
                node.timeout_handler.add_timeout_one_instance(new_instance.instance)

                instance.to_be_proposed = v.pop().v_val
            phase_two_a_msg = MessageTwoA(instance.c_round, instance.to_be_proposed, instance.instance)
            node.send(NodeType.Acceptor, phase_two_a_msg)
            node.log.debug('multicasting 2A to acceptors - {}'.format(phase_two_a_msg))

            # instance.start_timeout(Phase.two, MessageOneBHandler.timeout_phase_two_a, node, message)
            node.timeout_handler.add_timeout_two_instance(phase_two_a_msg)

            instance.one_b_majority_reached = True

    @staticmethod
    def timeout_phase_two_a(self, message: MessageTwoA):
        self.log.debug('sending again message 2A - {}'.format(message))
        self.send(NodeType.Acceptor, message)
