import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from duckietown_tokens import (
    verify_token,
    DuckietownToken,
    get_id_from_token,
    InvalidToken,
)

SAMPLE_TOKEN = (
    "dt1-9Hfd69b5ythetkCiNG12pKDrL987sLJT6KejWP2Eo5QQ"
    "-43dzqWFnWd8KBa1yev1g3UKnzVxZkkTbfWWn6of92V5Bf8qGV24rZHe6r7sueJNtWF"
)
SAMPLE_TOKEN_UID = -1
SAMPLE_TOKEN_EXP = "2018-10-20"


# if False: # this assumes we have the key
#     def tests_private():
#         payload: str = json.dumps({"uid": SAMPLE_TOKEN_UID, "exp": SAMPLE_TOKEN_EXP})
#         # generate a token
#         token = create_signed_token(payload.encode())
#         s = token.as_string()
#         print(s)
#         assert s == SAMPLE_TOKEN, (s, SAMPLE_TOKEN)
#         token2 = token.from_string(s)
#
#         assert verify_token(token2)


def test1():
    token = DuckietownToken.from_string(SAMPLE_TOKEN)
    data = json.loads(token.payload)
    print(data)
    assert data["uid"] == SAMPLE_TOKEN_UID
    assert data["exp"] == SAMPLE_TOKEN_EXP
    verify_token(token)

    seq = SAMPLE_TOKEN[6:8]
    msg_bad = SAMPLE_TOKEN.replace(seq, "XY")
    token = DuckietownToken.from_string(msg_bad)
    try:
        verify_token(token)
    except InvalidToken:
        pass
    else:
        raise Exception(token)

    assert SAMPLE_TOKEN_UID == get_id_from_token(SAMPLE_TOKEN)

    try:
        get_id_from_token(msg_bad)
    except InvalidToken:
        pass
    else:
        raise Exception()


def test_verify1():
    # in this token, uid is string
    invalid = (
        "dt1-wEJsmra4x9TT5bxVq1QYEEGQQW18bje1MvVmg4sDEdUSQjA4k"
        "-43dzqWFnWd8KBa1yev1g3UKnzVxZkkTbfTxZ1tQ5rvJk3Vaa9gHKwhoV38ms4nNR2x"
    )
    token = DuckietownToken.from_string(invalid)
    logger.info(f"token {token}")
    try:
        get_id_from_token(invalid)
    except InvalidToken:
        pass
    else:
        msg = "Expected invalid"
        raise Exception(msg)
