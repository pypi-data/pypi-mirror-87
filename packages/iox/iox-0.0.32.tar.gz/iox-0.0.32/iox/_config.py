
from configparser import RawConfigParser
import os.path
import sys

this = sys.modules[__name__]
this.defaults = {}
this.google = {}

home = os.path.expanduser('~')

# If ~/.ioxrc exists, read it
config_file = os.path.join(home, '.ioxrc')
if os.path.exists(config_file):
    # Parse the configuration file
    parser = RawConfigParser()
    parser.read(config_file)

    # Defaults
    database = parser.get('defaults', 'database', fallback=None)
    this.defaults['database'] = database if database is None else database.lower()

    # Google
    this.google['credentials'] = parser.get('google', 'credentials', fallback='credentials.json')
    this.google['project_id'] = parser.get('google', 'project_id', fallback=None)
