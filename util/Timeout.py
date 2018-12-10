from __future__ import annotations

from typing import TYPE_CHECKING, Set, List

from Component import NodeType
from Message import MessageOneA, MessageTwoA
from util.ThreadTimer import ThreadTimer

if TYPE_CHECKING:
    from Proposer import Proposer


class Timeout:

    def __init__(self, node: Proposer):
        self.node = node

        self.timer_phase_one = ThreadTimer(node.PHASE_ONE_TIMEOUT, self.timeout_phase_one_a)
        self.timer_phase_two = ThreadTimer(node.PHASE_TWO_TIMEOUT, self.timeout_phase_two_a)

        self.phase_one_instances: List[int] = list()
        self.phase_two_instances: List[MessageTwoA] = list()

    def timeout_phase_one_a(self):
        if self.node.is_leader():
            for instance_id in sorted(self.phase_one_instances):
                self.node.state[instance_id].phase_one_b_messages = []
                self.node.state[instance_id].c_round = self.node.state[instance_id].c_round + 1

                phase_one_a_msg = MessageOneA(self.node.state[instance_id].c_round, self.node.state[instance_id].instance)
                self.node.send(NodeType.Acceptor, phase_one_a_msg)
                self.node.log.debug('re-sending message phase 1A with new c-round {}'.format(phase_one_a_msg))

    def timeout_phase_two_a(self):
        if self.node.is_leader():
            for message in self.phase_two_instances:
                self.node.log.debug('sending again message 2A - {}'.format(message))
                self.node.send(NodeType.Acceptor, message)

    def stop(self):
        self.timer_phase_one.stop()
        self.timer_phase_two.stop()

    def add_timeout_one_instance(self, instance: int):
        self.phase_one_instances.append(instance)

    def add_timeout_two_instance(self, message: MessageTwoA):
        self.phase_two_instances.append(message)

    def remove_timeout_one_instance(self, instance: int):
        self.phase_one_instances.remove(instance)

    def remove_timeout_two_instance(self, instance: int):
        for msg in self.phase_two_instances:
            if msg.instance == instance:
                self.phase_two_instances.remove(msg)
                break