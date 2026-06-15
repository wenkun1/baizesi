import os
import sys
from threading import Lock
from pathlib import Path


RPA_DIR = Path(os.getenv(
    "BAIZESI_RPA_DIR",
    r"E:\Project\furongxiaomei\Work_order_organization\RPA"
))

WORKFLOW_PATH = Path(os.getenv(
    "BAIZESI_RPA_WORKFLOW_PATH",
    str(RPA_DIR / "workflows" / "wechat_copy.json")
))

ELEMENT_PATH = Path(os.getenv(
    "BAIZESI_RPA_ELEMENT_PATH",
    str(RPA_DIR / "elements" / "wechat_elements.json")
))

_RPA_SEND_LOCK = Lock()


def send_wechat_reply(reply_text, contact_name=None, account_id=None):
    reply_text = str(reply_text or "").strip()
    contact_name = str(contact_name or account_id or "").strip()
    account_id = str(account_id or "").strip()

    if not reply_text:
        return False

    rpa_dir = str(RPA_DIR)

    if rpa_dir not in sys.path:
        sys.path.insert(0, rpa_dir)

    from engine import run_workflow

    with _RPA_SEND_LOCK:
        run_workflow(
            workflow_path=str(WORKFLOW_PATH),
            element_path=str(ELEMENT_PATH),
            runtime={
                "reply": reply_text,
                "contact_name": contact_name,
                "account_id": account_id
            }
        )

    return True
