import unittest

from app.services.jwt_tools import decode_jwt, sign_jwt, verify_jwt
from app.services.transformers import CodecName, Direction, transform_text


class TransformTests(unittest.TestCase):
    def test_base64_roundtrip(self):
        encoded = transform_text(CodecName.BASE64, Direction.ENCODE, "hello")
        self.assertEqual(encoded, "aGVsbG8=")
        decoded = transform_text(CodecName.BASE64, Direction.DECODE, encoded)
        self.assertEqual(decoded, "hello")

    def test_hex_roundtrip(self):
        encoded = transform_text(CodecName.HEX, Direction.ENCODE, "Hi")
        self.assertEqual(encoded, "4869")
        self.assertEqual(transform_text(CodecName.HEX, Direction.DECODE, encoded), "Hi")

    def test_caesar_roundtrip(self):
        encoded = transform_text(CodecName.CAESAR, Direction.ENCODE, "Attack", shift=5)
        self.assertEqual(transform_text(CodecName.CAESAR, Direction.DECODE, encoded, shift=5), "Attack")


class JWTTests(unittest.TestCase):
    def test_sign_decode_verify(self):
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"sub": "alice", "admin": False}
        token = sign_jwt(header, payload, "very-long-secret", "HS256")

        decoded = decode_jwt(token)
        self.assertEqual(decoded.payload["sub"], "alice")
        self.assertTrue(verify_jwt(token, "very-long-secret"))
        self.assertFalse(verify_jwt(token, "wrong-secret"))


if __name__ == "__main__":
    unittest.main()
