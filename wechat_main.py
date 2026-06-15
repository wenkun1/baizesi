import argparse
import os
import time

from rpa_bridge import send_wechat_reply
from storage.init_db import init_database
from wechat.archive_client import WeChatArchiveClient
from wechat.message_runner import WeChatMessageRunner


DEFAULT_HISTORY_SOURCE = (
    "http://192.168.80.12:8060"
    "/api/v1/wechat-archive/chat/history?limit=1"
)
DEFAULT_BOT_ACCOUNT = "assistant@chinasns.com"


def parse_args():
    parser = argparse.ArgumentParser(
        description="从企业微信历史接口实时读取消息并进入白泽思流程"
    )

    parser.add_argument(
        "--source",
        default=os.getenv(
            "WECHAT_HISTORY_SOURCE",
            DEFAULT_HISTORY_SOURCE
        ),
        help="企业微信历史接口 URL，或本地 JSON 文件路径"
    )

    parser.add_argument(
        "--bot-account",
        default=os.getenv(
            "WECHAT_BOT_ACCOUNT",
            DEFAULT_BOT_ACCOUNT
        ),
        help="机器人企业微信账号，用于过滤自己发出的消息"
    )

    parser.add_argument(
        "--interval",
        type=float,
        default=float(os.getenv("WECHAT_POLL_INTERVAL", "2")),
        help="轮询间隔秒数"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.getenv("WECHAT_HTTP_TIMEOUT", "5")),
        help="HTTP 请求超时时间秒数"
    )

    parser.add_argument(
        "--skip-existing",
        action="store_true",
        default=True,
        help="启动时只记录当前最新消息，从下一条新消息开始处理"
    )

    parser.add_argument(
        "--process-existing",
        action="store_false",
        dest="skip_existing",
        help="启动时处理接口当前返回的已有消息"
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="只拉取并处理一次，便于用本地 JSON 验证"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    init_database()

    client = WeChatArchiveClient(
        source=args.source,
        timeout=args.timeout
    )

    runner = WeChatMessageRunner(
        archive_client=client,
        bot_account=args.bot_account,
        poll_interval=args.interval,
        skip_existing=args.skip_existing
    )

    if args.once:
        for reply in runner.poll_once():
            send_wechat_reply(
                reply.reply,
                contact_name=reply.display_name,
                account_id=reply.account_id
            )
        return

    print(f"企业微信监听启动：{args.source}")
    print(f"机器人账号：{args.bot_account}")

    while True:
        try:
            for reply in runner.poll_once():
                send_wechat_reply(
                    reply.reply,
                    contact_name=reply.display_name,
                    account_id=reply.account_id
                )

        except KeyboardInterrupt:
            print("企业微信监听已停止")
            raise

        except Exception as exc:
            print(f"企业微信监听异常：{exc}")

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
