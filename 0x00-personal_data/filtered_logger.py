#!/usr/bin/env python3
""" 0. Regex-ing to return the log message obfuscated """


import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def filter_datum(
        fields: List[str], redaction: str, message: str,
        separator: str
    ) -> str:
        """ returns the log message obfuscated """
        for field in fields:
            message = re.sub(rf'{field}=[^;]*', f'{field}={redaction}', message)
        return message.replace(';', separator)

    def format(self, record: logging.LogRecord) -> str:
        message = record.getMessage()
        return self.filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
        
