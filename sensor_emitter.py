import redis
import os
import sys
import random
import time
import hashlib
import json
from dotenv import load_dotenv

load_dotenv()

redisClient = redis.from_url(os.getenv('REDIS_URL'), decode_responses=True)

brands = ["Toyota", "VW", "Honda", "Kia", "Audi", "BMW", "Mazda", "Nissan", "Hyundai", "Porsche", "Ferrari", "Fiat", "Peugeot", "Renault", "Citroen"]
colors = ["White", "Black", "Red", "Blue", "Grey", "Silver", "Pink"]
bodyType = ["Hatchback", "Sedan", "Estate", "Suv", "Truck"]


def run(sensor_id):
    """
    Generate mock car spottings to a Redis stream
    """
    print(f'Starting car spotter publishing to sensor:{sensor_id} stream')

    while True:
        m = hashlib.md5()
        m.update(str(time.time()).encode())

        payload = json.dumps({
            '_version': 'v1',
            'registration': m.hexdigest()[:8].upper(),
            'brand': random.choice(brands),
            'color': random.choice(colors),
            'body_type': random.choice(bodyType),
            'speed': random.randint(1, 200)
        }, sort_keys=True, indent=4)

        redisClient.xadd(
            f'sensor:{sensor_id}',
            { 'payload': payload},
            maxlen=10000
        )
        time.sleep(1)


if __name__ == "__main__":
    """
    Example: python sensor_emitter.py sensor_id
    """
    run(sys.argv[1])
