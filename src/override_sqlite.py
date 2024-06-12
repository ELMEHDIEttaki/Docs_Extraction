import pysqlite3
import sys

# Override the default sqlite3 library
sys.modules['sqlite3'] = pysqlite3
