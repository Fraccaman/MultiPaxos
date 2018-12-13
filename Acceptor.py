import argparse
from typing import Dict, Tuple, Any, NoReturn

from AcceptorInstance import AcceptorInstance
from Component import Component, NodeType
from Message import Message
from MessageController import MessageController


class Acceptor(Component):

    def __init__(self, id: int, config_path: str = 'config', ttl=1):
        super().__init__(NodeType.Acceptor, id, config_path, 8, ttl)
        self.state: Dict[int, AcceptorInstance] = {}

        self.handler: MessageController = MessageController(self)

    def handle_message(self, serialized_msg: Message) -> NoReturn:
        message = Message.deserialize(serialized_msg)
        self.handler.handle(message)

    def add_instance(self, c_round: int, instance_id: int):
        if instance_id not in self.state:
            self.state[instance_id] = AcceptorInstance(instance_id)

    def update_instance(self, c_round: int, instance_id: int):
        if instance_id in self.state and c_round > self.state[instance_id].round:
            self.state[instance_id].round = c_round

    def get_instance(self, instance: int) -> Tuple[Any, Any, Any, Any]:
        instance = self.state[instance]
        return instance.round, instance.v_round, instance.v_val, instance.instance

    def run(self):
        self.log.debug('acceptor {} is ready to receive'.format(self.id))
        while True:
            value = self.receive()
            self.thread_pool.submit(self.handle_message, value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Paxos Acceptor component')

    parser.add_argument('id', action="store", help='Acceptor ID', type=int)
    parser.add_argument('config_path', action="store", help='Path to config file')
    args = parser.parse_args()

    acceptor = Acceptor(args.id, args.config_path)

    try:
        acceptor.run()
    except (KeyboardInterrupt, SystemExit):
        acceptor.thread_pool.shutdown()
