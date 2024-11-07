#!/usr/bin/env python3
""" 0. Regex-ing """


import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str,
    separator: str) -> str:
    """ returns the log message obfuscated """
    for field in fields:
        message = re.sub(rf'{field}=[^;]*', f'{field}={redaction}', message)
    return message.replace(';', separator)
