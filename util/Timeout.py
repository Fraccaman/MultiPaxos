from __future__ import annotations

from threading import Thread
import time
from typing import TYPE_CHECKING, List, Dict

from Component import NodeType
from Message import MessageOneA, MessageTwoA, MessageLeaderElection

if TYPE_CHECKING:
    from Proposer import Proposer


class Timeout:
    LEADER_TIMEOUT = 6
    PHASE_ONE_TIMEOUT = 3
    PHASE_TWO_TIMEOUT = 3

    def __init__(self, node: Proposer):
        self.node = node

        self.timer_phase_one = Thread(target=self.timeout_phase_one_a)
        self.timer_phase_two = Thread(target=self.timeout_phase_two_a)
        self.timer_leader_election = Thread(target=self.heartbeat_leader)
        self.timer_phase_one.daemon = True
        self.timer_phase_two.daemon = True
        self.timer_leader_election.daemon = True

        self.phase_one_instances: Dict[int, float] = {}
        self.phase_one_time = time.time()
        self.phase_two_instances: List[MessageTwoA] = list()
        self.phase_two_time = time.time()
        self.leader_election_time = time.time()

        self.timer_phase_one.start()
        self.timer_phase_two.start()
        self.timer_leader_election.start()

    def timeout_phase_one_a(self):
        while True:
            if self.node.is_leader() and self.phase_one_time + self.PHASE_ONE_TIMEOUT < time.time():
                for instance_id in sorted(self.phase_one_instances.keys()):
                    if self.phase_one_instances[instance_id] + self.PHASE_ONE_TIMEOUT < time.time():
                        self.node.state[instance_id].phase_one_b_messages = []
                        self.node.state[instance_id].c_round = self.node.state[instance_id].c_round + 1
                        self.node.state[instance_id].one_b_majority_reached = False

                        phase_one_a_msg = MessageOneA(self.node.state[instance_id].c_round,
                                                      self.node.state[instance_id].instance)
                        self.node.send(NodeType.Acceptor, phase_one_a_msg)
                        self.node.log.debug('re-sending message phase 1A with new c-round {}'.format(phase_one_a_msg))
                        self.phase_one_instances[instance_id] = time.time()
                self.phase_one_time = time.time()
                time.sleep(1)

    def timeout_phase_two_a(self):
        while True:
            if self.node.is_leader() and self.phase_two_time + self.PHASE_TWO_TIMEOUT < time.time():
                for message in self.phase_two_instances:
                    self.node.log.debug('sending again message 2A - {}'.format(message))
                    self.node.state[message.instance].phase_two_b_messages = []
                    self.node.state[message.instance].two_b_majority_reached = False
                    self.node.send(NodeType.Acceptor, message)
                self.phase_two_time = time.time()
                time.sleep(1)

    def heartbeat_leader(self):
        while True:
            if self.leader_election_time + self.LEADER_TIMEOUT < time.time():
                self.node.send(self.node.whoiam, MessageLeaderElection(self.node.id))
                self.leader_election_time = time.time()
            time.sleep(1)

    def add_timeout_one_instance(self, instance: int):
        self.phase_one_instances[instance] = time.time()

    def add_timeout_two_instance(self, message: MessageTwoA):
        self.phase_two_instances.append(message)

    def remove_timeout_one_instance(self, instance: int):
        self.phase_one_instances.pop(instance)

    def remove_timeout_two_instance(self, instance: int):
        for msg in self.phase_two_instances:
            if msg.instance == instance:
                self.phase_two_instances.remove(msg)
                break
