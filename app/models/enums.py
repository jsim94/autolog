# app > models > enums.py

from enum import Enum
from telnetlib import FORWARD_X


class FormEnum():
    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, choice):
        return cls(int(choice)) if not isinstance(choice, cls) else choice

    def __str__(self):
        return str(self.value)


class PrivacyStatus(FormEnum, Enum):
    '''Choices for friendship status'''
    PUBLIC = 1
    PRIVATE = 2
    UNLISTED = 3


class Drivetrain(FormEnum, Enum):
    '''Choices for drivetrain'''
    FWD = 1
    RWD = 2
    AWD = 3
