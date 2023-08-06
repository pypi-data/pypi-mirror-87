import json

from typing import Any


def encode_data(data: Any) -> bytes:
    return json.dumps(data).encode(encoding="utf-8")


def decode_data(data: bytes) -> Any:
    return json.loads(data.decode(encoding="utf-8"))
