from __future__ import annotations

import base64
import binascii
import codecs
import html
import string
import urllib.parse
import unicodedata
from enum import Enum


class Direction(str, Enum):
    ENCODE = "encode"
    DECODE = "decode"


class CodecName(str, Enum):
    URL = "url"
    BASE64 = "base64"
    HEX = "hex"
    HTML = "html"
    ROT13 = "rot13"
    CAESAR = "caesar"
    UNICODE_NORMALIZE = "unicode_normalize"


def transform_text(
    codec: CodecName,
    direction: Direction,
    value: str,
    shift: int = 3,
    normalization_form: str = "NFC",
) -> str:
    if codec == CodecName.URL:
        return _url(value, direction)
    if codec == CodecName.BASE64:
        return _base64(value, direction)
    if codec == CodecName.HEX:
        return _hex(value, direction)
    if codec == CodecName.HTML:
        return _html(value, direction)
    if codec == CodecName.ROT13:
        return codecs.encode(value, "rot_13")
    if codec == CodecName.CAESAR:
        return _caesar(value, direction, shift)
    if codec == CodecName.UNICODE_NORMALIZE:
        return _unicode_normalize(value, normalization_form)
    raise ValueError(f"Unsupported codec: {codec}")


def _url(value: str, direction: Direction) -> str:
    if direction == Direction.ENCODE:
        return urllib.parse.quote(value, safe="")
    return urllib.parse.unquote(value)


def _base64(value: str, direction: Direction) -> str:
    if direction == Direction.ENCODE:
        return base64.b64encode(value.encode("utf-8")).decode("ascii")
    try:
        decoded = base64.b64decode(value, validate=True)
    except binascii.Error as exc:
        raise ValueError("Invalid base64 input") from exc
    return decoded.decode("utf-8", errors="replace")


def _hex(value: str, direction: Direction) -> str:
    if direction == Direction.ENCODE:
        return value.encode("utf-8").hex()
    try:
        decoded = bytes.fromhex(value)
    except ValueError as exc:
        raise ValueError("Invalid hex input") from exc
    return decoded.decode("utf-8", errors="replace")


def _html(value: str, direction: Direction) -> str:
    if direction == Direction.ENCODE:
        return html.escape(value)
    return html.unescape(value)


def _caesar(value: str, direction: Direction, shift: int) -> str:
    if direction == Direction.DECODE:
        shift = -shift

    def shift_char(char: str) -> str:
        if char in string.ascii_lowercase:
            base = ord("a")
            return chr((ord(char) - base + shift) % 26 + base)
        if char in string.ascii_uppercase:
            base = ord("A")
            return chr((ord(char) - base + shift) % 26 + base)
        return char

    return "".join(shift_char(char) for char in value)


def _unicode_normalize(value: str, normalization_form: str) -> str:
    valid_forms = {"NFC", "NFD", "NFKC", "NFKD"}
    if normalization_form not in valid_forms:
        raise ValueError("normalization_form must be one of NFC, NFD, NFKC, NFKD")
    return unicodedata.normalize(normalization_form, value)
