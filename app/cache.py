import time
from typing import Any, Optional
from dataclasses import dataclass, field
from collections import OrderedDict


@dataclass
class CacheEntry:
    value: Any
    expires_at: float
    created_at: float = field(default_factory=time.time)


@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    size: int = 0

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class TTLCache:
    """In-memory cache with TTL and LRU eviction."""

    def __init__(self, default_ttl: int = 3600, max_size: int = 1000):
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._default_ttl = default_ttl
        self._max_size = max_size
        self._stats = CacheStats()

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if entry is None:
            self._stats.misses += 1
            return None
        if time.time() > entry.expires_at:
            del self._cache[key]
            self._stats.misses += 1
            return None
        # Move to end (most recently used)
        self._cache.move_to_end(key)
        self._stats.hits += 1
        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl or self._default_ttl

        # Remove oldest entries if cache is full
        while len(self._cache) >= self._max_size:
            self._cache.popitem(last=False)

        self._cache[key] = CacheEntry(
            value=value,
            expires_at=time.time() + ttl
        )
        self._cache.move_to_end(key)

    def delete(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()
        self._stats = CacheStats()

    def cleanup(self) -> None:
        """Remove expired entries."""
        now = time.time()
        expired = [k for k, v in self._cache.items() if now > v.expires_at]
        for key in expired:
            del self._cache[key]

    def stats(self) -> dict:
        """Return cache statistics."""
        self._stats.size = len(self._cache)
        return {
            "hits": self._stats.hits,
            "misses": self._stats.misses,
            "hit_rate": f"{self._stats.hit_rate:.1%}",
            "size": self._stats.size,
            "max_size": self._max_size,
        }


# Global cache instances
cache = TTLCache(default_ttl=3600, max_size=1000)  # API responses
user_cache = TTLCache(default_ttl=1800, max_size=100)  # User analysis results (30 min)
