from django.db import connection

class DatabaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
        return cls._instance

    def query(self, sql, params=None):
        with connection.cursor() as cursor:
            cursor.execute(sql, params or [])
            return cursor.fetchall()