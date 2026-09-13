#!/usr/bin/env python3
"""Select bounded Codex root-user rollout lineages from a trusted thread store."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys


class SelectionError(ValueError):
    pass


def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def managed_roots(transcript_root: Path, archive_root: Path) -> tuple[Path, ...]:
    roots: list[Path] = []
    for path, label, required in (
        (transcript_root, "transcript root", True),
        (archive_root, "archive root", False),
    ):
        if not path.is_absolute():
            raise SelectionError(f"{label} must be absolute")
        try:
            resolved = path.resolve(strict=required)
        except OSError as exc:
            raise SelectionError(str(exc)) from exc
        if resolved.exists() and not resolved.is_dir():
            raise SelectionError(f"{label} is not a directory")
        roots.append(resolved)
    return tuple(roots)


def read_first_line(path: Path) -> bytes:
    if not path.name.endswith(".zst"):
        try:
            with path.open("rb") as source:
                return source.readline()
        except OSError as exc:
            raise SelectionError(str(exc)) from exc
    zstd = shutil.which("zstd")
    if zstd is None:
        raise SelectionError("zstd is required to read a compressed Codex rollout")
    try:
        process = subprocess.Popen(
            [zstd, "-q", "-dc", "--", str(path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert process.stdout is not None
        line = process.stdout.readline()
        process.stdout.close()
        process.terminate()
        process.wait(timeout=5)
        return line
    except (OSError, subprocess.SubprocessError) as exc:
        raise SelectionError(f"cannot read compressed rollout {path}: {exc}") from exc


def load_meta(path: Path) -> dict:
    try:
        record = json.loads(read_first_line(path))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SelectionError(f"invalid session metadata in {path}: {exc}") from exc
    if not isinstance(record, dict) or record.get("type") != "session_meta":
        raise SelectionError(f"rollout does not begin with session_meta: {path}")
    payload = record.get("payload")
    if not isinstance(payload, dict):
        raise SelectionError(f"rollout has invalid session_meta payload: {path}")
    return payload


def is_root_user(meta: dict) -> bool:
    source = meta.get("source")
    return (
        meta.get("parent_thread_id") is None
        and meta.get("thread_source") in (None, "user")
        and isinstance(source, str)
        and not source.startswith(("internal_", "subagent_"))
    )


def validate_existing(path: Path, roots: tuple[Path, ...]) -> Path | None:
    if path.is_symlink() or not path.is_file():
        return None
    try:
        resolved = path.resolve(strict=True)
    except OSError:
        return None
    if not any(inside(resolved, root) for root in roots):
        return None
    return resolved


def existing_representation(path: Path, roots: tuple[Path, ...]) -> Path | None:
    if path.name.endswith(".jsonl.zst"):
        candidates = (path.with_name(path.name.removesuffix(".zst")), path)
    else:
        candidates = (path, path.with_name(path.name + ".zst"))
    for candidate in candidates:
        resolved = validate_existing(candidate, roots)
        if resolved is not None:
            return resolved
    return None


def rollout_id_from_name(path: Path) -> str | None:
    name = path.name.removesuffix(".zst")
    if not name.startswith("rollout-") or not name.endswith(".jsonl"):
        return None
    core = name.removesuffix(".jsonl")
    if len(core) < 57 or core[27:28] != "-":
        return None
    return core[28:].rsplit("_", 1)[-1]


def find_rollout(rollout_id: str, roots: tuple[Path, ...]) -> Path:
    matches: dict[str, Path] = {}
    for root in roots:
        if not root.is_dir():
            continue
        for pattern in (f"*{rollout_id}.jsonl", f"*{rollout_id}.jsonl.zst"):
            for candidate in root.rglob(pattern):
                if rollout_id_from_name(candidate) != rollout_id:
                    continue
                resolved = validate_existing(candidate, roots)
                if resolved is None:
                    continue
                logical = str(resolved).removesuffix(".zst")
                previous = matches.get(logical)
                if previous is None or previous.name.endswith(".zst"):
                    matches[logical] = resolved
    if len(matches) != 1:
        raise SelectionError(
            f"expected one managed rollout for lineage id {rollout_id}, found {len(matches)}"
        )
    return next(iter(matches.values()))


def history_base(meta: dict, path: Path) -> dict | None:
    value = meta.get("history_base")
    if value is None:
        return None
    if not isinstance(value, dict):
        raise SelectionError(f"history_base is malformed in {path}")
    rollout_id = value.get("thread_id")
    end = value.get("end_ordinal_exclusive")
    offset = value.get("end_byte_offset")
    if not isinstance(rollout_id, str) or not isinstance(end, int) or end < 1:
        raise SelectionError(f"history_base has an invalid rollout id or ordinal in {path}")
    if not isinstance(offset, int) or offset < 0:
        raise SelectionError(f"history_base has an invalid byte offset in {path}")
    return value


def build_lineage(thread_id: str, head: Path, roots: tuple[Path, ...]) -> dict:
    segments: list[dict] = []
    seen: set[str] = set()
    path = head
    end: int | None = None
    end_byte_offset: int | None = None
    expected_rollout_id: str | None = None
    first = True
    while True:
        meta = load_meta(path)
        owner_thread_id = meta.get("id")
        if not isinstance(owner_thread_id, str):
            raise SelectionError(f"rollout lineage has no valid owner in {path}")
        if first and owner_thread_id != thread_id:
            raise SelectionError(f"active rollout does not belong to requested thread {thread_id}")
        if not is_root_user(meta):
            raise SelectionError(f"rollout lineage for {thread_id} is not operator-owned root history")
        rollout_id = rollout_id_from_name(path) or (thread_id if first else None)
        if rollout_id is None or (expected_rollout_id is not None and rollout_id != expected_rollout_id):
            raise SelectionError(f"rollout filename does not match lineage id in {path}")
        if rollout_id in seen:
            raise SelectionError(f"cycle detected in rollout lineage for {thread_id}")
        seen.add(rollout_id)
        base = history_base(meta, path)
        if base is not None and meta.get("history_mode") not in (None, "paginated"):
            raise SelectionError(f"history_base appears on a non-paginated rollout: {path}")
        start = base["end_ordinal_exclusive"] + 1 if base is not None else 1
        segments.append(
            {
                "rollout_id": rollout_id,
                "owner_thread_id": owner_thread_id,
                "path": str(path),
                "start_ordinal": start,
                "end_ordinal_exclusive": end,
                "end_byte_offset": end_byte_offset,
            }
        )
        if base is None:
            break
        expected_rollout_id = base["thread_id"]
        end = base["end_ordinal_exclusive"]
        end_byte_offset = base["end_byte_offset"]
        path = find_rollout(expected_rollout_id, roots)
        first = False
    segments.reverse()
    return {"session_id": thread_id, "segments": segments}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript-root", required=True, type=Path)
    parser.add_argument("--archive-root", required=True, type=Path)
    parser.add_argument("--thread-store", required=True, type=Path)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--session-id")
    scope.add_argument("--project-root", type=Path)
    args = parser.parse_args()

    try:
        roots = managed_roots(args.transcript_root.expanduser(), args.archive_root.expanduser())
        store = args.thread_store.expanduser()
        if not store.is_absolute():
            raise SelectionError("thread store must be absolute")
        if store.is_symlink() or not store.is_file():
            raise SelectionError("thread store must be a regular non-symlink file")
        store = store.resolve(strict=True)
        codex_home = roots[0].parent
        if roots[1].parent != codex_home or store.parent != codex_home:
            raise SelectionError("transcript roots and thread store must belong to the same Codex home")

        project_root = args.project_root
        if project_root is not None:
            if not project_root.is_absolute():
                raise SelectionError("project root must be absolute")
            project_root = project_root.resolve(strict=False)

        where = "id = ?" if args.session_id is not None else "cwd = ?"
        parameter = args.session_id if args.session_id is not None else str(project_root)
        connection = sqlite3.connect(f"{store.as_uri()}?mode=ro", uri=True)
        try:
            rows = connection.execute(
                f"SELECT id, rollout_path, source, thread_source FROM threads WHERE {where}",
                (parameter,),
            ).fetchall()
        finally:
            connection.close()

        lineages: list[dict] = []
        for thread_id, rollout_path, source, thread_source in rows:
            if not isinstance(thread_id, str) or not isinstance(rollout_path, str):
                raise SelectionError("thread store returned an invalid id or rollout path")
            if thread_source not in (None, "user") or not isinstance(source, str):
                continue
            raw = Path(rollout_path)
            if not raw.is_absolute():
                raise SelectionError(f"thread store returned a relative rollout path for {thread_id}")
            head = existing_representation(raw, roots)
            if head is None:
                raise SelectionError(f"managed rollout is missing or unreadable for {thread_id}")
            meta = load_meta(head)
            if meta.get("id") != thread_id or not is_root_user(meta):
                raise SelectionError(f"thread store and rollout metadata disagree for {thread_id}")
            if project_root is not None:
                cwd = meta.get("cwd")
                if not isinstance(cwd, str) or Path(cwd).resolve(strict=False) != project_root:
                    continue
            lineages.append(build_lineage(thread_id, head, roots))
        lineages.sort(key=lambda value: value["session_id"])
        json.dump(lineages, sys.stdout, separators=(",", ":"))
        sys.stdout.write("\n")
        return 0
    except (OSError, sqlite3.Error, SelectionError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
