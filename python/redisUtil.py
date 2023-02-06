import redis
import os


host=os.getenv("REDIS_HOST")
port=os.getenv("REDIS_PORT")

pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# r = redis.Redis(host=host, port=port, decode_responses=True)

redis_msg_key = "MESSIGE_ID:"


def set_msg(msgId):
    """默认过期时间15m"""
    r.set(redis_msg_key + msgId, msgId, ex=15 * 60)


def get_msg(msgId):
    return r.get(redis_msg_key + msgId)


def if_msg_value_repetition(msgId):
    # print("msgId ---> ",msgId)
    key = redis_msg_key + msgId
    # print("r.exists(key)->",r.exists(key))
    if r.exists(key):
        # print("get_msg(msgId) ---> ", get_msg(msgId))
        return get_msg(msgId) is not None
    else:
        # 是新消息
        set_msg(msgId)
        return False


