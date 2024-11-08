#!/usr/bin/env python3
""" 0. Regex-ing to return the log message obfuscated """


import re
import logging
import os
import mysql.connector
from mysql.connector import Error
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'ip')


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
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db():
    """
    Returns a MySQL database connection object
    using credentials stored as environment variables.
    The function reads the following environment variables:
    - PERSONAL_DATA_DB_USERNAME
    - PERSONAL_DATA_DB_PASSWORD
    - PERSONAL_DATA_DB_HOST
    - PERSONAL_DATA_DB_NAME
    """

    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # If the database name is not set, raise an error
    name_error = "(PERSONAL_DATA_DB_NAME) is required but not set."
    if not db_name:
        raise ValueError(name_error)

    try:
        # Connect to the database using the retrieved credentials
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        # Check if the connection was successful
        if connection.is_connected():
            return connection
        else:
            raise ValueError("Failed to connect to the database.")

    except Error as e:
        print(f"Error: {e}")
        raise
