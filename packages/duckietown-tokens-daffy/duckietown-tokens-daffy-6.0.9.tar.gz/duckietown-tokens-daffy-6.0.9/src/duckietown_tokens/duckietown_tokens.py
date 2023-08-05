import json
import os
from typing import cast

import base58

from ecdsa import BadSignatureError, SigningKey, VerifyingKey, NIST192p

from . import logger

__all__ = [
    "DuckietownToken",
    "InvalidToken",
    "verify_token",
    "create_signed_token",
    "get_signing_key",
    "get_id_from_token",
]

private = "key1.pem"
public = "key1-pub.pem"
curve = NIST192p


class DuckietownToken:
    VERSION = "dt1"
    payload: bytes
    signature: bytes

    def __init__(self, payload: bytes, signature: bytes):
        self.payload = payload
        self.signature = signature

    def as_string(self):
        payload_58 = base58.b58encode(self.payload).decode("utf-8")
        signature_58 = base58.b58encode(self.signature).decode("utf-8")
        return "%s-%s-%s" % (DuckietownToken.VERSION, payload_58, signature_58)

    @staticmethod
    def from_string(s: str) -> "DuckietownToken":
        p = s.split("-")
        if len(p) != 3:
            raise ValueError(p)
        if p[0] != DuckietownToken.VERSION:
            raise ValueError(p[0])
        payload_base58 = p[1]
        signature_base58 = p[2]
        payload = base58.b58decode(payload_base58)
        signature = base58.b58decode(signature_base58)
        return DuckietownToken(payload, signature)


def get_signing_key() -> SigningKey:
    """ Loads the key in the location "private" """
    if not os.path.exists(private):
        logger.info(f"Creating private key {private!r}")
        sk0 = SigningKey.generate(curve=curve)
        with open(private, "wb") as f:
            p = cast(bytes, sk0.to_pem())  # docstring is wrong
            f.write(p)

        vk = sk0.get_verifying_key()
        with open(public, "wb") as f:
            q = cast(bytes, vk.to_pem())  # docstring is wrong
            f.write(q)
    with open(private, "r") as _:
        pem = _.read()
    sk = SigningKey.from_pem(pem)
    return cast(SigningKey, sk)


def get_verify_key() -> VerifyingKey:
    key1 = """-----BEGIN PUBLIC KEY-----
MEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAEQr/8RJmJZT+Bh1YMb1aqc2ao5teE
ixOeCMGTO79Dbvw5dGmHJLYyNPwnKkWayyJS
-----END PUBLIC KEY-----"""
    return VerifyingKey.from_pem(key1)


def create_signed_token(payload: bytes, sk: SigningKey = None) -> DuckietownToken:
    assert isinstance(payload, bytes), payload
    if sk is None:
        sk: SigningKey = get_signing_key()

    def entropy(numbytes: int) -> bytes:
        s = b"duckietown is a place of relaxed introspection" * 100
        return s[:numbytes]

    logger.info(f"signing payload {payload!r}")
    signature = sk.sign(payload, entropy=entropy)
    return DuckietownToken(payload, signature)


def verify_token(token: DuckietownToken):
    vk: VerifyingKey = get_verify_key()
    try:
        sig_ok = vk.verify(token.signature, token.payload)
    except BadSignatureError as e:
        #
        # if not sig_ok:
        msg = "Signature is invalid"
        raise InvalidToken(msg) from e
    try:
        data = json.loads(token.payload)
    except:
        msg = "Cannot load json"
        raise InvalidToken(msg)

    if "uid" not in data:
        msg = '"uid" not present'
        raise InvalidToken(msg)
    uid = data["uid"]
    if not isinstance(uid, int):
        msg = f"uid {uid!r} is not an integer."
        raise InvalidToken(msg)


class InvalidToken(Exception):
    pass


def get_id_from_token(s: str) -> int:
    """
        Returns a numeric ID from the token, or raises InvalidToken.

    """
    try:
        token = DuckietownToken.from_string(s)
    except ValueError:
        msg = "Invalid token format %r." % s
        raise InvalidToken(msg)

    verify_token(token)

    try:
        data = json.loads(token.payload)
        uid = data["uid"]
        return uid
    except ValueError:
        raise InvalidToken()
