#!/usr/bin/env python3
""" 0. Regex-ing to return the log message obfuscated """


import re
import logging
from typing import List


PII_FIELDS = (
    'name', 'email', 'phone', 'ssn', 'ip')


def filter_datum(
    fields: List[str],
    redaction: str, message: str, separator: str
) -> str:
    """ Returns the log message obfuscated
    by replacing field values with REDACTION """
    for field in fields:
        pattern = rf'{field}=[^;]*'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message.replace(';', separator)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT =\
        "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initializes the RedactingFormatter class
        with a list of fields to redact """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Formats the log record and applies redaction """
        message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION,
            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ function that takes no arguments and returns a logging.Logger"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    formatter = RedactingFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
