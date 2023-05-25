#!/usr/bin/env python3
"""Filters log messages."""


from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> List[str]:
    message = re.sub("password=[\d\w]*;", "password="+redaction+";", message)
    message = re.sub("date_of_birth=[0-9]{2}\/[0-9]{2}\/[0-9]{4};", "date_of_birth="+redaction+";", message)
    return (message)
