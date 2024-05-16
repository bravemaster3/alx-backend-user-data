#!/usr/bin/env python3
"""
Module for loging logs...
"""
import mysql.connector
import os
import logging
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """Obfuscates specified fields in the log msg using regex substitution."""
    for field in fields:
        message = re.sub(f"{field}=[^;]*", f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format function definition"""
        message = super().format(record)
        m = filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
        return m


# Define the PII fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


def get_db() -> 'mysql.connector.connection.MySQLConnection':
    """Returns a connector to the database."""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    config = {
        'user': username,
        'password': password,
        'host': host,
        'database': db_name,
    }

    return mysql.connector.connect(**config)


def main():
    """Main function that retrieves and logs all rows in the users table."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        message = "; ".join(
            [f"{field}={value}" for field, value in zip(PII_FIELDS, row)])
        logger.info(message)


if __name__ == "__main__":
    main()
