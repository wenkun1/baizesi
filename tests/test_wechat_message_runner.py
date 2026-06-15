import unittest
import sys
from collections import deque
from types import SimpleNamespace

sys.modules.setdefault(
    "pymysql",
    SimpleNamespace(
        cursors=SimpleNamespace(DictCursor=object),
        connect=lambda *args, **kwargs: None
    )
)
sys.modules.setdefault(
    "openai",
    SimpleNamespace(OpenAI=lambda *args, **kwargs: None)
)

from wechat.message_runner import WeChatMessageRunner


class FakeArchiveClient:
    source = "fake"

    @staticmethod
    def messages_from_payload(payload):
        return payload.get("data", [])


class FakeUserManager:

    def ensure_user(
            self,
            account_id,
            user_name=None,
            department=None,
            employee_no=None
    ):
        return {
            "id": sum(ord(char) for char in account_id),
            "account_id": account_id,
            "user_name": user_name or account_id,
            "department": department,
            "employee_no": employee_no
        }, False


class FakeWorkflowEngine:

    def __init__(self):
        self.calls = []

    def process(self, session, text):
        session.user_info["message_count"] = (
            session.user_info.get("message_count", 0) + 1
        )
        self.calls.append((session.account_id, text))

        return {
            "finish": False,
            "reply": (
                f"{session.account_id}:"
                f"{session.user_info['message_count']}:"
                f"{text}"
            )
        }


def make_message(
        msg_id,
        account_id,
        text,
        msg_time,
        row_id=None,
        to_users=None
):
    return {
        "id": row_id or int(msg_id),
        "msg_id": str(msg_id),
        "msg_time": msg_time,
        "msg_type": "text",
        "from_user": account_id,
        "from_user_display": account_id,
        "to_users": to_users or ["assistant@chinasns.com"],
        "content": {
            "text": text
        }
    }


class WeChatMessageRunnerTest(unittest.TestCase):

    def make_runner(self, skip_existing=False):
        runner = WeChatMessageRunner.__new__(WeChatMessageRunner)
        runner.archive_client = FakeArchiveClient()
        runner.bot_account = "assistant@chinasns.com"
        runner.poll_interval = 2
        runner.skip_existing = skip_existing
        runner.user_manager = FakeUserManager()
        runner.engine = FakeWorkflowEngine()
        runner.sessions = {}
        runner.user_message_queues = {}
        runner.message_order_queue = deque()
        runner.processed_message_keys = set()
        runner.initialized = False
        return runner

    def test_first_poll_marks_existing_messages_when_skip_existing(self):
        runner = self.make_runner(skip_existing=True)
        old_message = make_message(1, "alice", "old", "2026-06-15 10:00:00")
        new_message = make_message(2, "alice", "new", "2026-06-15 10:01:00")

        first_replies = runner.process_payload({
            "data": [old_message]
        })
        second_replies = runner.process_payload({
            "data": [old_message, new_message]
        })

        self.assertEqual(first_replies, [])
        self.assertEqual(len(second_replies), 1)
        self.assertEqual(second_replies[0].text, "new")
        self.assertEqual(runner.engine.calls, [("alice", "new")])

    def test_messages_are_processed_by_global_arrival_order(self):
        runner = self.make_runner()
        messages = [
            make_message(3, "alice", "alice second", "2026-06-15 10:03:00"),
            make_message(1, "alice", "alice first", "2026-06-15 10:01:00"),
            make_message(2, "bob", "bob first", "2026-06-15 10:02:00")
        ]

        replies = runner.process_payload({
            "data": messages
        })

        self.assertEqual(
            [reply.text for reply in replies],
            ["alice first", "bob first", "alice second"]
        )
        self.assertEqual(
            runner.engine.calls,
            [
                ("alice", "alice first"),
                ("bob", "bob first"),
                ("alice", "alice second")
            ]
        )

    def test_each_user_keeps_an_independent_session(self):
        runner = self.make_runner()

        replies = runner.process_payload({
            "data": [
                make_message(1, "alice", "a1", "2026-06-15 10:01:00"),
                make_message(2, "bob", "b1", "2026-06-15 10:02:00"),
                make_message(3, "alice", "a2", "2026-06-15 10:03:00"),
                make_message(4, "bob", "b2", "2026-06-15 10:04:00")
            ]
        })

        self.assertEqual(
            [reply.reply for reply in replies],
            [
                "alice:1:a1",
                "bob:1:b1",
                "alice:2:a2",
                "bob:2:b2"
            ]
        )
        self.assertIsNot(
            runner.sessions["alice"],
            runner.sessions["bob"]
        )

    def test_bot_account_messages_are_skipped(self):
        runner = self.make_runner()

        replies = runner.process_payload({
            "data": [
                make_message(
                    1,
                    " assistant@chinasns.com ",
                    "bot echo",
                    "2026-06-15 10:01:00"
                ),
                make_message(
                    2,
                    "alice",
                    "customer message",
                    "2026-06-15 10:02:00"
                )
            ]
        })

        self.assertEqual(
            [reply.text for reply in replies],
            ["customer message"]
        )
        self.assertEqual(
            runner.engine.calls,
            [("alice", "customer message")]
        )


if __name__ == "__main__":
    unittest.main()
