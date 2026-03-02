"""Authentication API endpoints."""

from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from src.api.schemas.auth import LoginSchema, TokenResponseSchema
from src.core.config import settings
from src.core.security import create_access_token, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Default dev password (only used when admin_password_hash is not configured)
_DEFAULT_DEV_PASSWORD = "admin123admin"


@router.post("/login", response_model=TokenResponseSchema)
async def login(payload: LoginSchema):
    """Authenticate admin user and return JWT token."""
    if payload.email != settings.admin_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if settings.admin_password_hash:
        if not verify_password(payload.password, settings.admin_password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
    else:
        # Dev mode: accept default password
        if payload.password != _DEFAULT_DEV_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

    # Create JWT token with admin claims
    token = create_access_token(
        data={
            "sub": payload.email,
            "email": payload.email,
            "role": "admin",
            "tenant_id": "00000000-0000-0000-0000-000000000001",  # Default tenant
        },
        expires_delta=timedelta(minutes=settings.jwt_expire_minutes),
    )

    return TokenResponseSchema(
        access_token=token,
        token_type="bearer",
        expires_in=settings.jwt_expire_minutes * 60,
    )
