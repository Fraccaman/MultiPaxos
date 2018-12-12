import datetime
import logging


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MyLogger(object, metaclass=SingletonType):
    # __metaclass__ = SingletonType   # python 2 Style
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("crumbs")
        self._logger.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')

        now = datetime.datetime.now()

        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(streamHandler)

    def get_logger(self):
        return self._logger


if __name__ == "__main__":
    logger = MyLogger.__call__().get_logger()
    logger.info("Hello, Logger")
    logger.debug("bug occured")
