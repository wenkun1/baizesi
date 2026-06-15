import json
import os
from urllib import request


class WeChatArchiveClient:

    def __init__(
            self,
            source,
            timeout=5
    ):
        self.source = source
        self.timeout = timeout

    def fetch(self):
        if self._is_local_file():
            with open(
                    self.source,
                    "r",
                    encoding="utf-8"
            ) as file:
                return json.load(file)

        req = request.Request(
            self.source,
            headers={
                "Accept": "application/json"
            }
        )

        with request.urlopen(
                req,
                timeout=self.timeout
        ) as response:
            charset = (
                response.headers.get_content_charset()
                or "utf-8"
            )
            body = response.read().decode(charset)

        return json.loads(body)

    def _is_local_file(self):
        return (
            "://" not in self.source
            and os.path.exists(self.source)
        )

    @staticmethod
    def messages_from_payload(payload):
        if not isinstance(payload, dict):
            return []

        data = payload.get("data", [])

        if not isinstance(data, list):
            return []

        return data
