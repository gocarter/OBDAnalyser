#!/usr/bin/env python3

import os
from pathlib import Path
from csv import reader
from datetime import datetime
from obd_analyser.data_structures import *


def import_raw_car_scanner_csv(file: Path) -> ObdRawSession:
    with open(file) as raw_file:
        first = True
        response = ObdRawSession()
        for row in reader(raw_file, delimiter=";", quotechar='"', strict=True):
            if first:
                first = False
                if row[0] != 'SECONDS' or row[1] != 'PID' or row[2] != 'VALUE' or row[3] != 'UNITS':
                    raise ValueError(
                        'Trying to read file failed because of wrong header.')
                response.SESSION_NAME = response.FILE_NAME = os.path.basename(
                    file.absolute())
                response.SESSION_NAME = response.SESSION_NAME.split('.')[0]
                try:
                    response.START_TIME = datetime(*[int(x) for x in response.SESSION_NAME.split(' ')[0].split('-')],
                                                   *[int(x) for x in response.SESSION_NAME.split(' ')[1].split('-')])
                except Exception as ex:
                    try:
                        response.START_TIME = datetime.fromtimestamp(
                            os.path.getctime(file))
                    except:
                        pass
            else:
                second, pid_name, value, units = [
                    float(row[0]), str(row[1]), str(row[2]), str(row[3])]
                try:
                    value = float(value)
                except Exception:
                    pass
                if not [parameter for parameter in response.parameters if pid_name == parameter.PID_NAME]:
                    param = ObdRawParameter(pid_name, units, type(value))
                    response.parameters.append(param)
                [parameter] = [
                    param for param in response.parameters if pid_name == param.PID_NAME]
                parameter.addValue(second, value)

        return response
