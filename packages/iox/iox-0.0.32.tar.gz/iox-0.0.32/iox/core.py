"""
core.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from .google import *

from iox._config import defaults as config

database = None
if 'database' in config and config['database'] == 'bigquery':
    database = BigQuery()


def query(sql):
    if database is None:
        raise AttributeError('database default not set')
    return database.query(sql)
