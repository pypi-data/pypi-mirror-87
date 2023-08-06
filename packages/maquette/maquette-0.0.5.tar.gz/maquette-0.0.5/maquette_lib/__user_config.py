import os

class UserConfiguration:

    __mq_home: str = None

    def __init__(self, mq_home: str):
        self.__mq_home = mq_home

    def url(self) -> str:
        return os.environ.get('MQ_BASE_URL','http://localhost:9042/api/')

    def user(self) -> str:
        return os.environ.get('MQ_USERNAME', 'alice')