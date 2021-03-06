import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

OPEN_CRS_KEY = ''               # Open CRS API Key

GOVTRACK_XML_PATH = ''          #path to govtrack xml root

#TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)