import os
import redis

# Get environment variable for REDIS_URL or use default
REDIS_URL = os.getenv('REDIS_URL', "redis://localhost:6379")

# Establish connection to Redis
r = redis.Redis.from_url(REDIS_URL)

def increment_count():
    try:
        count = r.get('count')
        if count is None:
            # if count does not exist, create it
            count = 0
        else:
            count = int(count)

        count += 1
        r.set('count', count)
        print(f"Incremented count to {count}")

    except redis.RedisError as e:
        print(f"An error occurred while incrementing count: {e}")

def get_count():
    try:
        count = r.get('count')
        if count is not None:
            return int(count)
        else:
            return 0
    except redis.RedisError as e:
        print(f"An error occurred while fetching count: {e}")
        return None

if __name__ == '__main__':
    increment_count()