import time
from collections import deque
from dataclasses import dataclass

from session.session_manager import SessionManager
from user.user_manager import UserManager
from workflow.workflow_engine import WorkflowEngine


@dataclass
class WeChatReply:
    account_id: str
    display_name: str
    msg_id: str
    msg_time: str
    text: str
    reply: str


class WeChatMessageRunner:

    def __init__(
            self,
            archive_client,
            bot_account="assistant@chinasns.com",
            poll_interval=2,
            skip_existing=True
    ):
        self.archive_client = archive_client
        self.bot_account = bot_account
        self.poll_interval = poll_interval
        self.skip_existing = skip_existing

        self.user_manager = UserManager()
        self.engine = WorkflowEngine()
        self.sessions = {}
        self.user_message_queues = {}
        self.message_order_queue = deque()
        self.processed_message_keys = set()
        self.initialized = False

    def run_forever(self):
        print(
            f"企业微信监听启动：{self.archive_client.source}"
        )
        print(
            f"机器人账号：{self.bot_account}"
        )

        while True:
            try:
                replies = self.poll_once()

                for reply in replies:
                    print(self.format_reply(reply))

            except KeyboardInterrupt:
                print("企业微信监听已停止")
                raise

            except Exception as exc:
                print(f"企业微信监听异常：{exc}")

            time.sleep(self.poll_interval)

    def poll_once(self):
        payload = self.archive_client.fetch()

        return self.process_payload(payload)

    def process_payload(self, payload):
        messages = self.archive_client.messages_from_payload(
            payload
        )

        messages = self._sort_messages(messages)

        if self.skip_existing and not self.initialized:
            for message in messages:
                self._remember_message(message)

            self.initialized = True
            return []

        self.initialized = True

        for message in messages:
            self.enqueue_message(message)

        return self.process_queued_messages()

    def enqueue_message(self, message):
        message_key = self._message_key(message)

        if not message_key:
            return False

        if message_key in self.processed_message_keys:
            return False

        self._remember_message(message)

        if not self._is_incoming_text(message):
            return False

        account_id = message.get("from_user")

        if not account_id:
            return False

        if account_id not in self.user_message_queues:
            self.user_message_queues[account_id] = deque()

        self.user_message_queues[account_id].append(message)
        self.message_order_queue.append(account_id)

        return True

    def process_queued_messages(self):
        replies = []

        while self.message_order_queue:
            account_id = self.message_order_queue.popleft()
            user_queue = self.user_message_queues.get(account_id)

            if not user_queue:
                continue

            message = user_queue.popleft()

            if not user_queue:
                self.user_message_queues.pop(account_id, None)

            reply = self._process_message(message)

            if reply:
                replies.append(reply)

        return replies

    def process_message(self, message):
        if not self.enqueue_message(message):
            return None

        replies = self.process_queued_messages()

        if not replies:
            return None

        return replies[0]

    def _process_message(self, message):
        if not self._is_incoming_text(message):
            return None

        account_id = message.get("from_user")
        display_name = (
            message.get("from_user_display")
            or account_id
        )
        text = self._extract_text(message).strip()

        session, register_reply = self._get_or_create_session(
            account_id,
            display_name
        )

        result = self.engine.process(
            session,
            text
        )

        reply_text = result.get("reply", "")

        if register_reply:
            reply_text = f"{register_reply}\nAI：{reply_text}"

        return WeChatReply(
            account_id=account_id,
            display_name=display_name,
            msg_id=str(message.get("msg_id") or ""),
            msg_time=str(message.get("msg_time") or ""),
            text=text,
            reply=reply_text
        )

    def _get_or_create_session(
            self,
            account_id,
            display_name
    ):
        if account_id in self.sessions:
            return self.sessions[account_id], None

        user, created = self.user_manager.ensure_user(
            account_id=account_id,
            user_name=display_name
        )

        session = SessionManager(
            account_id=account_id,
            user_id=user["id"],
            user_info={
                "display_name": display_name
            }
        )

        self.sessions[account_id] = session

        if not created:
            return session, None

        return (
            session,
            f"首次进线已自动注册，用户ID：{user['id']}"
        )

    def _is_incoming_text(self, message):
        if message.get("msg_type") != "text":
            return False

        account_id = message.get("from_user")

        if not account_id:
            return False

        if self._is_bot_account(account_id):
            return False

        to_users = message.get("to_users") or []
        room_id = message.get("room_id")

        if (
                self.bot_account
                and not room_id
                and to_users
                and not any(
                    self._is_bot_account(to_user)
                    for to_user in to_users
                )
        ):
            return False

        return bool(self._extract_text(message).strip())

    def _extract_text(self, message):
        content = message.get("content") or {}

        if not isinstance(content, dict):
            return ""

        return str(content.get("text") or "")

    def _is_bot_account(self, account_id):
        if not self.bot_account or not account_id:
            return False

        return (
            str(account_id).strip().lower()
            == str(self.bot_account).strip().lower()
        )

    def _message_key(self, message):
        return str(
            message.get("msg_id")
            or message.get("id")
            or ""
        )

    def _remember_message(self, message):
        message_key = self._message_key(message)

        if message_key:
            self.processed_message_keys.add(message_key)

        if len(self.processed_message_keys) > 1000:
            self.processed_message_keys = set(
                list(self.processed_message_keys)[-500:]
            )

    @staticmethod
    def _sort_messages(messages):
        return sorted(
            messages,
            key=lambda item: (
                item.get("msg_time") or "",
                item.get("id") or 0,
                item.get("msg_id") or ""
            )
        )

    @staticmethod
    def format_reply(reply):
        return (
            "\n========== 企业微信消息 ==========\n"
            f"时间：{reply.msg_time}\n"
            f"用户：{reply.display_name} ({reply.account_id})\n"
            f"消息：{reply.text}\n"
            f"AI：{reply.reply}\n"
            "================================"
        )
