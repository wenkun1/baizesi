import requests

CHAT_URL = "http://192.168.80.12:8060/api/v1/wechat-archive/chat/history?limit=1"

def get_latest_wechat_message():
    """
    获取最新一条用户消息
    """
    try:
        resp = requests.get(CHAT_URL, timeout=10)
        data = resp.json()

        if data["status"] != "success":
            return None

        messages = data.get("data", [])

        if not messages:
            return None

        msg = messages[0]

        # 只处理文本消息
        if msg["msg_type"] != "text":
            return None

        return {
            "msg_id": msg["msg_id"],
            "user": msg["from_user"],
            "text": msg["content"]["text"]
        }

    except Exception as e:
        print("获取企业微信消息失败：", e)
        return None