#!/usr/bin/env python3
"""Filters log messages."""


from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obsufcator function"""
    for i in fields:
        message = re.sub(i + "=[\d\w\S][^" + separator + "]*" + separator, i + "=" + redaction + ";", message)
    return (message)
"""
return (message)
message = re.sub(i + "=[\d\w\S][^;]*;", i + "=" + redaction + ";", message)
obf = i + "=[\d\w\S][^;]*;"
fld = i + "=" + redaction + ";"
message = re.sub(p, "password="+redaction+";", message)
#message = re.sub("password=[\d\w]*;", "password="+redaction+";", message)
"""

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    FIELDS = ""

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.FIELDS = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formatter class for logging."""
        record.msg = filter_datum(self.FIELDS, "***", record.getMessage(), self.SEPARATOR)
        return (super(RedactingFormatter, self).format(record))
        
