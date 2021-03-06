import argparse
from time import sleep
from typing import List

from Component import Component, NodeType
from Message import MessageClient


class Client(Component):

    def __init__(self, values: List[int], id: int = None, config_path: str = 'config', ttl=1):
        super().__init__(NodeType.Client, id, config_path, ttl)
        self.values: List[int] = values

    def propose_value(self, msg: MessageClient):
        self.log.debug('Client {} is proposing value: {}'.format(self.id, msg.value))
        self.send(NodeType.Proposer, msg)

    def run(self):
        for value in self.values:
            self.propose_value(MessageClient(value))
            sleep(0.005)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Paxos Proposer component')

    parser.add_argument('id', action="store", help='Acceptor ID', type=int)
    parser.add_argument('config_path', action="store", help='Path to config file')
    parser.add_argument('values', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')

    args = parser.parse_args()
    values = [i for i in range(0, 2222)]

    client = Client(values, args.id, args.config_path)
    try:
        client.run()
    except Exception as e:
        print(e)

