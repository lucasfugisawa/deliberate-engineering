#!/usr/bin/env python3
"""Behavioral controls for the multi-host plugin contract."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts" / "check-host-compatibility.py"
HOST_SCRIPTS = ROOT / "plugins/deliberate-engineering/skills/deliberate-engineering-host-context/scripts"
RESOLVER = HOST_SCRIPTS / "resolve-host-context.py"
SELECTOR = HOST_SCRIPTS / "select-codex-rollouts.py"
EXTRACTOR = HOST_SCRIPTS / "extract-operator-messages.py"


def load_checker():
    if not CHECKER_PATH.is_file():
        raise AssertionError(f"missing repository validator: {CHECKER_PATH.relative_to(ROOT)}")
    spec = importlib.util.spec_from_file_location("host_compatibility", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load host compatibility validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def codex_meta(
    session_id: str,
    *,
    cwd: str = "/repo",
    source: object = "vscode",
    thread_source: str | None = "user",
    parent: str | None = None,
    history_base: dict | None = None,
    ordinal: int | None = None,
) -> dict:
    record = {
        "type": "session_meta",
        "payload": {
            "id": session_id,
            "cwd": cwd,
            "timestamp": "2026-09-12T12:00:00Z",
            "source": source,
            "thread_source": thread_source,
            "parent_thread_id": parent,
            "history_mode": "paginated" if history_base is not None or ordinal is not None else None,
            "history_base": history_base,
        },
    }
    if ordinal is not None:
        record["ordinal"] = ordinal
    return record


def codex_message(text: str, *, proven: bool = True, current_envelope: bool = True, ordinal: int | None = None) -> dict:
    payload: dict = {
        "type": "message",
        "role": "user",
        "content": [{"type": "input_text", "text": text}],
    }
    if proven:
        payload["internal_chat_message_metadata_passthrough"] = {
            "content_item_kinds": ["user.text"]
        }
    if current_envelope:
        payload["id"] = "message-id"
    record = {"type": "response_item", "payload": payload}
    if ordinal is not None:
        record["ordinal"] = ordinal
    return record


class RepositoryContractTests(unittest.TestCase):
    def test_repository_satisfies_multi_host_contract(self) -> None:
        checker = load_checker()
        self.assertEqual(checker.check_repository(ROOT), [])

    def test_repository_check_rejects_host_version_skew(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            manifest_path = copy / "plugins/deliberate-engineering/.codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["version"] = "999.0.0"
            manifest_path.write_text(json.dumps(manifest))
            errors = checker.check_repository(copy)
        self.assertTrue(any("versions must be in lockstep" in error for error in errors), errors)

    def test_repository_check_rejects_codex_adapter_claude_dependency(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            manifest_path = copy / "plugins/deliberate-engineering/.codex-plugin/plugin.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["homepage"] = "~/.claude/deliberate-engineering"
            manifest_path.write_text(json.dumps(manifest))
            errors = checker.check_repository(copy)
        self.assertTrue(any("depends on Claude token" in error for error in errors), errors)

    def test_repository_check_rejects_claude_command_syntax_in_shared_methodology(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            shared = copy / "plugins/deliberate-engineering/skills/deliberate-engineering-router/SKILL.md"
            shared.write_text(shared.read_text() + "\nUse `/deliberate-engineering:start`.\n")
            errors = checker.check_repository(copy)
        self.assertTrue(any("shared methodology contains host-specific token" in error for error in errors), errors)

    def test_repository_check_rejects_legacy_codex_argument_template(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            adapter = copy / "plugins/deliberate-engineering/codex/commands/plan/SKILL.md"
            adapter.write_text(adapter.read_text() + "\n$ARGUMENTS\n")
            errors = checker.check_repository(copy)
        self.assertTrue(any("unsupported template arguments" in error for error in errors), errors)

    def test_repository_check_rejects_swapped_codex_command_targets(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            plan = copy / "plugins/deliberate-engineering/codex/commands/plan/SKILL.md"
            review = copy / "plugins/deliberate-engineering/codex/commands/review/SKILL.md"
            plan_body = plan.read_text()
            review_body = review.read_text()
            plan.write_text(plan_body.replace("planning-strategy-selector", "review-strategy-selector"))
            review.write_text(review_body.replace("review-strategy-selector", "planning-strategy-selector"))
            errors = checker.check_repository(copy)
        self.assertTrue(any("dispatch target mismatch" in error for error in errors), errors)

    def test_repository_check_rejects_weakened_private_file_contract(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            contract = copy / "plugins/deliberate-engineering/skills/deliberate-engineering-host-context/SKILL.md"
            contract.write_text(contract.read_text().replace("0600", "default file mode"))
            errors = checker.check_repository(copy)
        self.assertTrue(any("private-file contract" in error for error in errors), errors)

    def test_repository_check_rejects_manifest_exclusion_from_version_gate(self) -> None:
        checker = load_checker()
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
            gate = copy / ".github/workflows/version-gate.yml"
            gate.write_text(
                gate.read_text().replace(
                    'git diff --name-only "$base" HEAD -- plugins/deliberate-engineering/ .claude-plugin/marketplace.json .agents/plugins/marketplace.json',
                    'git diff --name-only "$base" HEAD -- plugins/other/',
                )
            )
            errors = checker.check_repository(copy)
        self.assertTrue(any("version gate" in error for error in errors), errors)


class HostResolverTests(unittest.TestCase):
    def run_resolver(self, host: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        clean_env = {
            "HOME": env["HOME"],
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            **{key: value for key, value in env.items() if key != "HOME"},
        }
        return subprocess.run(
            [sys.executable, str(RESOLVER), "--host", host],
            text=True,
            capture_output=True,
            env=clean_env,
            check=False,
        )

    def test_claude_and_codex_resolve_independent_roots(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            claude = self.run_resolver("claude", {"HOME": home, "CLAUDE_CODE_SESSION_ID": "claude-session"})
            codex = self.run_resolver("codex", {"HOME": home, "CODEX_THREAD_ID": "codex-thread"})
        self.assertEqual(claude.returncode, 0, claude.stderr)
        self.assertEqual(codex.returncode, 0, codex.stderr)
        claude_values = json.loads(claude.stdout)
        codex_values = json.loads(codex.stdout)
        canonical_home = str(Path(home).resolve())
        self.assertEqual(claude_values["data_root"], f"{canonical_home}/.claude/deliberate-engineering")
        self.assertEqual(codex_values["data_root"], f"{canonical_home}/.codex/deliberate-engineering")
        self.assertNotIn(".claude", codex_values["data_root"])
        self.assertEqual(claude_values["session_id"], "claude-session")
        self.assertEqual(codex_values["session_id"], "codex-thread")

    def test_explicit_host_does_not_require_session_identity(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            result = self.run_resolver("codex", {"HOME": home})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNone(json.loads(result.stdout)["session_id"])

    def test_codex_honors_absolute_codex_home_and_discovers_thread_store(self) -> None:
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as codex_home:
            store = Path(codex_home) / "state_5.sqlite"
            store.touch()
            result = self.run_resolver("codex", {"HOME": home, "CODEX_HOME": codex_home, "CODEX_THREAD_ID": "thread"})
        self.assertEqual(result.returncode, 0, result.stderr)
        values = json.loads(result.stdout)
        canonical_codex_home = str(Path(codex_home).resolve())
        self.assertEqual(values["data_root"], f"{canonical_codex_home}/deliberate-engineering")
        self.assertEqual(values["transcript_root"], f"{canonical_codex_home}/sessions")
        self.assertEqual(values["archive_root"], f"{canonical_codex_home}/archived_sessions")
        self.assertEqual(values["thread_store"], str(store.resolve()))

    def test_codex_rejects_relative_home_and_invalid_session_identity(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            relative = self.run_resolver("codex", {"HOME": home, "CODEX_HOME": ".codex"})
            newline = self.run_resolver("codex", {"HOME": home, "CODEX_THREAD_ID": "valid\nforged"})
        self.assertNotEqual(relative.returncode, 0)
        self.assertIn("absolute path", relative.stderr)
        self.assertNotEqual(newline.returncode, 0)
        self.assertIn("control character", newline.stderr)

    def test_codex_rejects_thread_store_symlink_escaping_codex_home(self) -> None:
        with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as codex_home:
            outside = Path(home) / "outside.sqlite"
            outside.touch()
            (Path(codex_home) / "state_9.sqlite").symlink_to(outside)
            result = self.run_resolver("codex", {"HOME": home, "CODEX_HOME": codex_home})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must not be a symlink", result.stderr)

    def test_auto_rejects_ambiguous_or_missing_host_identity(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            missing = self.run_resolver("auto", {"HOME": home})
            ambiguous = self.run_resolver("auto", {"HOME": home, "CLAUDE_CODE_SESSION_ID": "claude", "CODEX_THREAD_ID": "codex"})
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("cannot determine host", missing.stderr)
        self.assertNotEqual(ambiguous.returncode, 0)
        self.assertIn("cannot determine host", ambiguous.stderr)


class CodexRolloutSelectorTests(unittest.TestCase):
    def write_store(self, path: Path, rows: list[tuple[str, str, str, str | None, str]]) -> None:
        connection = sqlite3.connect(path)
        connection.execute("CREATE TABLE threads (id TEXT, rollout_path TEXT, source TEXT, thread_source TEXT, cwd TEXT)")
        connection.executemany("INSERT INTO threads VALUES (?, ?, ?, ?, ?)", rows)
        connection.commit()
        connection.close()

    def write_rollout(self, path: Path, *records: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(record) + "\n" for record in records))

    def run_selector(self, base: Path, *scope: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SELECTOR),
                "--transcript-root",
                str(base / "sessions"),
                "--archive-root",
                str(base / "archived_sessions"),
                "--thread-store",
                str(base / "state_5.sqlite"),
                *scope,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_selector_uses_active_store_pointer_after_revert(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sessions = base / "sessions"
            stale = sessions / "rollout-thread.jsonl"
            active = sessions / "rollout-thread_revert.jsonl"
            self.write_rollout(stale, codex_meta("thread"))
            self.write_rollout(active, codex_meta("thread"))
            store = base / "state_5.sqlite"
            self.write_store(store, [("thread", str(active), "vscode", "user", "/repo")])
            result = self.run_selector(base, "--session-id", "thread")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            [{"session_id": "thread", "segments": [{"rollout_id": "thread", "owner_thread_id": "thread", "path": str(active.resolve()), "start_ordinal": 1, "end_ordinal_exclusive": None, "end_byte_offset": None}]}],
        )

    def test_selector_encodes_reserved_characters_in_state_store_uri(self) -> None:
        for reserved in ("?", "#"):
            with self.subTest(reserved=reserved), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp) / f"codex{reserved}home"
                rollout = base / "sessions" / "rollout-thread.jsonl"
                self.write_rollout(rollout, codex_meta("thread"))
                self.write_store(
                    base / "state_5.sqlite",
                    [("thread", str(rollout), "vscode", "user", "/repo")],
                )
                result = self.run_selector(base, "--session-id", "thread")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)[0]["session_id"], "thread")

    def test_project_selector_excludes_subagents_and_guardians(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sessions = base / "sessions"
            root = sessions / "root.jsonl"
            child = sessions / "child.jsonl"
            guardian = sessions / "guardian.jsonl"
            self.write_rollout(root, codex_meta("root"))
            self.write_rollout(child, codex_meta("child", source={"subagent": "review"}, thread_source="subagent", parent="root"))
            self.write_rollout(guardian, codex_meta("guardian", source={"subagent": "guardian"}, thread_source="guardian_review", parent="root"))
            store = base / "state_5.sqlite"
            self.write_store(store, [
                ("root", str(root), "vscode", "user", "/repo"),
                ("child", str(child), "subagent_review", "subagent", "/repo"),
                ("guardian", str(guardian), "subagent_guardian", "guardian_review", "/repo"),
            ])
            result = self.run_selector(base, "--project-root", "/repo")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            [{"session_id": "root", "segments": [{"rollout_id": "root", "owner_thread_id": "root", "path": str(root.resolve()), "start_ordinal": 1, "end_ordinal_exclusive": None, "end_byte_offset": None}]}],
        )

    def test_selector_and_extractor_follow_bounded_user_fork_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sessions = base / "sessions"
            parent_id = "44444444-4444-4444-8444-444444444444"
            child_id = "55555555-5555-4555-8555-555555555555"
            parent = sessions / f"rollout-2026-09-12T12-00-00-{parent_id}.jsonl"
            child = sessions / f"rollout-2026-09-12T13-00-00-{child_id}.jsonl"
            parent_meta = codex_meta(parent_id, ordinal=0)
            inherited = codex_message("inherited parent message", ordinal=2)
            end_offset = len((json.dumps(parent_meta) + "\n" + json.dumps(inherited) + "\n").encode())
            base_pointer = {
                "thread_id": parent_id,
                "end_ordinal_exclusive": 3,
                "end_byte_offset": end_offset,
            }
            self.write_rollout(
                parent,
                parent_meta,
                inherited,
                codex_message("excluded parent tail", ordinal=3),
            )
            self.write_rollout(
                child,
                codex_meta(child_id, history_base=base_pointer, ordinal=3),
                codex_message("child message", ordinal=4),
            )
            store = base / "state_5.sqlite"
            self.write_store(store, [(child_id, str(child), "vscode", "user", "/repo")])
            selected = self.run_selector(base, "--session-id", child_id)
            manifest = base / "lineage.json"
            manifest.write_text(selected.stdout)
            extracted = subprocess.run(
                [
                    sys.executable,
                    str(EXTRACTOR),
                    "--host",
                    "codex",
                    "--transcript-root",
                    str(sessions),
                    "--archive-root",
                    str(base / "archived_sessions"),
                    "--session-id",
                    child_id,
                    "--lineage-manifest",
                    str(manifest),
                ],
                capture_output=True,
                check=False,
            )
        self.assertEqual(selected.returncode, 0, selected.stderr)
        self.assertEqual(extracted.returncode, 0, extracted.stderr.decode())
        self.assertEqual(extracted.stdout, b"inherited parent message\0child message\0")

    def test_project_extraction_deduplicates_inherited_user_fork_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sessions = base / "sessions"
            parent_id = "44444444-4444-4444-8444-444444444444"
            child_id = "55555555-5555-4555-8555-555555555555"
            parent = sessions / f"rollout-2026-09-12T12-00-00-{parent_id}.jsonl"
            child = sessions / f"rollout-2026-09-12T13-00-00-{child_id}.jsonl"
            parent_meta = codex_meta(parent_id, ordinal=0)
            inherited = codex_message("inherited parent message", ordinal=2)
            end_offset = len((json.dumps(parent_meta) + "\n" + json.dumps(inherited) + "\n").encode())
            base_pointer = {
                "thread_id": parent_id,
                "end_ordinal_exclusive": 3,
                "end_byte_offset": end_offset,
            }
            self.write_rollout(
                parent,
                parent_meta,
                inherited,
                codex_message("parent tail", ordinal=3),
            )
            self.write_rollout(
                child,
                codex_meta(child_id, history_base=base_pointer, ordinal=3),
                codex_message("child message", ordinal=4),
            )
            store = base / "state_5.sqlite"
            self.write_store(
                store,
                [
                    (parent_id, str(parent), "vscode", "user", "/repo"),
                    (child_id, str(child), "vscode", "user", "/repo"),
                ],
            )
            selected = self.run_selector(base, "--project-root", "/repo")
            manifest = base / "lineage.json"
            manifest.write_text(selected.stdout)
            extracted = subprocess.run(
                [
                    sys.executable,
                    str(EXTRACTOR),
                    "--host",
                    "codex",
                    "--transcript-root",
                    str(sessions),
                    "--archive-root",
                    str(base / "archived_sessions"),
                    "--lineage-manifest",
                    str(manifest),
                ],
                capture_output=True,
                check=False,
            )
        self.assertEqual(selected.returncode, 0, selected.stderr)
        self.assertEqual(extracted.returncode, 0, extracted.stderr.decode())
        self.assertEqual(
            extracted.stdout,
            b"inherited parent message\0parent tail\0child message\0",
        )

    def test_selector_and_extractor_reconstruct_bounded_revert_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sessions = base / "sessions"
            thread_id = "11111111-1111-4111-8111-111111111111"
            replacement_id = "22222222-2222-4222-8222-222222222222"
            original = sessions / f"rollout-2026-09-12T12-00-00-{thread_id}.jsonl"
            replacement = sessions / f"rollout-2026-09-12T13-00-00-{thread_id}_{replacement_id}.jsonl"
            original_meta = codex_meta(thread_id, ordinal=0)
            retained = codex_message("kept before revert", ordinal=2)
            end_offset = len((json.dumps(original_meta) + "\n" + json.dumps(retained) + "\n").encode())
            base_pointer = {
                "thread_id": thread_id,
                "end_ordinal_exclusive": 3,
                "end_byte_offset": end_offset,
            }
            self.write_rollout(
                original,
                original_meta,
                retained,
                codex_message("must stay reverted", ordinal=3),
            )
            self.write_rollout(
                replacement,
                codex_meta(thread_id, history_base=base_pointer, ordinal=3),
                codex_message("kept after revert", ordinal=4),
            )
            store = base / "state_5.sqlite"
            self.write_store(store, [(thread_id, str(replacement), "vscode", "user", "/repo")])
            selected = self.run_selector(base, "--session-id", thread_id)
            manifest = base / "lineage.json"
            manifest.write_text(selected.stdout)
            extracted = subprocess.run(
                [
                    sys.executable,
                    str(EXTRACTOR),
                    "--host",
                    "codex",
                    "--transcript-root",
                    str(sessions),
                    "--archive-root",
                    str(base / "archived_sessions"),
                    "--session-id",
                    thread_id,
                    "--lineage-manifest",
                    str(manifest),
                ],
                capture_output=True,
                check=False,
            )
            invalid_manifest = json.loads(selected.stdout)
            invalid_manifest[0]["segments"][0]["end_byte_offset"] += 1
            manifest.write_text(json.dumps(invalid_manifest))
            invalid_offset = subprocess.run(
                [
                    sys.executable,
                    str(EXTRACTOR),
                    "--host",
                    "codex",
                    "--transcript-root",
                    str(sessions),
                    "--archive-root",
                    str(base / "archived_sessions"),
                    "--session-id",
                    thread_id,
                    "--lineage-manifest",
                    str(manifest),
                ],
                capture_output=True,
                check=False,
            )
        self.assertEqual(selected.returncode, 0, selected.stderr)
        self.assertEqual(extracted.returncode, 0, extracted.stderr.decode())
        self.assertEqual(extracted.stdout, b"kept before revert\0kept after revert\0")
        self.assertNotEqual(invalid_offset.returncode, 0)
        self.assertIn(b"byte offset", invalid_offset.stderr)
        self.assertEqual(invalid_offset.stdout, b"")

    @unittest.skipUnless(shutil.which("zstd"), "zstd is required for compressed-rollout coverage")
    def test_selector_and_extractor_support_archived_compressed_rollout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sessions = base / "sessions"
            sessions.mkdir()
            archive = base / "archived_sessions"
            archive.mkdir()
            thread_id = "33333333-3333-4333-8333-333333333333"
            plain = archive / f"rollout-2026-09-12T12-00-00-{thread_id}.jsonl"
            self.write_rollout(
                plain,
                codex_meta(thread_id, ordinal=0),
                codex_message("archived message", ordinal=2),
            )
            subprocess.run([shutil.which("zstd") or "zstd", "-q", "-f", str(plain)], check=True)
            plain.unlink()
            store = base / "state_5.sqlite"
            self.write_store(store, [(thread_id, str(plain), "vscode", "user", "/repo")])
            selected = self.run_selector(base, "--session-id", thread_id)
            manifest = base / "lineage.json"
            manifest.write_text(selected.stdout)
            extracted = subprocess.run(
                [
                    sys.executable,
                    str(EXTRACTOR),
                    "--host",
                    "codex",
                    "--transcript-root",
                    str(sessions),
                    "--archive-root",
                    str(archive),
                    "--lineage-manifest",
                    str(manifest),
                ],
                capture_output=True,
                check=False,
            )
        self.assertEqual(selected.returncode, 0, selected.stderr)
        self.assertEqual(extracted.returncode, 0, extracted.stderr.decode())
        self.assertEqual(extracted.stdout, b"archived message\0")


class TranscriptExtractorTests(unittest.TestCase):
    def run_extractor(self, host: str, records: list[dict], *, session_id: str = "session", raw_tail: bytes = b"") -> subprocess.CompletedProcess[bytes]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "sessions"
            root.mkdir()
            name = f"{session_id}.jsonl" if host == "claude" else f"rollout-{session_id}.jsonl"
            transcript = root / name
            transcript.write_bytes(b"".join((json.dumps(record) + "\n").encode() for record in records) + raw_tail)
            return subprocess.run(
                [sys.executable, str(EXTRACTOR), "--host", host, "--transcript-root", str(root), "--session-id", session_id, str(transcript)],
                capture_output=True,
                check=False,
            )

    def test_claude_extracts_only_human_text(self) -> None:
        records = [
            {"type": "user", "origin": {"kind": "human"}, "message": {"content": "Keep this"}},
            {"type": "user", "isMeta": True, "message": {"content": "drop meta"}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "content": "drop tool"}]}},
            {"type": "assistant", "message": {"content": "drop assistant"}},
        ]
        result = self.run_extractor("claude", records)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(result.stdout, b"Keep this\0")

    def test_codex_uses_structural_provenance_not_content_prefixes(self) -> None:
        generated = codex_message("<task-notification>generated</task-notification>")
        generated["payload"]["internal_chat_message_metadata_passthrough"]["content_item_kinds"] = ["app_context"]
        records = [
            codex_meta("session"),
            generated,
            codex_message("# AGENTS.md instructions\nThis is genuinely my request", proven=True),
            {"type": "response_item", "payload": {"type": "message", "role": "developer", "content": [{"type": "input_text", "text": "drop"}]}},
        ]
        result = self.run_extractor("codex", records)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(result.stdout, b"# AGENTS.md instructions\nThis is genuinely my request\0")

    def test_codex_rejects_embedded_nul_without_ambiguous_framing(self) -> None:
        result = self.run_extractor(
            "codex",
            [codex_meta("session"), codex_message("before\0after")],
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"embedded NUL", result.stderr)
        self.assertEqual(result.stdout, b"")

    def test_encoding_failure_never_publishes_a_partial_corpus(self) -> None:
        result = self.run_extractor(
            "codex",
            [
                codex_meta("session"),
                codex_message("valid first"),
                codex_message("invalid surrogate: \ud800"),
            ],
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"not valid UTF-8", result.stderr)
        self.assertEqual(result.stdout, b"")

    def test_codex_rejects_unproven_plain_user_text(self) -> None:
        result = self.run_extractor("codex", [codex_meta("session"), codex_message("generated continuation summary", proven=False)])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"no structural provenance", result.stderr)

    def test_codex_rejects_legacy_user_records_without_provenance(self) -> None:
        result = self.run_extractor(
            "codex",
            [
                codex_meta("session"),
                codex_message("# AGENTS.md instructions\nThis is genuinely my request", proven=False, current_envelope=False),
                codex_message("<command-message>generated</command-message>", proven=False, current_envelope=False),
            ],
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"no structural provenance", result.stderr)
        self.assertEqual(result.stdout, b"")

    def test_codex_rejects_guardian_transcript(self) -> None:
        result = self.run_extractor("codex", [codex_meta("session", source={"subagent": "guardian"}, thread_source="guardian_review", parent="root")])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"not an operator-owned root", result.stderr)

    def test_extractor_rejects_off_root_and_symlink_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "root"
            root.mkdir()
            outside = base / "session.jsonl"
            outside.write_text("{}\n")
            link = root / "session.jsonl"
            link.symlink_to(outside)
            results = [
                subprocess.run([sys.executable, str(EXTRACTOR), "--host", "claude", "--transcript-root", str(root), "--session-id", "session", str(path)], capture_output=True, check=False)
                for path in (outside, link)
            ]
        self.assertTrue(all(result.returncode != 0 for result in results))
        self.assertTrue(all(b"regular non-symlink file below a managed transcript root" in result.stderr for result in results))

    def test_malformed_middle_record_fails_but_unterminated_tail_is_tolerated(self) -> None:
        malformed = self.run_extractor("claude", [], raw_tail=b"{bad}\n")
        tail = self.run_extractor(
            "claude",
            [{"type": "user", "origin": {"kind": "human"}, "message": {"content": "Keep"}}],
            raw_tail=b'{"partial"',
        )
        self.assertNotEqual(malformed.returncode, 0)
        self.assertIn(b"invalid JSON", malformed.stderr)
        self.assertEqual(tail.returncode, 0, tail.stderr.decode())
        self.assertEqual(tail.stdout, b"Keep\0")

    def test_schema_mismatch_fails_with_line_number(self) -> None:
        result = self.run_extractor("codex", [codex_meta("session"), {"type": "response_item", "payload": {"type": "message", "role": "user", "content": "wrong"}}])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"line 2", result.stderr)

    def test_lineage_failure_never_publishes_a_partial_corpus(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "sessions"
            root.mkdir()
            valid = root / "valid.jsonl"
            invalid = root / "invalid.jsonl"
            valid.write_text(
                json.dumps(codex_meta("valid", ordinal=0))
                + "\n"
                + json.dumps(codex_message("must not leak partially", ordinal=1))
                + "\n"
            )
            invalid.write_text("{bad}\n")
            manifest = base / "lineage.json"
            manifest.write_text(
                json.dumps(
                    [
                        {
                            "session_id": "valid",
                            "segments": [{"rollout_id": "valid", "owner_thread_id": "valid", "path": str(valid), "start_ordinal": 1, "end_ordinal_exclusive": None, "end_byte_offset": None}],
                        },
                        {
                            "session_id": "invalid",
                            "segments": [{"rollout_id": "invalid", "owner_thread_id": "invalid", "path": str(invalid), "start_ordinal": 1, "end_ordinal_exclusive": None, "end_byte_offset": None}],
                        },
                    ]
                )
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(EXTRACTOR),
                    "--host",
                    "codex",
                    "--transcript-root",
                    str(root),
                    "--lineage-manifest",
                    str(manifest),
                ],
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b"")

    def test_unknown_host_is_rejected(self) -> None:
        result = self.run_extractor("other", [])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
