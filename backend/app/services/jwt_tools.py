from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass
from typing import Any


@dataclass
class JWTParts:
    header: dict[str, Any]
    payload: dict[str, Any]
    signature: str


SUPPORTED_ALGS = {
    "HS256": hashlib.sha256,
    "HS384": hashlib.sha384,
    "HS512": hashlib.sha512,
}


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data + padding)


def decode_jwt(token: str) -> JWTParts:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("JWT must contain exactly three dot-separated parts")

    try:
        header = json.loads(_b64url_decode(parts[0]).decode("utf-8"))
        payload = json.loads(_b64url_decode(parts[1]).decode("utf-8"))
    except Exception as exc:
        raise ValueError("Failed to decode JWT header/payload") from exc

    if not isinstance(header, dict) or not isinstance(payload, dict):
        raise ValueError("JWT header and payload must be JSON objects")

    return JWTParts(header=header, payload=payload, signature=parts[2])


def sign_jwt(header: dict[str, Any], payload: dict[str, Any], secret: str, algorithm: str) -> str:
    if algorithm not in SUPPORTED_ALGS:
        raise ValueError("Unsupported algorithm. Allowed: HS256, HS384, HS512")

    encoded_header = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    encoded_payload = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")

    digest = SUPPORTED_ALGS[algorithm]
    signature = hmac.new(secret.encode("utf-8"), signing_input, digest).digest()

    return f"{encoded_header}.{encoded_payload}.{_b64url_encode(signature)}"


def verify_jwt(token: str, secret: str) -> bool:
    parts = decode_jwt(token)
    algorithm = parts.header.get("alg")
    if algorithm not in SUPPORTED_ALGS:
        raise ValueError("Unsupported algorithm. Allowed: HS256, HS384, HS512")

    expected = sign_jwt(parts.header, parts.payload, secret, algorithm)
    expected_signature = expected.split(".")[2]
    return hmac.compare_digest(parts.signature, expected_signature)
