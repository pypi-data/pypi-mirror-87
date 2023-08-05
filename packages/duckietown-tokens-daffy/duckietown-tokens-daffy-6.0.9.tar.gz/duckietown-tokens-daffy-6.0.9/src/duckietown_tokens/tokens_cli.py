import argparse
import datetime
import json
import sys

import dateutil.parser
from ecdsa import SigningKey
from future import builtins
from . import logger

from .duckietown_tokens import create_signed_token, DuckietownToken, get_verify_key

__all__ = ["main_verify", "main_generate"]


def main_verify(args=None):
    try:
        if args is None:
            args = sys.argv[1:]

        if args:
            token_s = args[0]
        else:
            msg = "Please enter token:\n> "
            token_s = builtins.input(msg)

        logger.info("Verifying token %r\n" % token_s)

        try:
            token = DuckietownToken.from_string(token_s)
        except ValueError:
            msg = "Invalid token format."
            logger.error(msg)
            sys.exit(3)

        vk = get_verify_key()
        ok = vk.verify(token.signature, token.payload)
        if not ok:
            msg = "This is an invalid token; signature check failed."
            logger.error(msg)
            sys.exit(5)

        try:
            data = json.loads(token.payload)
        except ValueError:
            msg = "Invalid token format; cannot interpret payload %r." % token.payload
            logger.error(msg)
            sys.exit(4)

        if not "uid" in data or not "exp" in data:
            msg = "Invalid token format; missing fields from %s." % data
            logger.error(msg)
            sys.exit(6)

        if data["uid"] == -1:
            msg = "This is the sample token. Use your own token."
            logger.error(msg)
            sys.exit(7)

        exp_date = dateutil.parser.parse(data["exp"])
        now = datetime.datetime.today()

        if exp_date < now:
            msg = "This token has expired on %s" % exp_date
            logger.error(msg)
            sys.exit(6)

        o = dict()
        o["uid"] = data["uid"]
        o["expiration"] = data["exp"]
        msg = json.dumps(o)
        print(msg)
        sys.exit(0)

    except Exception as e:
        logger.error(str(e))
        sys.exit(3)


def main_generate(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--uid", type=int, help="ID to sign")
    parser.add_argument("--key", type=str, help="Path to signing key")

    args = parser.parse_args(args=args)

    if args.key is None:
        msg = "Please supply --key "
        raise Exception(msg)
    if args.uid is None:
        msg = "Please supply --uid "
        raise Exception(msg)

    payload: str = json.dumps({"uid": args.uid, "exp": "2021-01-01"})
    payload_bytes = payload.encode()
    with open(args.key, "r") as _:
        pem = _.read()
    sk = SigningKey.from_pem(pem)
    # noinspection PyTypeChecker
    dt = create_signed_token(payload_bytes, sk)  # XXX it says it's a verifying key
    token = dt.as_string()
    print(token)
