#!/usr/bin/env python3
"""Resolve host-local Deliberate Engineering paths without cross-host fallback."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys


SESSION_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def safe_env(name: str, *, required: bool = False) -> str | None:
    value = os.environ.get(name)
    if value is None or value == "":
        if required:
            raise ValueError(f"{name} is unset")
        return None
    if any(character in value for character in ("\r", "\n", "\0")):
        raise ValueError(f"{name} contains a control character")
    return value


def absolute_root(value: str, name: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise ValueError(f"{name} must be an absolute path")
    return path.resolve(strict=False)


def valid_session(value: str | None, name: str) -> str | None:
    if value is not None and not SESSION_ID_RE.fullmatch(value):
        raise ValueError(f"{name} has an invalid session identifier")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", choices=("auto", "claude", "codex"), default="auto")
    args = parser.parse_args()

    try:
        home = absolute_root(safe_env("HOME", required=True) or "", "HOME")
        claude_session = valid_session(
            safe_env("CLAUDE_CODE_SESSION_ID"), "CLAUDE_CODE_SESSION_ID"
        )
        codex_thread = valid_session(safe_env("CODEX_THREAD_ID"), "CODEX_THREAD_ID")

        host = args.host
        if host == "auto":
            identities = [name for name, value in (("claude", claude_session), ("codex", codex_thread)) if value]
            if len(identities) != 1:
                reason = "both host identities are set" if identities else "no host identity is set"
                raise ValueError(f"cannot determine host: {reason}")
            host = identities[0]

        if host == "claude":
            host_root = home / ".claude"
            session_id = claude_session
            transcript_root = host_root / "projects"
            archive_root = None
            thread_store = None
        else:
            configured_codex_home = safe_env("CODEX_HOME")
            host_root = absolute_root(configured_codex_home, "CODEX_HOME") if configured_codex_home else home / ".codex"
            session_id = codex_thread
            transcript_root = host_root / "sessions"
            archive_root = host_root / "archived_sessions"
            candidates = list(host_root.glob("state_*.sqlite"))
            if any(path.is_symlink() for path in candidates):
                raise ValueError("Codex thread store must not be a symlink")
            state_stores = sorted(
                (path for path in candidates if path.is_file()),
                key=lambda path: int(path.stem.removeprefix("state_"))
                if path.stem.removeprefix("state_").isdigit()
                else -1,
            )
            if state_stores:
                resolved_store = state_stores[-1].resolve(strict=True)
                try:
                    resolved_store.relative_to(host_root)
                except ValueError as exc:
                    raise ValueError("Codex thread store escapes CODEX_HOME") from exc
                thread_store = str(resolved_store)
            else:
                thread_store = None

        result = {
            "host": host,
            "data_root": str((host_root / "deliberate-engineering").resolve(strict=False)),
            "transcript_root": str(transcript_root.resolve(strict=False)),
            "archive_root": str(archive_root.resolve(strict=False)) if archive_root else None,
            "session_id": session_id,
            "thread_store": thread_store,
        }
        json.dump(result, sys.stdout, separators=(",", ":"))
        sys.stdout.write("\n")
        return 0
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
