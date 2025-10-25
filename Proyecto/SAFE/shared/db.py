from threading import Lock
from django.db import DEFAULT_DB_ALIAS, transaction, connections
from typing import Any, Type
from django.db.models import Model

class SingletonMeta(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    """
    Fachada Singleton para acceso a la DB en Django
    """
    def __init__(self, alias: str = DEFAULT_DB_ALIAS):
        self._alias = alias

    @property
    def alias(self) -> str:
        return self._alias

    # --- Façade ---
    def manager(self, model: Type[Model]):
        return model._default_manager.using(self._alias)

    def atomic(self):
        return transaction.atomic(using=self._alias)

    def is_usable(self) -> bool:
        try:
            conn = connections[self._alias]
            conn.close_if_unusable_or_obsolete()
            conn.ensure_connection()
            return True
        except Exception:
            return False
