import os
import socket
import struct
from concurrent.futures.thread import ThreadPoolExecutor
from enum import Enum
from typing import NoReturn

from Message import Message
from util.Config import Config
from util.Logger import MyLogger


class NodeType(Enum):
    Proposer = "proposers"
    Leader = "leaders"
    Acceptor = "acceptors"
    Leaner = "learners"
    Client = "clients"


class Component:
    BUFFER_SIZE = 4096

    def __init__(self, whoiam: NodeType, id: int = None, file_path: str = 'config', n_of_workers=4, ttl: int = 1):
        self.whoiam: NodeType = whoiam
        self.config: Config = Config(file_path)
        self.mc_group: str = self.get_group()
        self.mc_port: int = self.get_port()
        self.recv_sock: socket = self.__init_recv_socket(self.mc_group, self.mc_port)
        self.ttl: int = ttl  # default 1 if localhost
        self.thread_pool: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self.log: MyLogger = MyLogger.__call__().get_logger()
        self.id: int = id if id > 0 else os.getpid()

    def receive(self) -> bytes:
        return self.recv_sock.recv(self.BUFFER_SIZE)

    def send(self, to: NodeType, message: Message) -> NoReturn:
        self.__send(self.get_component_group(to), self.get_component_port(to), message.serialize())

    def get_group(self) -> str:
        return self.get_component_group(self.whoiam)

    def get_port(self) -> int:
        return self.get_component_port(self.whoiam)

    def get_component_port(self, component: NodeType) -> int:
        return self.config.get(component).get_port()

    def get_component_group(self, component: NodeType) -> str:
        return self.config.get(component).get_group()

    @staticmethod
    def handle_message(serialized_msg):
        raise Exception("Not Implemented!")

    def __send(self, mc_group: str, mc_port: int, msg: bytes) -> NoReturn:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.ttl)
        sock.sendto(msg, (mc_group, mc_port))

    @staticmethod
    def __init_recv_socket(mc_group: str, mc_port: int) -> socket:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        recv_socket.bind((mc_group, mc_port))
        mreq = struct.pack("4sl", socket.inet_aton(mc_group), socket.INADDR_ANY)
        recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        return recv_socket
