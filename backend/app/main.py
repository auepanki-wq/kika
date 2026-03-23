from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.services.flask_unsign_tools import decode_cookie, sign_cookie, verify_cookie
from app.services.jwt_tools import decode_jwt, sign_jwt, verify_jwt
from app.services.transformers import CodecName, Direction, transform_text


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


class JWTDecodeRequest(BaseModel):
    token: str


class JWTDecodeResponse(BaseModel):
    header: dict[str, Any]
    payload: dict[str, Any]
    signature: str


class JWTSignRequest(BaseModel):
    header: dict[str, Any]
    payload: dict[str, Any]
    secret: str
    algorithm: str = "HS256"


class JWTSignResponse(BaseModel):
    token: str


class JWTVerifyRequest(BaseModel):
    token: str
    secret: str


class JWTVerifyResponse(BaseModel):
    valid: bool


class FlaskDecodeRequest(BaseModel):
    cookie: str


class FlaskDecodeResponse(BaseModel):
    payload: dict[str, Any]


class FlaskSignRequest(BaseModel):
    payload: dict[str, Any]
    secret: str
    salt: str = "cookie-session"


class FlaskSignResponse(BaseModel):
    cookie: str


class FlaskVerifyRequest(BaseModel):
    cookie: str
    secret: str
    salt: str = "cookie-session"


class FlaskVerifyResponse(BaseModel):
    valid: bool


app = FastAPI(title="CTF Web Hub API", version="0.2.0")

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
        output = transform_text(
            codec=req.codec,
            direction=req.direction,
            value=req.value,
            shift=req.shift,
            normalization_form=req.normalization_form,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return TransformResponse(codec=req.codec, direction=req.direction, input=req.value, output=output)


@app.post("/api/jwt/decode", response_model=JWTDecodeResponse)
def jwt_decode(req: JWTDecodeRequest) -> JWTDecodeResponse:
    try:
        parts = decode_jwt(req.token)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return JWTDecodeResponse(header=parts.header, payload=parts.payload, signature=parts.signature)


@app.post("/api/jwt/sign", response_model=JWTSignResponse)
def jwt_sign(req: JWTSignRequest) -> JWTSignResponse:
    try:
        token = sign_jwt(req.header, req.payload, req.secret, req.algorithm)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return JWTSignResponse(token=token)


@app.post("/api/jwt/verify", response_model=JWTVerifyResponse)
def jwt_verify(req: JWTVerifyRequest) -> JWTVerifyResponse:
    try:
        valid = verify_jwt(req.token, req.secret)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return JWTVerifyResponse(valid=valid)


@app.post("/api/flask-unsign/decode", response_model=FlaskDecodeResponse)
def flask_decode(req: FlaskDecodeRequest) -> FlaskDecodeResponse:
    try:
        payload = decode_cookie(req.cookie)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return FlaskDecodeResponse(payload=payload)


@app.post("/api/flask-unsign/sign", response_model=FlaskSignResponse)
def flask_sign(req: FlaskSignRequest) -> FlaskSignResponse:
    try:
        cookie = sign_cookie(payload=req.payload, secret=req.secret, salt=req.salt)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return FlaskSignResponse(cookie=cookie)


@app.post("/api/flask-unsign/verify", response_model=FlaskVerifyResponse)
def flask_verify(req: FlaskVerifyRequest) -> FlaskVerifyResponse:
    try:
        valid = verify_cookie(cookie_value=req.cookie, secret=req.secret, salt=req.salt)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return FlaskVerifyResponse(valid=valid)
