from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING, List

from Component import NodeType
from Message import MessageOneA, MessageTwoA

if TYPE_CHECKING:
    from Proposer import Proposer


class Timeout:

    def __init__(self, node: Proposer):
        self.node = node

        self.timer_phase_one = threading.Thread(target=self.timeout_phase_one_a)
        self.timer_phase_two = threading.Thread(target=self.timeout_phase_two_a)
        self.timer_phase_one.setDaemon(True)
        self.timer_phase_two.setDaemon(True)

        self.phase_one_instances: List[int] = list()
        self.phase_one_time = time.time()
        self.phase_two_instances: List[MessageTwoA] = list()
        self.phase_two_time = time.time()

        self.timer_phase_one.start()
        self.timer_phase_two.start()

    def timeout_phase_one_a(self):
        while True:
            if self.node.is_leader() and self.phase_one_time + 5 < time.time():
                for instance_id in self.phase_one_instances:
                    self.node.state[instance_id].phase_one_b_messages = []
                    self.node.state[instance_id].c_round = self.node.state[instance_id].c_round + 1

                    phase_one_a_msg = MessageOneA(self.node.state[instance_id].c_round, self.node.state[instance_id].instance)
                    self.node.send(NodeType.Acceptor, phase_one_a_msg)
                    self.node.log.debug('re-sending message phase 1A with new c-round {}'.format(phase_one_a_msg))
                self.phase_one_time = time.time()
                time.sleep(1)

    def timeout_phase_two_a(self):
        while True:
            if self.node.is_leader() and self.phase_two_time + 5 < time.time():
                for message in self.phase_two_instances:
                    self.node.log.debug('sending again message 2A - {}'.format(message))
                    self.node.send(NodeType.Acceptor, message)
                self.phase_two_time = time.time()
                time.sleep(1)

    def stop(self):
        self.timer_phase_one.join()
        self.timer_phase_two.join()

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
