import os

# SqlServer Config
SQLSERVER_HOST = os.getenv("SQLSERVER_HOST", "127.0.0.1")
SQLSERVER_USER = os.getenv("SQLSERVER_USER", "root")
SQLSERVER_PW = os.getenv("SQLSERVER_PW", "123456")
SQLSERVER_DB = os.getenv("SQLSERVER_DB", "db")
SQLSERVER_PORT = int(os.getenv("SQLSERVER_PORT", 1433))

# MySQL Config
MYSQL_HOST = os.getenv("MYSQL_HOST", "10.88.188.229")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 13306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "nirvana")
MYSQL_DB = os.getenv("MYSQL_DB", "nirvana")
MYSQL_CHARSET = os.getenv("MYSQL_CHARSET", "utf8")

# Callback
CALLBACK_PROTOCOL = os.getenv("CALLBACK_PROTOCOL", "http")
CALLBACK_HOST = os.getenv("CALLBACK_HOST", "10.88.188.229")
CALLBACK_PORT = int(os.getenv("CALLBACK_PORT", 13306))
