"""Unit tests for authentication and security utilities."""

import pytest

from src.core.security import create_access_token, decode_token, hash_password, verify_password


class TestPasswordHashing:
    """Test password hashing and verification."""

    def test_hash_password_returns_hash(self):
        hashed = hash_password("test_password")
        assert hashed != "test_password"
        assert hashed.startswith("$2b$")

    def test_verify_correct_password(self):
        hashed = hash_password("correct_password")
        assert verify_password("correct_password", hashed) is True

    def test_verify_wrong_password(self):
        hashed = hash_password("correct_password")
        assert verify_password("wrong_password", hashed) is False

    def test_different_hashes_for_same_password(self):
        h1 = hash_password("same_password")
        h2 = hash_password("same_password")
        assert h1 != h2  # bcrypt uses random salt


class TestJWT:
    """Test JWT token creation and decoding."""

    def test_create_and_decode_token(self):
        data = {"sub": "user@example.com", "tenant_id": "test-tenant-id"}
        token = create_access_token(data)
        decoded = decode_token(token)
        assert decoded["sub"] == "user@example.com"
        assert decoded["tenant_id"] == "test-tenant-id"

    def test_token_has_expiration(self):
        token = create_access_token({"sub": "test"})
        decoded = decode_token(token)
        assert "exp" in decoded

    def test_invalid_token_raises_error(self):
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc_info:
            decode_token("invalid.token.here")
        assert exc_info.value.status_code == 401
