import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

logger = logging.getLogger(__name__)

def get_sqlite_memory_uri() -> str:
    """Get the SQLite in-memory URI."""
    return "sqlite:///:memory:"

def get_sqlite_file_url() -> str:
    """
    Get the fully-qualified path to the SQLite database file.
    The database file is located in the same directory as this script.
    """
    return f"sqlite:///{os.path.join(basedir, 'social_services.db')}"

def get_postgres_uri() -> str:
    """
    Get the PostgreSQL connection URI.
    The values for host, port, password, user, and db_name can be configured using environment variables.
    """
    host = os.environ.get("DB_HOST", "localhost")
    port = 54321 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = "socialservicenewtable", "socialservicenewtable"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

def get_api_url() -> str:
    """
    Get the URL of the API.
    The host and port can be configured using environment variables.
    """
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"

def get_redis_host_and_port() -> dict:
    """
    Get the Redis host and port.
    The host and port can be configured using environment variables.
    """
    host = os.environ.get("REDIS_HOST", "localhost")
    port = 63791 if host == "localhost" else 6379
    return {"host": host, "port": port}

def get_email_host_and_port() -> dict:
    """
    Get the email host and port for sending notifications.
    The host, port, and http_port can be configured using environment variables.
    """
    host = os.environ.get("EMAIL_HOST", "localhost")
    port = 11025 if host == "localhost" else 1025
    http_port = 18025 if host == "localhost" else 8025
    return {"host": host, "port": port, "http_port": http_port}
