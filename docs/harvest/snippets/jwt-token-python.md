# Snippet: JWT Token Creation and Decoding (Python)

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Functions for creating and decoding JSON Web Tokens (JWT) with configurable expiry. Uses HMAC-SHA256 (HS256) signing by default. `create_access_token` encodes a payload with an expiration claim. `decode_token` verifies the signature and expiration, returning the payload or raising an error.

## Dependencies

- `python-jose[cryptography]>=3.3.0`

## Code

```python
"""JWT token creation and decoding."""

from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

# Configuration -- replace with your settings source
SECRET_KEY = "your-secret-key-at-least-32-characters-long"
ALGORITHM = "HS256"
DEFAULT_EXPIRE_MINUTES = 60


class TokenError(Exception):
    """Raised when token creation or decoding fails."""


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT token with an expiration claim.

    Args:
        data: Payload to encode (e.g., {"sub": "user-id", "role": "admin"}).
        expires_delta: Custom expiry duration. Defaults to DEFAULT_EXPIRE_MINUTES.

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=DEFAULT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token.

    Args:
        token: The encoded JWT string.

    Returns:
        Decoded payload dictionary.

    Raises:
        TokenError: If the token is invalid, expired, or has a bad signature.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise TokenError(f"Invalid or expired token: {e}") from e
```

## Usage Example

```python
# Create a token
token = create_access_token(
    data={"sub": "user-42", "role": "admin"},
    expires_delta=timedelta(hours=2),
)
print(token)
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Decode and verify
payload = decode_token(token)
print(payload["sub"])   # "user-42"
print(payload["role"])  # "admin"

# Expired token raises TokenError
try:
    expired_token = create_access_token(
        data={"sub": "user-42"},
        expires_delta=timedelta(seconds=-1),
    )
    decode_token(expired_token)
except TokenError as e:
    print(f"Token error: {e}")

# Integration with FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    try:
        return decode_token(credentials.credentials)
    except TokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
```

## Notes

- The `SECRET_KEY` must be at least 32 characters for HS256. In production, load it from an environment variable or secret manager.
- `algorithms=[ALGORITHM]` in `decode` is a list, not a string. This prevents algorithm confusion attacks where an attacker switches the algorithm.
- The `"sub"` (subject) claim conventionally holds the user identifier. Add custom claims (e.g., `"role"`, `"tenant_id"`) as needed.
- For refresh tokens, create a separate function with a longer `expires_delta` (e.g., 7 days) and a different signing key.
- This snippet uses `python-jose`. The `PyJWT` library (`import jwt`) is an alternative with a slightly different API.
- Never log or expose the decoded token payload in error messages sent to clients.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |
