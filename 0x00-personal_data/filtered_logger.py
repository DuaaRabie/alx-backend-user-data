#!/usr/bin/env python3
""" 0. Regex-ing """


import re
from typing import List


def filter_datum(fields, redaction, message, separator):
    """ returns the log message obfuscated """
    message = message.replace(';', separator)
    for field in fields:
        message = re.sub(rf'{field}=[^;]*', f'{field}={redaction}', message)
    return message
