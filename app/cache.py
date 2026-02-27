from cachetools import TTLCache
import time
from typing import Any , Optional


class SearchCache:

    def __init__(self, maxsize: int = 200, ttl: int = 60):
        self.cache = TTLCache(maxsize=maxsize , ttl=ttl)
        self.hints = 0 
        self.misses = 0
        self.total_requests = 0

    def _make_key(self, q:str, limit:int ) -> str:
        """Create a unique cache key from query parameters"""
        return f"search:{q.lower()}:{limit}"

    def get(self , q: str, limit: int) -> Optional[Any]:
        """Get cached result if exists and not expired"""
        key = self._make_key(q , limit)
        self.total_requests += 1

        if key in self.cache:
            self.hints += 1
            return self.cache[key]
        else:
            self.misses += 1
            return None
    
    def set(self , q: str, limit:int , value: Any) -> None:
        """Store result in cache"""
        key = self._make_key(q , limit)
        self.cache[key] = value
    
    def get_stats(self) -> dict:
        """Return cache statistics"""
        hit_ratio = 0
        if self.total_requests > 0:
            hit_ratio = (self.hints / self.total_requests) * 100
            return{
                "hints" : self.hints,
                "misses" : self.misses,
                "total_requests" : self.total_requests ,
                "hit_ratio_percent" : round(hit_ratio , 2),
                "current_cache_size" : len(self.cache) ,
                "max_cache_size" : self.cache.maxsize
            }
    
    def reset_states(self) -> None:
        """Reset statistics counters"""
        self.hints = 0 
        self.misses = 0
        self.total_requests = 0
    
    def clear(self) -> None:
        """Clear all cached items"""
        self.cache.clear()
        self.reset_states()

    def invalidate(self , q: str, limit: int) -> None:
        """Remove specific item from cache"""
        key = self._make_key(q , limit)
        if key in self.cache:
            del self.cache

search_cache = SearchCache(maxsize=200, ttl=60)
