from datetime import timedelta

from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_and_verify_password_roundtrip():
    password = "my-strong-password"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong-password", hashed) is False


def test_create_and_decode_access_token_roundtrip():
    token = create_access_token({"sub": "alice"}, expires_delta=timedelta(minutes=5))
    data = decode_token(token)

    assert data is not None
    assert data.username == "alice"


def test_decode_token_returns_none_for_invalid_token():
    assert decode_token("not-a-jwt") is None
