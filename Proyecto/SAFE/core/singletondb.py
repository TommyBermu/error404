class SingletonDB(type):
    _instances={}
    def __call__(cls,*a,**k):
        if cls not in cls._instances:
            cls._instances[cls]=super().__call__(*a,**k)
        return cls._instances[cls]

class ConexionBD(metaclass=SingletonDB):
    def __init__(self):
        from django.db import connection
        self.connection = connection

    def obtener_cursor(self):
        return self.connection.cursor()
