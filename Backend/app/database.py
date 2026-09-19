import os
from contextlib import contextmanager

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Database Configuration
# --------------------------------------------------

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "sih_database")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


# --------------------------------------------------
# Connection Pool
# --------------------------------------------------

try:
    connection_pool = psycopg2.pool.ThreadedConnectionPool(
        minconn=1,
        maxconn=10,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    print("PostgreSQL connection pool created successfully.")

except psycopg2.Error as error:
    connection_pool = None
    print("Error creating PostgreSQL connection pool:")
    print(error)


# --------------------------------------------------
# Get Database Connection
# --------------------------------------------------

def get_connection():
    """
    Get a connection from the PostgreSQL connection pool.
    """

    if connection_pool is None:
        raise Exception("Database connection pool is not available.")

    connection = connection_pool.getconn()

    return connection


# --------------------------------------------------
# Return Connection to Pool
# --------------------------------------------------

def release_connection(connection):
    """
    Return a connection back to the connection pool.
    """

    if connection_pool is not None and connection is not None:
        connection_pool.putconn(connection)


# --------------------------------------------------
# Database Connection Context Manager
# --------------------------------------------------

@contextmanager
def get_db_connection():
    """
    Provides a database connection and automatically
    returns it to the connection pool.
    """

    connection = None

    try:
        connection = get_connection()

        yield connection

    except Exception:
        if connection is not None:
            connection.rollback()

        raise

    finally:
        if connection is not None:
            release_connection(connection)


# --------------------------------------------------
# Execute SELECT Query
# --------------------------------------------------

def fetch_all(query, parameters=None):
    """
    Execute a SELECT query and return all rows.

    Returns:
        list of dictionaries
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(query, parameters)

        results = cursor.fetchall()

        return results

    except psycopg2.Error:
        if connection is not None:
            connection.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            release_connection(connection)


# --------------------------------------------------
# Execute SELECT Query - Single Row
# --------------------------------------------------

def fetch_one(query, parameters=None):
    """
    Execute a SELECT query and return one row.

    Returns:
        dictionary or None
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(query, parameters)

        result = cursor.fetchone()

        return result

    except psycopg2.Error:
        if connection is not None:
            connection.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            release_connection(connection)


# --------------------------------------------------
# Execute INSERT / UPDATE / DELETE
# --------------------------------------------------

def execute_query(query, parameters=None):
    """
    Execute INSERT, UPDATE or DELETE query.

    The transaction is committed automatically.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(query, parameters)

        connection.commit()

    except psycopg2.Error:
        if connection is not None:
            connection.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            release_connection(connection)


# --------------------------------------------------
# Execute INSERT and Return Inserted Row
# --------------------------------------------------

def execute_returning(query, parameters=None):
    """
    Execute an INSERT/UPDATE query containing
    RETURNING and return the resulting row.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute(query, parameters)

        result = cursor.fetchone()

        connection.commit()

        return result

    except psycopg2.Error:
        if connection is not None:
            connection.rollback()

        raise

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            release_connection(connection)


# --------------------------------------------------
# Test Database Connection
# --------------------------------------------------

def check_database_connection():
    """
    Check whether PostgreSQL is reachable.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute("SELECT 1;")

        result = cursor.fetchone()

        return result[0] == 1

    except psycopg2.Error:
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            release_connection(connection)


# --------------------------------------------------
# Check PostGIS
# --------------------------------------------------

def check_postgis():
    """
    Check whether PostGIS is installed and available.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT PostGIS_Version();"
        )

        version = cursor.fetchone()

        return version[0]

    except psycopg2.Error:
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            release_connection(connection)


# --------------------------------------------------
# Close Connection Pool
# --------------------------------------------------

def close_connection_pool():
    """
    Close all PostgreSQL connections.
    """

    if connection_pool is not None:
        connection_pool.closeall()

        print("PostgreSQL connection pool closed.")