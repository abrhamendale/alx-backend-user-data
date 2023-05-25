#!/usr/bin/env python3
"""Filters log messages."""


from typing import List
import re
import logging
import mysql.connector
import os


PII_FIELDS = ()
"""
return (message)
message = re.sub(i + "=[\d\w\S][^;]*;", i + "=" + redaction + ";", message)
obf = i + "=[\d\w\S][^;]*;"
fld = i + "=" + redaction + ";"
message = re.sub(p, "password="+redaction+";", message)
message = re.sub("password=[\d\w]*;", "password="+redaction+";", message)
"""

def filter_datum_helper(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obsufcator function"""
    for i in fields:
        message = re.sub(i + "=[\d\w\S][^" + separator + "]*" + separator, i + "=" + redaction + ";", message)
    return (message)

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obsufcator function"""
    return (filter_datum_helper(fields, redaction, message, separator))


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    FIELDS = ""

    def __init__(self, fields: List[str]):
        """Initializes new redacting formatter classes."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.FIELDS = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formatter class for logging."""
        record.msg = filter_datum(self.FIELDS, "***", record.getMessage(), self.SEPARATOR).replace(";", "; ").rstrip()
        return (super(RedactingFormatter, self).format(record))

def get_logger() -> logging.Logger:
    """A get logger function."""
    lg = logging.getLogger("user_data")
    lg.propagate = False
    lg.setLevel(logging.INFO)
    handle = logging.StreamHandler()
    handle.setLevel(logging.INFO)
    formatter = RedactingFormatter()
    handle.setFormatter(formatter)
    lg.addHandler(handle)


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connection to a database."""
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', "localhost")
    database = os.environ.get('PERSONAL_DATA_DB_NAME', "")
    #name = os.environ.get('KEY_THAT_MIGHT_EXIST', default_value))
    cnx = mysql.connector.connect(user,
                                  password,
                                  host,
                                  database)
    return (cnx)


def main():
    """Queries a database."""
    cnx = get_db()
    cur = cnx.cursor()
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    for i in rows:
        print(i)

if __name__ == '__main__':
        main()
