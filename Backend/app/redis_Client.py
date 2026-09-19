import os
import json

import redis
from redis.exceptions import RedisError
from dotenv import load_dotenv


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Redis Configuration
# --------------------------------------------------

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)


# --------------------------------------------------
# Redis Connection Pool
# --------------------------------------------------

redis_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True,
    max_connections=20
)


# --------------------------------------------------
# Redis Client
# --------------------------------------------------

redis_client = redis.Redis(
    connection_pool=redis_pool
)


# --------------------------------------------------
# Test Redis Connection
# --------------------------------------------------

def check_redis_connection():
    """
    Check whether Redis is reachable.

    Returns:
        True  -> Redis is available
        False -> Redis is unavailable
    """

    try:
        return redis_client.ping()

    except RedisError:
        return False


# --------------------------------------------------
# Set String Value
# --------------------------------------------------

def set_value(key, value, expiration=None):
    """
    Store a value in Redis.

    Args:
        key: Redis key
        value: Value to store
        expiration: Expiration time in seconds

    Example:
        set_value("test_key", "hello", 60)
    """

    try:
        redis_client.set(
            key,
            value,
            ex=expiration
        )

        return True

    except RedisError:
        return False


# --------------------------------------------------
# Get String Value
# --------------------------------------------------

def get_value(key):
    """
    Get a value from Redis.

    Returns:
        Value if found
        None if key does not exist or Redis fails
    """

    try:
        return redis_client.get(key)

    except RedisError:
        return None


# --------------------------------------------------
# Delete Value
# --------------------------------------------------

def delete_value(key):
    """
    Delete a Redis key.
    """

    try:
        redis_client.delete(key)

        return True

    except RedisError:
        return False


# --------------------------------------------------
# Check Whether Key Exists
# --------------------------------------------------

def key_exists(key):
    """
    Check whether a Redis key exists.
    """

    try:
        return redis_client.exists(key) == 1

    except RedisError:
        return False


# --------------------------------------------------
# Set JSON Data
# --------------------------------------------------

def set_json(key, data, expiration=None):
    """
    Store Python dictionary/list as JSON in Redis.

    Example:

        set_json(
            "route:123",
            {
                "distance": 12.5,
                "traffic_probability": 0.42
            },
            300
        )
    """

    try:
        json_data = json.dumps(data)

        redis_client.set(
            key,
            json_data,
            ex=expiration
        )

        return True

    except (RedisError, TypeError, ValueError):
        return False


# --------------------------------------------------
# Get JSON Data
# --------------------------------------------------

def get_json(key):
    """
    Retrieve JSON data from Redis.

    Returns:
        Python dictionary/list if found
        None otherwise
    """

    try:
        data = redis_client.get(key)

        if data is None:
            return None

        return json.loads(data)

    except (RedisError, TypeError, ValueError):
        return None


# --------------------------------------------------
# Set Expiration
# --------------------------------------------------

def set_expiration(key, expiration):
    """
    Set expiration time for an existing key.

    expiration:
        Time in seconds
    """

    try:
        return redis_client.expire(
            key,
            expiration
        )

    except RedisError:
        return False


# --------------------------------------------------
# Get Remaining TTL
# --------------------------------------------------

def get_ttl(key):
    """
    Get remaining lifetime of a Redis key.

    Returns:
        TTL in seconds
    """

    try:
        return redis_client.ttl(key)

    except RedisError:
        return -1


# --------------------------------------------------
# Clear Specific Key
# --------------------------------------------------

def clear_cache(key):
    """
    Delete a specific cached value.
    """

    return delete_value(key)


# --------------------------------------------------
# Clear All Redis Data
# --------------------------------------------------

def clear_all_cache():
    """
    Delete all keys from the currently configured
    Redis database.

    WARNING:
        Do not use this in normal API requests.
    """

    try:
        redis_client.flushdb()

        return True

    except RedisError:
        return False


# --------------------------------------------------
# Close Redis Connection Pool
# --------------------------------------------------

def close_redis_connection():
    """
    Close the Redis connection pool.
    """

    try:
        redis_client.close()

    except RedisError:
        pass