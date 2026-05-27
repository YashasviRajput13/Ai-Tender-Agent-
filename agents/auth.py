# auth.py — TenderIQ API Key Authentication
# Drop this file in the same folder as main.py
#
# Usage:
#   from auth import require_api_key
#   @app.get("/api/something")
#   def my_endpoint(api_key: str = Depends(require_api_key)):
#       ...

import os
import secrets
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

# ── Read allowed API keys from environment ──────────────────────
# In your .env (or deployment env vars), set:
#   TENDERIQ_API_KEYS=key1,key2,key3
#
# Generate a strong key with:  python -c "import secrets; print(secrets.token_urlsafe(32))"

_raw = os.getenv("TENDERIQ_API_KEYS", "")
VALID_API_KEYS: set[str] = {k.strip() for k in _raw.split(",") if k.strip()}

if not VALID_API_KEYS:
    import warnings
    warnings.warn(
        "TENDERIQ_API_KEYS is not set — all API requests will be rejected. "
        "Add at least one key to your .env file.",
        stacklevel=2,
    )

# ── Header scheme — clients send:  X-API-Key: <your-key> ────────
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(api_key: str = Security(_api_key_header)) -> str:
    """
    FastAPI dependency — inject with Depends(require_api_key).
    Returns the validated key string, or raises HTTP 401/403.
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Add  X-API-Key: <key>  to your request headers.",
        )
    # Use constant-time comparison to prevent timing attacks
    for valid_key in VALID_API_KEYS:
        if secrets.compare_digest(api_key.strip(), valid_key):
            return api_key
    raise HTTPException(
        status_code=403,
        detail="Invalid API key.",
    )
