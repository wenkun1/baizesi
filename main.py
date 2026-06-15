# main.py
import time
from collections import deque

from Information.qiwei import get_latest_wechat_message
from rpa_bridge import send_wechat_reply
from session.session_manager import SessionManager
from storage.init_db import init_database
from user.user_manager import UserManager
from workflow.workflow_engine import WorkflowEngine


POLL_INTERVAL_SECONDS = 1


def get_or_create_session(
        sessions,
        user_manager,
        account_id
):
    if account_id in sessions:
        return sessions[account_id]

    user, created = user_manager.ensure_user(
        account_id=account_id,
        user_name=account_id
    )

    session = SessionManager(
        account_id=account_id,
        user_id=user["id"],
        user_info={
            "display_name": account_id
        }
    )
    sessions[account_id] = session

    if created:
        print(f"首次进线已自动注册，用户ID：{user['id']}")

    return session


def enqueue_message(
        msg,
        processed_msg_ids,
        user_message_queues,
        message_order_queue
):
    msg_id = str(msg.get("msg_id") or "")
    account_id = msg.get("user")

    if not msg_id or not account_id:
        return False

    if msg_id in processed_msg_ids:
        return False

    processed_msg_ids.add(msg_id)

    if account_id not in user_message_queues:
        user_message_queues[account_id] = deque()

    user_message_queues[account_id].append(msg)
    message_order_queue.append(account_id)

    return True


def process_queued_messages(
        sessions,
        user_manager,
        engine,
        user_message_queues,
        message_order_queue
):
    while message_order_queue:
        account_id = message_order_queue.popleft()
        user_queue = user_message_queues.get(account_id)

        if not user_queue:
            continue

        msg = user_queue.popleft()

        if not user_queue:
            user_message_queues.pop(account_id, None)

        session = get_or_create_session(
            sessions,
            user_manager,
            account_id
        )

        result = engine.process(
            session,
            msg["text"]
        )

        print(f"用户({account_id})：{msg['text']}")
        send_wechat_reply(
            result["reply"],
            contact_name=account_id,
            account_id=account_id
        )


def mark_current_latest_as_processed(processed_msg_ids):
    msg = get_latest_wechat_message()

    if not msg:
        return

    msg_id = str(msg.get("msg_id") or "")

    if msg_id:
        processed_msg_ids.add(msg_id)


def main():
    init_database()

    user_manager = UserManager()
    engine = WorkflowEngine()
    sessions = {}
    processed_msg_ids = set()
    user_message_queues = {}
    message_order_queue = deque()

    mark_current_latest_as_processed(processed_msg_ids)

    while True:
        msg = get_latest_wechat_message()

        if msg:
            enqueue_message(
                msg,
                processed_msg_ids,
                user_message_queues,
                message_order_queue
            )
            process_queued_messages(
                sessions,
                user_manager,
                engine,
                user_message_queues,
                message_order_queue
            )

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
