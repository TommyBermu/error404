
# SAFE/core/models.py
from django.db import models
from django.core.cache import cache
from django.db import transaction
import threading

class SingletonModel(models.Model):
    """
    Abstract base class implementing the Singleton pattern
    with thread-safe access and high-performance caching.
    """
    _lock = threading.Lock()
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save the object ensuring singleton behavior and clear the cache.
        """
        with self._lock:
            # Force pk to 1 to ensure singleton behavior
            self.pk = 1
            # Clear the cache when saved
            cache.delete(self.get_cache_key())
            super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Prevent deletion of singleton instances.
        """
        raise NotImplementedError("Cannot delete singleton instances")

    @classmethod
    def get_cache_key(cls):
        """
        Helper method to get a unique cache key for this class.
        """
        return f"singleton_{cls.__name__}"

    @classmethod
    def load(cls):
        """
        Global access point with caching and thread safety.
        """
        cache_key = cls.get_cache_key()
        
        # Try to get from cache first
        obj = cache.get(cache_key)
        
        if obj is None:
            with cls._lock:
                # Double-check pattern: check cache again after acquiring lock
                obj = cache.get(cache_key)
                if obj is None:
                    # If not in cache, get from DB and set cache
                    try:
                        obj = cls.objects.get(pk=1)
                    except cls.DoesNotExist:
                        # Create the singleton instance if it doesn't exist
                        obj = cls(pk=1)
                        obj.save()
                    
                    # Store in cache
                    cache.set(cache_key, obj, timeout=3600)  # Cache for 1 hour

        return obj

    @classmethod
    def get_or_create_singleton(cls, **defaults):
        """
        Get or create singleton instance with default values.
        """
        cache_key = cls.get_cache_key()
        
        # Try to get from cache first
        obj = cache.get(cache_key)
        
        if obj is None:
            with cls._lock:
                # Double-check pattern
                obj = cache.get(cache_key)
                if obj is None:
                    try:
                        obj = cls.objects.get(pk=1)
                    except cls.DoesNotExist:
                        # Create with defaults
                        obj = cls(pk=1, **defaults)
                        obj.save()
                    
                    cache.set(cache_key, obj, timeout=3600)

        return obj
