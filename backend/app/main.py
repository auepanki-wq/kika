from __future__ import annotations

import base64
import binascii
import codecs
import html
import string
import urllib.parse
import unicodedata
from enum import Enum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


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


class TransformRequest(BaseModel):
    codec: CodecName
    direction: Direction
    value: str = Field(..., description="Input text")
    shift: int = Field(3, description="Only for caesar codec")
    normalization_form: str = Field("NFC", description="Only for unicode_normalize codec")


class TransformResponse(BaseModel):
    codec: CodecName
    direction: Direction
    input: str
    output: str


app = FastAPI(title="CTF Web Hub API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/transform", response_model=TransformResponse)
def transform(req: TransformRequest) -> TransformResponse:
    try:
        output = _transform(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return TransformResponse(
        codec=req.codec,
        direction=req.direction,
        input=req.value,
        output=output,
    )


def _transform(req: TransformRequest) -> str:
    if req.codec == CodecName.URL:
        return _url(req.value, req.direction)
    if req.codec == CodecName.BASE64:
        return _base64(req.value, req.direction)
    if req.codec == CodecName.HEX:
        return _hex(req.value, req.direction)
    if req.codec == CodecName.HTML:
        return _html(req.value, req.direction)
    if req.codec == CodecName.ROT13:
        return codecs.encode(req.value, "rot_13")
    if req.codec == CodecName.CAESAR:
        return _caesar(req.value, req.direction, req.shift)
    if req.codec == CodecName.UNICODE_NORMALIZE:
        return _unicode_normalize(req.value, req.normalization_form)
    raise ValueError(f"Unsupported codec: {req.codec}")


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
