import Message
from Component import Component
from handlers.MessageLearnerCatchUpHandler import MessageLearnerCatchUpHandler
from handlers.MessageClientHandler import MessageClientHandler
from handlers.MessageDecisionHandler import MessageDecisionHandler
from handlers.MessageLeaderElectionHandler import MessageLeaderElectionHandler
from handlers.MessageOneAHandler import MessageOneAHandler
from handlers.MessageOneBHandler import MessageOneBHandler
from handlers.MessageTwoAHandler import MessageTwoAHandler
from handlers.MessageTwoBHandler import MessageTwoBHandler


class MessageController:

    def __init__(self, type: Component):
        self.node = type
        self.handlers = [
            MessageOneAHandler,
            MessageOneBHandler,
            MessageTwoAHandler,
            MessageTwoBHandler,
            MessageClientHandler,
            MessageDecisionHandler,
            MessageLeaderElectionHandler,
            MessageLearnerCatchUpHandler
        ]

    def handle(self, message: Message):
        for handler in self.handlers:
            if handler.is_valid_handler_for(self.node.whoiam, message):
                handler.handle(self.node, message)
                break
