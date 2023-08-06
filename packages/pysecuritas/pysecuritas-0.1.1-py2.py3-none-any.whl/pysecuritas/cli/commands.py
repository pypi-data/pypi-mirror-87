# -*- coding: utf-8 -*-
"""
    :copyright: © pysecuritas, All Rights Reserved
"""
from pysecuritas.api.alarm import get_available_commands as get_alarm_commands

DALARM_OPS = {
    'IMG': 'Take a picture (requires -s)'
}

DAPI_OPS = {
    'ACT_V2': 'get the activity log',
    'SRV': 'SIM Number and INSTIBS',
    'MYINSTALLATION': 'Sensor IDs and other info'
}

ALARM_OPS = list(DALARM_OPS.keys())
API_OPS = list(DAPI_OPS.keys())


def get_available_commands():
    """
    Returns a dictionary with all available commands and their descriptions

    :return: a dictionary with all available commands
    """

    commands = get_alarm_commands().copy()
    commands.update(DALARM_OPS)
    commands.update(DAPI_OPS)

    return commands
