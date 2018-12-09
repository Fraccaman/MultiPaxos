import argparse

from Component import Component, NodeType
from LeanerInstance import LeanerInstance
from Message import Message
from MessageController import MessageController


class Learner(Component):

    def __init__(self, id: int = None, config_path: str = 'config', ttl=1):
        super().__init__(NodeType.Leaner, id, config_path, ttl)
        self.state: LeanerInstance = LeanerInstance()

        self.handler: MessageController = MessageController(self)

    def handle_message(self, serialized_msg: Message):
        message = Message.deserialize(serialized_msg)
        self.handler.handle(message)

    def run(self):
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
    learner.run()
