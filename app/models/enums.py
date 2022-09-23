# app > models > enums.py

from enum import Enum
from telnetlib import FORWARD_X


class FormEnum():
    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    def __str__(self):
        return str(self.value)


class PrivacyStatus(FormEnum, Enum):
    '''Choices for friendship status'''
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'
    UNLISTED = 'UNLISTED'


class Drivetrain(FormEnum, Enum):
    '''Choices for drivetrain'''
    FWD = 'FWD'
    RWD = 'RWD'
    AWD = 'AWD'
