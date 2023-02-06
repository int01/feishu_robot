import redis
import os

host = os.getenv("REDIS_HOST")
port = os.getenv("REDIS_PORT")

pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
r = redis.Redis(connection_pool=pool)

# r = redis.Redis(host=host, port=port, decode_responses=True)

redis_msg_key = "MESSIGE_ID:"
redis_msg_txt_key = "USER_OPENID:"


def set_msg(msgId):
    """过期时间15m"""
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


def set_msg_txt(userOpenId, text):
    """过期时间5m"""
    r.set(redis_msg_txt_key + userOpenId, text, ex=30)


def get_msg_txt(userOpenId):
    return r.get(redis_msg_txt_key + userOpenId)


def build_req_msg_txt(userOpenId, text):
    """ 处理连续性的提问 需要将聊天记录一起发送，用'\n\n'分隔每句话 TODO """
    key = redis_msg_txt_key + userOpenId
    if r.exists(key):
        r_text = get_msg_txt(userOpenId) + "\n\n" + text

        # 临时的处理逻辑
        if len(r_text) > 1000:
            set_msg_txt(userOpenId, text)
            return text

        set_msg_txt(userOpenId, r_text)
        return r_text
    else:
        set_msg_txt(userOpenId, text)
        return text


def build_resp_msg_txt(userOpenId, text):
    """将ai的回复加到问句中"""
    r_text = get_msg_txt(userOpenId) + "\n" + text
    set_msg_txt(userOpenId, r_text)
