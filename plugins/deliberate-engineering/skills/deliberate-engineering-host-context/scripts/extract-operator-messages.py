#!/usr/bin/env python3
"""Extract NUL-delimited operator messages from trusted host transcripts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


CLAUDE_WRAPPER_RE = re.compile(
    r"<(command-name|command-message|command-args|local-command-stdout|system-reminder)>.*?</\1>",
    re.DOTALL,
)
class TranscriptError(ValueError):
    pass


def inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_root(root: Path, label: str, *, required: bool) -> Path:
    if not root.is_absolute():
        raise TranscriptError(f"{label} must be absolute")
    try:
        resolved = root.resolve(strict=required)
    except OSError as exc:
        raise TranscriptError(str(exc)) from exc
    if resolved.exists() and not resolved.is_dir():
        raise TranscriptError(f"{label} is not a directory")
    return resolved


def validate_transcript(path: Path, roots: tuple[Path, ...]) -> Path:
    if not path.is_absolute():
        raise TranscriptError("transcript path must be absolute")
    try:
        resolved_path = path.resolve(strict=True)
    except OSError as exc:
        raise TranscriptError(str(exc)) from exc
    if path.is_symlink() or not resolved_path.is_file() or not any(
        inside(resolved_path, root) for root in roots
    ):
        raise TranscriptError("transcript must be a regular non-symlink file below a managed transcript root")
    return resolved_path


def text_blocks(content: object, block_type: str, line_number: int) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        raise TranscriptError(f"line {line_number}: message content must be text or a list")
    kept: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            raise TranscriptError(f"line {line_number}: message block must be an object")
        if block.get("type") == block_type:
            text = block.get("text")
            if not isinstance(text, str):
                raise TranscriptError(f"line {line_number}: text block has a non-string value")
            kept.append(text)
    return "\n".join(kept)


def extract_claude(record: dict, line_number: int) -> str | None:
    if record.get("type") != "user" or record.get("isMeta") or record.get("isSidechain"):
        return None
    origin = record.get("origin")
    if isinstance(origin, dict) and origin.get("kind") not in (None, "human"):
        return None
    message = record.get("message")
    if not isinstance(message, dict):
        raise TranscriptError(f"line {line_number}: Claude user record has no message object")
    content = message.get("content")
    if isinstance(content, list) and any(
        isinstance(block, dict) and block.get("type") == "tool_result" for block in content
    ):
        return None
    text = CLAUDE_WRAPPER_RE.sub("", text_blocks(content, "text", line_number)).strip()
    return text or None


def extract_codex(record: dict, line_number: int) -> str | None:
    if record.get("type") != "response_item":
        return None
    payload = record.get("payload")
    if not isinstance(payload, dict) or payload.get("type") != "message" or payload.get("role") != "user":
        return None
    content = payload.get("content")
    if not isinstance(content, list) or not all(isinstance(block, dict) for block in content):
        raise TranscriptError(f"line {line_number}: Codex user message has invalid content")

    metadata = payload.get("internal_chat_message_metadata_passthrough")
    if isinstance(metadata, dict):
        kinds = metadata.get("content_item_kinds")
        if not isinstance(kinds, list) or len(kinds) != len(content) or not all(isinstance(kind, str) for kind in kinds):
            raise TranscriptError(f"line {line_number}: Codex content provenance is malformed")
        kept: list[str] = []
        for block, kind in zip(content, kinds, strict=True):
            if kind != "user.text":
                continue
            if block.get("type") != "input_text" or not isinstance(block.get("text"), str):
                raise TranscriptError(f"line {line_number}: user.text provenance does not match an input_text block")
            text = block["text"].strip()
            if text:
                kept.append(text)
        result = "\n".join(kept).strip()
        return result or None

    raise TranscriptError(
        f"line {line_number}: Codex user text has no structural provenance; refusing partial extraction"
    )


def validate_codex_meta(record: dict, session_id: str) -> dict:
    if record.get("type") != "session_meta" or not isinstance(record.get("payload"), dict):
        raise TranscriptError("line 1: Codex transcript must begin with session_meta")
    meta = record["payload"]
    source = meta.get("source")
    if meta.get("id") != session_id:
        raise TranscriptError("line 1: Codex transcript does not match the requested thread")
    if meta.get("parent_thread_id") is not None or meta.get("thread_source") not in (None, "user"):
        raise TranscriptError("line 1: Codex transcript is not an operator-owned root thread")
    if not isinstance(source, str) or source.startswith(("internal_", "subagent_")):
        raise TranscriptError("line 1: Codex transcript has a non-root session source")
    return meta


def read_transcript_bytes(path: Path) -> bytes:
    if not path.name.endswith(".zst"):
        try:
            return path.read_bytes()
        except OSError as exc:
            raise TranscriptError(str(exc)) from exc
    zstd = shutil.which("zstd")
    if zstd is None:
        raise TranscriptError("zstd is required to read a compressed Codex rollout")
    try:
        result = subprocess.run(
            [zstd, "-q", "-dc", "--", str(path)], capture_output=True, check=False
        )
    except OSError as exc:
        raise TranscriptError(f"cannot read compressed rollout {path}: {exc}") from exc
    if result.returncode != 0:
        detail = result.stderr.decode(errors="replace").strip()
        raise TranscriptError(f"cannot read compressed rollout {path}: {detail}")
    return result.stdout


def load_records(path: Path, end_byte_offset: int | None = None) -> list[tuple[int, dict]]:
    raw = read_transcript_bytes(path)
    if end_byte_offset is not None:
        if end_byte_offset <= 0 or end_byte_offset > len(raw):
            raise TranscriptError(f"lineage byte offset is outside rollout {path}")
        if raw[end_byte_offset - 1 : end_byte_offset] != b"\n":
            raise TranscriptError(f"lineage byte offset is not a JSONL record boundary in {path}")
        raw = raw[:end_byte_offset]
    records: list[tuple[int, dict]] = []
    lines = raw.splitlines(keepends=True)
    for index, raw_line in enumerate(lines, start=1):
        if not raw_line.strip():
            continue
        try:
            record = json.loads(raw_line)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            is_unterminated_tail = index == len(lines) and not raw_line.endswith((b"\n", b"\r"))
            if is_unterminated_tail and not path.name.endswith(".zst"):
                break
            raise TranscriptError(f"line {index}: invalid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise TranscriptError(f"line {index}: transcript record must be an object")
        records.append((index, record))
    return records


def collect(
    records: list[tuple[int, dict]],
    extractor,
    *,
    start: int | None = None,
    end: int | None = None,
    rollout_id: str | None = None,
    emitted_records: set[tuple[str, int]] | None = None,
) -> list[str]:
    previous_ordinal: int | None = None
    messages: list[str] = []
    for line_number, record in records:
        if start is not None:
            ordinal = record.get("ordinal")
            if not isinstance(ordinal, int) or ordinal < 0:
                raise TranscriptError(f"line {line_number}: paginated Codex record has no valid ordinal")
            if previous_ordinal is not None and ordinal <= previous_ordinal:
                raise TranscriptError(f"line {line_number}: Codex rollout ordinals are not strictly increasing")
            previous_ordinal = ordinal
            if ordinal < start or (end is not None and ordinal >= end):
                continue
        message = extractor(record, line_number)
        if message:
            if emitted_records is not None:
                if rollout_id is None or previous_ordinal is None:
                    raise TranscriptError("cannot deduplicate a Codex record without rollout identity and ordinal")
                record_key = (rollout_id, previous_ordinal)
                if record_key in emitted_records:
                    continue
                emitted_records.add(record_key)
            messages.append(message)
    if end is not None and previous_ordinal != end - 1:
        raise TranscriptError("lineage ordinal cutoff does not match its byte-offset boundary")
    return messages


def write_messages(messages: list[str]) -> None:
    encoded: list[bytes] = []
    for message in messages:
        if "\0" in message:
            raise TranscriptError("operator message contains an embedded NUL byte")
        try:
            encoded.append(message.encode())
        except UnicodeEncodeError as exc:
            raise TranscriptError(f"operator message is not valid UTF-8: {exc}") from exc
    if encoded:
        sys.stdout.buffer.write(b"\0".join(encoded) + b"\0")


def load_lineage_manifest(path: Path) -> list[dict]:
    if not path.is_absolute() or path.is_symlink() or not path.is_file():
        raise TranscriptError("lineage manifest must be an absolute regular non-symlink file")
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise TranscriptError(f"invalid lineage manifest: {exc}") from exc
    if not isinstance(value, list) or not all(isinstance(entry, dict) for entry in value):
        raise TranscriptError("lineage manifest must contain a list of thread objects")
    return value


def collect_lineages(entries: list[dict], roots: tuple[Path, ...], requested_session: str | None) -> list[str]:
    if requested_session is not None:
        entries = [entry for entry in entries if entry.get("session_id") == requested_session]
        if len(entries) != 1:
            raise TranscriptError("lineage manifest must contain exactly the requested session")
    messages: list[str] = []
    emitted_records: set[tuple[str, int]] | None = set() if requested_session is None else None
    for entry in entries:
        session_id = entry.get("session_id")
        segments = entry.get("segments")
        if not isinstance(session_id, str) or not isinstance(segments, list) or not segments:
            raise TranscriptError("lineage entry has invalid session_id or segments")
        prior_rollout: str | None = None
        prior_end: int | None = None
        prior_end_byte_offset: int | None = None
        seen: set[str] = set()
        for index, segment in enumerate(segments):
            if not isinstance(segment, dict):
                raise TranscriptError("lineage segment must be an object")
            rollout_id = segment.get("rollout_id")
            owner_thread_id = segment.get("owner_thread_id")
            raw_path = segment.get("path")
            start = segment.get("start_ordinal")
            end = segment.get("end_ordinal_exclusive")
            end_byte_offset = segment.get("end_byte_offset")
            if not isinstance(rollout_id, str) or rollout_id in seen:
                raise TranscriptError("lineage segment has an invalid or repeated rollout_id")
            if not isinstance(owner_thread_id, str):
                raise TranscriptError("lineage segment has no valid owner_thread_id")
            if not isinstance(raw_path, str) or not isinstance(start, int) or start < 1:
                raise TranscriptError("lineage segment has an invalid path or start ordinal")
            if end is not None and (not isinstance(end, int) or end < start):
                raise TranscriptError("lineage segment has an invalid end ordinal")
            if (end is None) != (end_byte_offset is None) or (
                end_byte_offset is not None
                and (not isinstance(end_byte_offset, int) or end_byte_offset <= 0)
            ):
                raise TranscriptError("lineage segment has an invalid byte-offset boundary")
            path = validate_transcript(Path(raw_path), roots)
            records = load_records(path, end_byte_offset)
            if not records:
                raise TranscriptError(f"Codex transcript is empty: {path}")
            meta = validate_codex_meta(records[0][1], owner_thread_id)
            if index == len(segments) - 1 and owner_thread_id != session_id:
                raise TranscriptError("active lineage segment does not belong to the requested session")
            base = meta.get("history_base")
            expected_start = 1
            if base is not None:
                if not isinstance(base, dict):
                    raise TranscriptError(f"line 1: malformed history_base in {path}")
                base_id = base.get("thread_id")
                base_end = base.get("end_ordinal_exclusive")
                base_offset = base.get("end_byte_offset")
                if not isinstance(base_id, str) or not isinstance(base_end, int) or not isinstance(base_offset, int):
                    raise TranscriptError(f"line 1: malformed history_base in {path}")
                expected_start = base_end + 1
                if prior_rollout != base_id or prior_end != base_end or prior_end_byte_offset != base_offset:
                    raise TranscriptError("lineage manifest does not match Codex history_base pointers")
            elif index != 0:
                raise TranscriptError("non-initial lineage segment has no history_base")
            if start != expected_start:
                raise TranscriptError("lineage segment start does not match its history_base")
            seen.add(rollout_id)
            messages.extend(
                collect(
                    records,
                    extract_codex,
                    start=start,
                    end=end,
                    rollout_id=rollout_id,
                    emitted_records=emitted_records,
                )
            )
            prior_rollout = rollout_id
            prior_end = end
            prior_end_byte_offset = end_byte_offset
    return messages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, choices=("claude", "codex"))
    parser.add_argument("--transcript-root", required=True, type=Path)
    parser.add_argument("--archive-root", type=Path)
    parser.add_argument("--session-id")
    parser.add_argument("--lineage-manifest", type=Path)
    parser.add_argument("transcript", nargs="?", type=Path)
    args = parser.parse_args()

    try:
        transcript_root = resolve_root(args.transcript_root, "transcript root", required=True)
        roots = (transcript_root,)
        if args.archive_root is not None:
            roots += (resolve_root(args.archive_root, "archive root", required=False),)

        if args.lineage_manifest is not None:
            if args.host != "codex" or args.transcript is not None:
                raise TranscriptError("lineage manifests are only valid for Codex without a transcript argument")
            messages = collect_lineages(load_lineage_manifest(args.lineage_manifest), roots, args.session_id)
            write_messages(messages)
            return 0

        if args.transcript is None or args.session_id is None:
            raise TranscriptError("a transcript and session id are required without a lineage manifest")
        transcript = validate_transcript(args.transcript, roots)
        if args.host == "claude" and transcript.name != f"{args.session_id}.jsonl":
            raise TranscriptError("Claude transcript filename does not match the requested session")
        records = load_records(transcript)
        if args.host == "codex":
            if not records:
                raise TranscriptError("Codex transcript is empty")
            validate_codex_meta(records[0][1], args.session_id)
        messages = collect(records, extract_claude if args.host == "claude" else extract_codex)
        write_messages(messages)
        return 0
    except TranscriptError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
