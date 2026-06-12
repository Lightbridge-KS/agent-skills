#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Project these shared skills into an agent's skills directory.

The canonical source of truth is `plugins/<domain>/skills/<name>/SKILL.md`. This
installer discovers those skills and either symlinks or copies them into a target
directory the agent reads from (skills land flat, keyed by skill name).

    uv run scripts/install_skills.py --list                       # available skills
    uv run scripts/install_skills.py --claude                     # all into ~/.claude/skills
    uv run scripts/install_skills.py --claude coding/conventional-commit  # one skill
    uv run scripts/install_skills.py --claude --domain coding     # a whole plugin/domain
    uv run scripts/install_skills.py --claude --dry-run           # preview, no writes

Skills are addressed as `<domain>/<skill>`, or by the bare `<skill>` name when it
is unambiguous across domains.

Install mode defaults to `auto`: symlink on macOS/Linux (live edits, zero drift),
copy on Windows where symlinks need elevated/Developer-Mode privileges. Override
with `--mode symlink|copy`.

A `--force` replace is guarded so it can never delete the canonical source if the
target happens to resolve to it.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_ROOT = REPO_ROOT / "plugins"

# Known agent skill directories. Shortcuts (--claude etc.) resolve to these.
TARGETS = {
    "claude": Path.home() / ".claude" / "skills",
    "codex": Path.home() / ".codex" / "skills",
    "agents": Path.home() / ".agents" / "skills",
}
DEFAULT_TARGET = TARGETS["claude"]


def resolve_mode(mode: str) -> str:
    """Resolve `auto` to copy on Windows, symlink elsewhere."""
    if mode != "auto":
        return mode
    return "copy" if os.name == "nt" else "symlink"


def same_real_path(left: Path, right: Path) -> bool:
    """True if both paths resolve to the same real location (guards --force)."""
    try:
        return os.path.realpath(left) == os.path.realpath(right)
    except OSError:
        return False


def available_skills() -> dict[str, Path]:
    """Map `<domain>/<skill>` -> source folder for every discovered skill."""
    found: dict[str, Path] = {}
    for skill_md in sorted(PLUGINS_ROOT.glob("*/skills/*/SKILL.md")):
        folder = skill_md.parent
        domain = folder.parent.parent.name
        found[f"{domain}/{folder.name}"] = folder
    return found


def resolve_selection(
    tokens: list[str],
    domain: str | None,
    available: dict[str, Path],
) -> tuple[list[str], list[str]]:
    """Resolve user tokens (and an optional --domain) to canonical `<domain>/<skill>` keys.

    Returns (selected_keys, errors). A bare `<skill>` resolves only when unique.
    """
    selected: list[str] = []
    errors: list[str] = []

    if domain:
        in_domain = [key for key in available if key.split("/", 1)[0] == domain]
        if not in_domain:
            errors.append(f"unknown domain: {domain}")
        selected.extend(in_domain)

    by_bare: dict[str, list[str]] = {}
    for key in available:
        by_bare.setdefault(key.split("/", 1)[1], []).append(key)

    for token in tokens:
        if token in available:  # already `<domain>/<skill>`
            selected.append(token)
        elif "/" in token:
            errors.append(f"unknown skill: {token}")
        else:  # bare `<skill>` name
            matches = by_bare.get(token, [])
            if not matches:
                errors.append(f"unknown skill: {token}")
            elif len(matches) > 1:
                errors.append(f"ambiguous skill '{token}': use one of {', '.join(matches)}")
            else:
                selected.append(matches[0])

    # De-duplicate while preserving order.
    return list(dict.fromkeys(selected)), errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="install_skills.py",
        description="Install shared skills into an agent's skills directory.",
    )
    parser.add_argument(
        "skills",
        nargs="*",
        help="Skills to install as <domain>/<skill> or bare <skill> (default: all).",
    )
    parser.add_argument("--domain", help="Install every skill in this plugin/domain.")
    parser.add_argument("--target", help="Install target directory. Default: ~/.claude/skills")
    parser.add_argument("--claude", action="store_true", help="Target ~/.claude/skills")
    parser.add_argument("--codex", action="store_true", help="Target ~/.codex/skills")
    parser.add_argument("--agents", action="store_true", help="Target ~/.agents/skills")
    parser.add_argument(
        "--mode",
        choices=["auto", "symlink", "copy"],
        default="auto",
        help="auto (default): symlink on macOS/Linux, copy on Windows.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without changing files.")
    parser.add_argument("--force", action="store_true", help="Replace an existing skill at the target.")
    parser.add_argument("--list", action="store_true", help="List available skills and exit.")
    return parser.parse_args(argv)


def resolve_target(args: argparse.Namespace) -> Path:
    chosen = [name for name in ("claude", "codex", "agents") if getattr(args, name)]
    if args.target and chosen:
        sys.exit("error: pass either --target or a shortcut (--claude/--codex/--agents), not both")
    if len(chosen) > 1:
        sys.exit("error: choose only one of --claude/--codex/--agents")
    if args.target:
        return Path(args.target).expanduser()
    if chosen:
        return TARGETS[chosen[0]]
    return DEFAULT_TARGET


def install_one(source: Path, target_dir: Path, mode: str, *, force: bool, dry_run: bool) -> None:
    name = source.name
    target = target_dir / name

    if target.exists() or target.is_symlink():
        if not force:
            print(f"exists, skipping: {target}", file=sys.stderr)
            return
        if not target.is_symlink() and same_real_path(source, target):
            print(f"target is source, skipping: {target}", file=sys.stderr)
            return
        if dry_run:
            print(f"remove {target}")
        else:
            if target.is_symlink() or target.is_file():
                target.unlink()
            else:
                shutil.rmtree(target)

    if not dry_run:
        if mode == "symlink":
            os.symlink(source, target, target_is_directory=True)
        else:
            shutil.copytree(source, target)

    prefix = f"would {mode}" if dry_run else mode
    print(f"{prefix} {name} -> {target}")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    available = available_skills()

    if args.list:
        print("\n".join(sorted(available)))
        return 0

    if not available:
        print("No plugins/*/skills/*/SKILL.md files found.", file=sys.stderr)
        return 1

    mode = resolve_mode(args.mode)
    target_dir = resolve_target(args)

    if args.skills or args.domain:
        selected, errors = resolve_selection(args.skills, args.domain, available)
        if errors:
            print("\n".join(errors), file=sys.stderr)
            print(f"available: {', '.join(sorted(available))}", file=sys.stderr)
            return 1
    else:
        selected = sorted(available)

    if not args.dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    for key in selected:
        install_one(available[key], target_dir, mode, force=args.force, dry_run=args.dry_run)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
