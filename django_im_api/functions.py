import socket

import redis
import requests
from django.core.cache import cache
from django.db import connection


def check_mysql_connection():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"MySQL connection failed: {e}")
        return False


def check_redis_connection():
    try:
        cache.set("test_key", "test_value", timeout=1)
        value = cache.get("test_key")
        if value == "test_value":
            return True
        else:
            return False
    except (redis.ConnectionError, socket.timeout) as e:
        print(f"Redis connection failed: {e}")
        return False


def check_openfood_connection():
    try:
        requests.get("https://world.openfoodfacts.org/api/v0/")
        return True
    except requests.exceptions.ConnectionError:
        return False
