import argparse
import threading
from typing import NoReturn, Dict

from Component import Component, NodeType
from Message import Message, MessageLeaderElection
from MessageController import MessageController
from ProposerInstance import ProposerInstance
from util.ThreadTimer import ThreadTimer
from util.TimedSet import TimedSet
from util.Timeout import Timeout


class Proposer(Component):
    LEADER_TIMEOUT = 4.0
    PHASE_ONE_TIMEOUT = 3.0
    PHASE_TWO_TIMEOUT = 3.0

    def __init__(self, id: int = None, config_path: str = 'config', ttl=1):
        super().__init__(NodeType.Proposer, id, config_path, ttl)
        # leader election stuff
        self.leader: bool = False
        self.ids: TimedSet = TimedSet()
        # proposer state
        self.processed_proposed: set = set()
        self.state: Dict[int, ProposerInstance] = {}

        self.handler: MessageController = MessageController(self)
        self.timeout_handler: Timeout = Timeout(self)
        # self.heartbeat = ThreadTimer(self.LEADER_TIMEOUT, self.heartbeat_leader)

    def handle_message(self, serialized_msg: bytes) -> NoReturn:
        message = Message.deserialize(serialized_msg)
        self.handler.handle(message)

    def is_leader(self) -> bool:
        return self.leader

    def is_new_propose_message(self, uuid: str) -> bool:
        return uuid not in self.processed_proposed

    def add_instance(self, value: int):
        new_instance_id = self.get_next_instance()
        new_instance = ProposerInstance(value, 1, new_instance_id)
        self.state[new_instance_id] = new_instance
        return new_instance

    def get_next_instance(self):
        return 0 if len(self.state.keys()) == 0 else max(self.state.keys()) + 1

    def heartbeat_leader(self):
        self.send(self.whoiam, MessageLeaderElection(self.id))

    def run(self) -> NoReturn:
        self.log.info('proposer {} is ready to receive'.format(self.id))
        while True:
            value = self.receive()
            self.thread_pool.submit(self.handle_message, value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Paxos Proposer component')

    parser.add_argument('id', action="store", help='Acceptor ID', type=int)
    parser.add_argument('config_path', action="store", help='Path to config file')
    args = parser.parse_args()
    proposer = Proposer(args.id, args.config_path)

    try:
        proposer.run()
    except (KeyboardInterrupt, SystemExit):
        proposer.thread_pool.shutdown(wait=True)
        proposer.heartbeat.stop()
        proposer.timeout_handler.stop()
