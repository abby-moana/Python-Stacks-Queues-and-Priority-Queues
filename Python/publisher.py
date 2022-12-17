import redis

with redis.Redis() as client:
    while True:
        message = input("Message: ")
