# 📚 Library API with Cache

<div align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Cachetools-FF6F00?style=for-the-badge&logo=python&logoColor=white"/>
</div>

<p align="center">
  <b>A high-performance Library API with in-memory caching layer</b><br/>
  Built on top of the original <a href="https://github.com/neo-0706/library-api-with-in-memory-cache">Library API</a> project
</p>

---

## 🔄 About This Project

This repository is an **enhanced version** of my previous [Library API](https://github.com/yourusername/library-api) project. The base functionality (database setup, raw SQL queries, FastAPI endpoints) remains the same as the original project.

### What's from the original project?
- ✅ PostgreSQL database setup (`authors` & `books` tables)
- ✅ Raw SQL queries with `JOIN` and `GROUP BY`
- ✅ FastAPI endpoints structure
- ✅ Database connection pooling
- ✅ Search functionality with `ILIKE`

### 🚀 What's new in this version?

This project adds a **caching layer** to significantly improve performance and reduce database load:

---

## ✨ New Features (Caching Layer)

### 1. **In-Memory Caching with TTLCache**
- Search results are cached in RAM for **60 seconds** (configurable)
- Each cache entry automatically expires after TTL
- Maximum cache size: **200 items** (prevents memory overflow)

### 2. **Smart Caching Decorator**
```python
@cached  # ← One line adds caching to any endpoint!
async def search_authors(q: str, limit: int):
    # Original database logic remains untouched

    3. **Cache Statistics Endpoint**

Monitor cache performance in real-time:
GET /cache-stats
{
  "hits": 42,
  "misses": 58,
  "total_requests": 100,
  "hit_ratio_percent": 42.0,
  "current_cache_size": 15,
  "max_cache_size": 200
}
4. Cache Management

Manually clear the cache when needed:
POST /cache-clear

📊 Performance Improvements
Scenario	Without Cache	With Cache	Improvement
First request (cache miss)	50-100ms	50-100ms	-
Repeated request (cache hit)	50-100ms	1-5ms	🚀 10-20x faster
1000 repeated requests	~50 seconds	~1 second	🚀 50x less load

🏗️ Cache Architecture
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│   @cached    │────▶│    Cache    │
└─────────────┘     │  Decorator   │     │   Storage   │
                    └──────────────┘     └─────────────┘
                           │                     │
                           ▼                     ▼
                    ┌──────────────┐     ┌─────────────┐
                    │   Database   │     │   Hit/Miss  │
                    │    Query     │     │  Statistics │
                    └──────────────┘     └─────────────┘

Cache Workflow:

    Cache Hit → Return cached result instantly

    Cache Miss → Query database → Store in cache → Return result

🔧 New Files Added

library-api-with-cache/
├── app/
│   ├── cache.py          # NEW: Cache manager with TTLCache
│   ├── decorators.py     # NEW: @cached decorator
│   └── main.py           # UPDATED: Added cache endpoints

📄 app/cache.py

    SearchCache class managing all cache operations

    TTL-based expiration

    Hit/miss statistics tracking

    Thread-safe operations

📄 app/decorators.py

    @cached decorator for easy endpoint caching

    Preserves function metadata with @wraps

    Handles async functions seamlessly

🚀 Quick Start
Prerequisites

    Python 3.9+

    PostgreSQL 12+

Installation

# Clone the repository
git clone https://github.com/yourusername/library-api-with-cache.git
cd library-api-with-cache

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Configure database
cp app/.env.example app/.env
# Edit .env with your database credentials

# Create database tables (using original schema)
psql -U your_user -d library_db -f schema.sql

# Insert sample data
psql -U your_user -d library_db -f sample_data.sql

# Run the server
uvicorn app.main:app --reload --port 8000

📖 API Endpoints
Method	Endpoint	Description
GET	/search/authors?q={query}&limit={n}	Search authors (cached)
GET	/cache-stats	Get cache performance statistics
POST	/cache-clear	Manually clear all cache
GET	/health	Health check

Example Requests

# Search (first request - cache miss)
curl "http://localhost:8000/search/authors?q=orwell"

# Same search again (cache hit) - much faster!
curl "http://localhost:8000/search/authors?q=orwell"

# Check cache performance
curl "http://localhost:8000/cache-stats"

# Clear cache if needed
curl -X POST "http://localhost:8000/cache-clear"

🧪 Testing Cache Performance
# Install Locust for load testing
pip install locust

# Run load test
locust -f locustfile.py --host=http://localhost:8000

# Open browser at http://localhost:8009
# Start with 100 users and watch cache statistics grow!

📊 Expected Cache Statistics

After running a few searches, you should see:

{
  "hits": 75,
  "misses": 25,
  "total_requests": 100,
  "hit_ratio_percent": 75.0,
  "current_cache_size": 8,
  "max_cache_size": 200
}
A hit ratio above 60% indicates effective caching!

🛠️ Configuration

You can adjust cache settings in app/cache.py:

search_cache = SearchCache(
    maxsize=200,  # Maximum items in cache
    ttl=60        # Time to live in seconds
)
📝 Dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
pydantic-settings==2.1.0
cachetools==5.3.1          # NEW: For TTLCache

