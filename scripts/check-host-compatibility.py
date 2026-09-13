#!/usr/bin/env python3
"""Validate the repository's Claude Code and Codex plugin contracts."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


EXPECTED_NAME = "deliberate-engineering"
COMMAND_SKILL_RE = re.compile(r"Invoke the `([^`]+)` skill")


def load_json(path: Path, root: Path, errors: list[str]) -> dict:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(root)}")
        return {}
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON in {path.relative_to(root)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(root)} must contain a JSON object")
        return {}
    return value


def resolve_declared_paths(plugin_root: Path, value: object, field: str, errors: list[str]) -> list[Path]:
    values = value if isinstance(value, list) else [value]
    resolved_paths: list[Path] = []
    if not values:
        errors.append(f"{field} paths must not be empty")
        return resolved_paths
    for declared in values:
        resolved = resolve_declared_path(plugin_root, declared, field, errors)
        if resolved is not None:
            resolved_paths.append(resolved)
    return resolved_paths


def resolve_declared_path(plugin_root: Path, value: object, field: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value.startswith("./"):
        errors.append(f"each Codex and Claude {field} path must be a ./-relative string")
        return None
    resolved = (plugin_root / value[2:]).resolve()
    try:
        resolved.relative_to(plugin_root.resolve())
    except ValueError:
        errors.append(f"{field} path escapes the plugin root: {value}")
        return None
    if not resolved.is_dir():
        errors.append(f"{field} path does not resolve to a directory: {value}")
    return resolved


def marketplace_entry(manifest: dict, path: str, errors: list[str]) -> dict:
    plugins = manifest.get("plugins")
    if not isinstance(plugins, list):
        errors.append(f"{path} must contain a plugins array")
        return {}
    matches = [entry for entry in plugins if isinstance(entry, dict) and entry.get("name") == EXPECTED_NAME]
    if len(matches) != 1:
        errors.append(f"{path} must contain exactly one {EXPECTED_NAME} entry")
        return {}
    return matches[0]


def check_repository(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    plugin_root = root / "plugins" / EXPECTED_NAME

    claude_plugin_path = plugin_root / ".claude-plugin" / "plugin.json"
    codex_plugin_path = plugin_root / ".codex-plugin" / "plugin.json"
    claude_market_path = root / ".claude-plugin" / "marketplace.json"
    codex_market_path = root / ".agents" / "plugins" / "marketplace.json"

    claude_plugin = load_json(claude_plugin_path, root, errors)
    codex_plugin = load_json(codex_plugin_path, root, errors)
    claude_market = load_json(claude_market_path, root, errors)
    codex_market = load_json(codex_market_path, root, errors)

    for label, manifest in (("Claude", claude_plugin), ("Codex", codex_plugin)):
        if manifest and manifest.get("name") != EXPECTED_NAME:
            errors.append(f"{label} plugin name must be {EXPECTED_NAME}")

    claude_skills = resolve_declared_paths(plugin_root, claude_plugin.get("skills"), "skills", errors) if claude_plugin else []
    codex_skills = resolve_declared_paths(plugin_root, codex_plugin.get("skills"), "skills", errors) if codex_plugin else []
    claude_commands = resolve_declared_paths(plugin_root, claude_plugin.get("commands"), "commands", errors) if claude_plugin else []
    if codex_plugin and "commands" in codex_plugin:
        errors.append("Codex adapter must expose command entry points as native skills, not legacy commands")
    shared_skills = (plugin_root / "skills").resolve()
    codex_commands = (plugin_root / "codex" / "commands").resolve()
    if claude_skills != [shared_skills]:
        errors.append("Claude skills must resolve exactly to the shared skills directory")
    if codex_skills != [shared_skills, codex_commands]:
        errors.append("Codex skills must resolve to shared skills followed by Codex command adapters")
    if claude_commands != [(plugin_root / "commands").resolve()]:
        errors.append("Claude commands must resolve exactly to the Claude command adapter directory")

    claude_entry = marketplace_entry(claude_market, ".claude-plugin/marketplace.json", errors)
    codex_entry = marketplace_entry(codex_market, ".agents/plugins/marketplace.json", errors)
    versions = {
        "Claude plugin": claude_plugin.get("version") if claude_plugin else None,
        "Codex plugin": codex_plugin.get("version") if codex_plugin else None,
        "Claude marketplace": claude_entry.get("version") if claude_entry else None,
    }
    if any(not isinstance(value, str) or not value for value in versions.values()):
        errors.append("all version-bearing host metadata must declare a non-empty version")
    elif len(set(versions.values())) != 1:
        rendered = ", ".join(f"{label}={value}" for label, value in versions.items())
        errors.append(f"host metadata versions must be in lockstep: {rendered}")
    if codex_entry:
        source = codex_entry.get("source")
        expected_source = {"source": "local", "path": f"./plugins/{EXPECTED_NAME}"}
        if source != expected_source:
            errors.append(f"Codex marketplace source must be {expected_source}")
        policy = codex_entry.get("policy")
        if not isinstance(policy, dict) or policy.get("installation") != "AVAILABLE":
            errors.append("Codex marketplace plugin must be available for installation")

    commands_dir = plugin_root / "commands"
    skills_dir = plugin_root / "skills"
    invoked: set[str] = set()
    claude_targets: dict[str, str] = {}
    command_files = sorted(commands_dir.glob("*.md")) if commands_dir.is_dir() else []
    if len(command_files) != 12:
        errors.append(f"expected 12 Claude command adapters, found {len(command_files)}")
    for command in command_files:
        body = command.read_text()
        if not body.startswith("---\n") or "description:" not in body.split("---", 2)[1]:
            errors.append(f"Claude command needs description frontmatter: {command.name}")
        if "$ARGUMENTS" not in body:
            errors.append(f"Claude command must propagate arguments: {command.name}")
        match = COMMAND_SKILL_RE.search(body)
        if not match:
            errors.append(f"command does not invoke one shared skill: {command.name}")
            continue
        skill = match.group(1)
        claude_targets[command.stem] = skill
        if skill in invoked:
            errors.append(f"multiple commands invoke {skill}")
        invoked.add(skill)
        if not (skills_dir / skill / "SKILL.md").is_file():
            errors.append(f"command {command.name} invokes missing skill {skill}")

    adapter_dirs = sorted(path for path in codex_commands.iterdir() if path.is_dir()) if codex_commands.is_dir() else []
    if len(adapter_dirs) != 12:
        errors.append(f"expected 12 Codex command adapters, found {len(adapter_dirs)}")
    if {path.name for path in adapter_dirs} != {path.stem for path in command_files}:
        errors.append("Claude and Codex command names must match")
    codex_invoked: set[str] = set()
    codex_targets: dict[str, str] = {}
    for adapter in adapter_dirs:
        skill_path = adapter / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"Codex command adapter is missing SKILL.md: {adapter.name}")
            continue
        body = skill_path.read_text()
        frontmatter = body.split("---", 2)[1] if body.startswith("---\n") and len(body.split("---", 2)) == 3 else ""
        if f"name: {adapter.name}" not in frontmatter or "description:" not in frontmatter:
            errors.append(f"Codex command adapter has invalid metadata: {adapter.name}")
        if "$ARGUMENTS" in body or re.search(r"\$[1-9]", body):
            errors.append(f"Codex command adapter contains unsupported template arguments: {adapter.name}")
        if "text accompanying this invocation" not in body:
            errors.append(f"Codex command adapter must preserve invocation context: {adapter.name}")
        match = COMMAND_SKILL_RE.search(body)
        if not match:
            errors.append(f"Codex command adapter does not invoke one shared skill: {adapter.name}")
            continue
        skill = match.group(1)
        codex_targets[adapter.name] = skill
        codex_invoked.add(skill)
        if not (skills_dir / skill / "SKILL.md").is_file():
            errors.append(f"Codex command adapter {adapter.name} invokes missing skill {skill}")
    if codex_invoked != invoked:
        errors.append("Claude and Codex command adapters must dispatch to the same shared skills")
    for command, claude_target in claude_targets.items():
        codex_target = codex_targets.get(command)
        if codex_target is not None and codex_target != claude_target:
            errors.append(
                f"dispatch target mismatch for {command}: Claude={claude_target}, Codex={codex_target}"
            )

    forbidden = ("~/.claude", "CLAUDE_PLUGIN_ROOT", ".claude-plugin")
    codex_adapter_files = [codex_plugin_path, codex_market_path]
    if (plugin_root / "codex").is_dir():
        codex_adapter_files.extend((plugin_root / "codex").rglob("*"))
    for path in codex_adapter_files:
        if path.is_file():
            text = path.read_text()
            for token in forbidden:
                if token in text:
                    errors.append(f"Codex adapter depends on Claude token {token}: {path.relative_to(root)}")

    for path in skills_dir.rglob("*") if skills_dir.is_dir() else []:
        if not path.is_file() or path.suffix not in (".md", ".py", ".json"):
            continue
        body = path.read_text()
        for token in ("/deliberate-engineering:", "$ARGUMENTS", "${CLAUDE_PLUGIN_ROOT}", "AskUserQuestion", "Task tool"):
            if token in body:
                errors.append(
                    f"shared methodology contains host-specific token {token}: {path.relative_to(root)}"
                )

    host_skill = skills_dir / "deliberate-engineering-host-context" / "SKILL.md"
    resolver = host_skill.parent / "scripts" / "resolve-host-context.py"
    selector = host_skill.parent / "scripts" / "select-codex-rollouts.py"
    extractor = host_skill.parent / "scripts" / "extract-operator-messages.py"
    for path in (host_skill, resolver, selector, extractor):
        if not path.is_file():
            errors.append(f"missing host-context resource {path.relative_to(root)}")
    if host_skill.is_file():
        host_contract = host_skill.read_text()
        for requirement in ("umask 077", "0700", "0600"):
            if requirement not in host_contract:
                errors.append(f"host-context private-file contract must require {requirement}")

    path_sensitive = (
        "deliberate-engineering-overrides",
        "deliberate-engineering-state",
        "deliberate-engineering-capture",
        "deliberate-engineering-voice",
        "deliberate-engineering-voice-build",
    )
    for skill in path_sensitive:
        path = skills_dir / skill / "SKILL.md"
        if path.is_file() and "deliberate-engineering-host-context" not in path.read_text():
            errors.append(f"path-sensitive skill must consult host context: {skill}")

    version_gate = root / ".github" / "workflows" / "version-gate.yml"
    if version_gate.is_file():
        gate_text = version_gate.read_text()
        expected_diff = 'git diff --name-only "$base" HEAD -- plugins/deliberate-engineering/ .claude-plugin/marketplace.json .agents/plugins/marketplace.json'
        if expected_diff not in gate_text:
            errors.append("version gate must include the plugin payload and both marketplace manifests")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = check_repository(root)
    if errors:
        for error in errors:
            print(f"  FAIL: {error}", file=sys.stderr)
        print(f"Host compatibility check FAILED: {len(errors)} error(s).", file=sys.stderr)
        return 1
    print("Host compatibility check OK: shared methodology, 2 native adapters, 12 matched command entry points.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
