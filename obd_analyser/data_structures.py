from datetime import datetime
from typing import List, Tuple


class ObdRawParameter:
    _value_type: type
    PID_CODE: str
    PID_NAME: str
    UNIT: str
    values: List[Tuple[float, object]]

    def __init__(self, pid_name: str, unit: str, value_type: type = float):
        self.PID_NAME = pid_name
        self.UNIT = unit
        self.values = []
        self._value_type = value_type

    def addValue(self, t_sec: float, value: object):
        if not isinstance(value, self._value_type):
            raise TypeError("Bad type for value parameter")
        if not [x for x in self.values if x[0] == t_sec]:
            self.values.append((t_sec, value))
        else:
            raise ValueError("Seconds duplicate in values list!")


class ObdRawSession:
    SESSION_NAME: str
    FILE_NAME: str
    START_TIME: datetime = datetime.min
    VIN: str
    OBD_STANDARD: str
    COM_STANDARD: str
    COMMENT: str
    # data
    data_markers: List[Tuple[float, object]]
    parameters: List[ObdRawParameter]

    def __init__(self):
        self.data_markers = []
        self.parameters = []
