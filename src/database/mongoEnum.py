from enum import Enum


class MongoErr(Enum):
    SUCCESS = 0
    EXISTS = -1
    EMPTY = -2
