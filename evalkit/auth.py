import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from anthropic import Anthropic

OAUTH_CLIENT_ID = "9d1c250a-e61b-44d9-88ed-5944d1962f5e"
OAUTH_TOKEN_URL = "https://platform.claude.com/v1/oauth/token"
OAUTH_BETA = "oauth-2025-04-20"
CC_PREFIX = "You are Claude Code, Anthropic's official CLI for Claude."
CREDENTIALS_PATH = Path.home() / ".claude" / ".credentials.json"


@dataclass
class AuthResult:
    token: str
    mode: str
    betas: list[str] = field(default_factory=list)


def resolve_auth() -> AuthResult:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        return AuthResult(token=api_key, mode="api_key")

    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            f"No ANTHROPIC_API_KEY set and {CREDENTIALS_PATH} not found. "
            f"Log in with `claude /login` first, or set ANTHROPIC_API_KEY."
        )

    creds = json.loads(CREDENTIALS_PATH.read_text())
    oauth = creds.get("claudeAiOauth")
    if not oauth or not oauth.get("accessToken"):
        raise ValueError(
            f"{CREDENTIALS_PATH} has no claudeAiOauth.accessToken. "
            f"Log in with `claude /login` first."
        )

    token = oauth["accessToken"]
    expires_at = oauth.get("expiresAt", 0)

    if expires_at and time.time() * 1000 >= expires_at - 60000:
        refresh = oauth.get("refreshToken")
        if refresh:
            token = _refresh_token(refresh, creds)

    return AuthResult(token=token, mode="oauth", betas=[OAUTH_BETA])


def _refresh_token(refresh_token: str, creds: dict) -> str:
    import httpx
    try:
        resp = httpx.post(
            OAUTH_TOKEN_URL,
            json={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": OAUTH_CLIENT_ID,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        new_token = data["access_token"]

        creds["claudeAiOauth"] = {
            **creds.get("claudeAiOauth", {}),
            "accessToken": new_token,
            "refreshToken": data.get("refresh_token", refresh_token),
            "expiresAt": int(time.time() * 1000) + (data.get("expires_in", 0) * 1000),
        }
        CREDENTIALS_PATH.write_text(json.dumps(creds, indent=2))
        CREDENTIALS_PATH.chmod(0o600)
        return new_token
    except Exception:
        return creds["claudeAiOauth"]["accessToken"]


def make_client(auth: AuthResult) -> Anthropic:
    if auth.mode == "oauth":
        return Anthropic(
            auth_token=auth.token,
            default_headers={
                "anthropic-beta": OAUTH_BETA,
                "x-app": "cli",
                "User-Agent": "claude-cli/evalkit",
            },
        )
    return Anthropic(api_key=auth.token)


def system_prefix(auth: AuthResult) -> Optional[str]:
    if auth.mode == "oauth":
        return CC_PREFIX
    return None


_global_auth: Optional[AuthResult] = None
_global_client: Optional[Anthropic] = None


def get_client() -> tuple[Anthropic, Optional[str]]:
    global _global_auth, _global_client
    if _global_client is not None and _global_auth is not None:
        return _global_client, system_prefix(_global_auth)
    _global_auth = resolve_auth()
    _global_client = make_client(_global_auth)
    return _global_client, system_prefix(_global_auth)