import argparse
from typing import NoReturn

from Component import Component, NodeType
from LearnerInstance import LearnerInstance
from Message import Message, MessageLearnerCatchUp
from MessageController import MessageController


class Learner(Component):

    def __init__(self, id: int = None, config_path: str = 'config', ttl=1):
        super().__init__(NodeType.Leaner, id, config_path, ttl)
        self.state: LearnerInstance = LearnerInstance()

        self.handler: MessageController = MessageController(self)
        self.send_catch_up_message()

    def handle_message(self, serialized_msg: Message) -> NoReturn:
        message = Message.deserialize(serialized_msg)
        self.handler.handle(message)

    def send_catch_up_message(self) -> NoReturn:
        if self.state.last_ordered_instance == -1:
            self.send(NodeType.Proposer, MessageLearnerCatchUp(self.state.last_ordered_instance, -1))

    def run(self) -> NoReturn:
        self.log.debug('Leaner {} is ready to receive'.format(self.id))
        while True:
            value = self.receive()
            self.thread_pool.submit(self.handle_message, value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Paxos Learner component')

    parser.add_argument('id', action="store", help='Acceptor ID', type=int)
    parser.add_argument('config_path', action="store", help='Path to config file')
    args = parser.parse_args()

    learner = Learner(args.id, args.config_path)

    try:
        learner.run()
    except (KeyboardInterrupt, SystemExit):
        learner.thread_pool.shutdown()
