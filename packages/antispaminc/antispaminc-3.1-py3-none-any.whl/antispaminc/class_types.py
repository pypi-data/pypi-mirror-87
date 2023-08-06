# Copyright (C) 2020 AntiSpam, Inc. <http://antispaminc.tk/>
#
#                    GNU GENERAL PUBLIC LICENSE
#                      Version 3, 29 June 2007

# Copyright (C) 2020 AntiSpam, Inc. <http://antispaminc.tk/>
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.

from enum import Enum, auto
from typing import Optional

class ClassTypes:
    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {self.__dict__}>'

    def __repr__(self) -> str:
        return self.__str__()

class Antispamclass(ClassTypes):
    token: str
    userid: int
    reason: str
    def __init__(self, reason: str, token: str, userid: int, **kwargs) -> None:
        self.token = token
        self.userid = userid
        self.reason = reason
