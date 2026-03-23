from __future__ import annotations

import hashlib
from typing import Any

from itsdangerous import BadSignature, URLSafeTimedSerializer

DEFAULT_SALT = "cookie-session"


def _serializer(secret: str, salt: str = DEFAULT_SALT) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(
        secret_key=secret,
        salt=salt,
        serializer_kwargs={"sort_keys": True},
        signer_kwargs={"key_derivation": "hmac", "digest_method": hashlib.sha1},
    )


def decode_cookie(cookie_value: str) -> dict[str, Any]:
    if "." not in cookie_value:
        raise ValueError("Cookie format is invalid")

    payload_part = cookie_value.split(".", 1)[0]
    # Flask prepends a leading dot for compressed payloads; ignore for display.
    payload_part = payload_part.lstrip(".")

    import base64
    import json
    import zlib

    padding = "=" * ((4 - len(payload_part) % 4) % 4)

    try:
        raw = base64.urlsafe_b64decode(payload_part + padding)
        try:
            raw = zlib.decompress(raw)
        except zlib.error:
            pass
        parsed = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise ValueError("Could not decode cookie payload") from exc

    if not isinstance(parsed, dict):
        raise ValueError("Cookie payload must decode to JSON object")
    return parsed


def verify_cookie(cookie_value: str, secret: str, salt: str = DEFAULT_SALT) -> bool:
    serializer = _serializer(secret=secret, salt=salt)
    try:
        serializer.loads(cookie_value)
        return True
    except BadSignature:
        return False


def sign_cookie(payload: dict[str, Any], secret: str, salt: str = DEFAULT_SALT) -> str:
    serializer = _serializer(secret=secret, salt=salt)
    return serializer.dumps(payload)
