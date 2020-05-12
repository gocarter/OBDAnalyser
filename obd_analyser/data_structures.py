from datetime import datetime
from typing import List, Tuple
from dataclasses import dataclass, field
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, String, Integer

Base = declarative_base()
@dataclass
class ObdParameters(Base):
    __tablename__ = 'OBD_PARAMETERS'

    UNIT: str
    PID_CODE: str = None
    PID_NAME: str = None

    values: List[Tuple[float, object]] = field(default_factory=list)
    _value_type: type = field(default=type(None), init=False)

    # def __init__(self, pid_name: str, unit: str, value_type: type = float):
    # self.PID_NAME = pid_name
    # self.UNIT = unit
    # self.values = []
    # self._value_type = value_type

    def addValue(self, t_sec: float, value: object):
        if not len(self.values):
            self._value_type = type(value)

        if not isinstance(value, self._value_type):
            raise TypeError("Bad type for value parameter")
        if not [x for x in self.values if x[0] == t_sec]:
            self.values.append((t_sec, value))
        else:
            raise ValueError("Seconds duplicate in values list!")


@dataclass
class ObdValues(Base):
    __tablename__ = 'OBD_VALUES'


@dataclass
class ObdSessions(Base):
    __tablename__ = 'OBD_SESSIONS'
    SESSION_NAME: str
    FILE_NAME: str = None
    VIN: str = None
    OBD_STANDARD: str = None
    COM_STANDARD: str = None
    COMMENT: str = None
    START_TIME: datetime = datetime.min
    # data
    data_markers: List[Tuple[float, object]] = field(default_factory=list)
    parameters: List[ObdRawParameter] = field(default_factory=list)
