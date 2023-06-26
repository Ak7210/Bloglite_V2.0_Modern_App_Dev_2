from flask_caching import Cache
cache = Cache(config={'CACHE_TYPE': "RedisCache",
                      'CACHE_REDIS_HOST': "localhost",
                      'CACHE_REDIS_PORT': 6379, 'CACHE_REDIS_DB': 3,
                      'CACHE_REDIS_URL': "redis://localhost:6379/4"})

# using the redis database cache in the application is 3. and the redis url server is 4.