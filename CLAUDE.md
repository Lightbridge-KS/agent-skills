# Agent Skills (Lightbridge-KS)

A **public, personal** collection of reusable skills for coding agents (Claude Code,
Codex, …), grouped by domain. This repo is the **single source of truth**: a skill is
written once here and shared with everyone via a Claude Code plugin marketplace or a
small `uv` installer.

> This file is the canonical editing guide. `AGENTS.md` is a symlink to it.

## The one rule

A folder under `plugins/<domain>/skills/` is a skill **iff it contains `SKILL.md`**. The
filesystem is the index — there is no separate registry to keep in sync.

## Domain = plugin

Each domain folder under `plugins/` is **one Claude Code plugin**, listed in
`.claude-plugin/marketplace.json`. This is what lets the same tree serve three consumers:

- **Plugin marketplace** — Claude Code discovers a plugin's skills at
  `plugins/<domain>/skills/<name>/SKILL.md`.
- **`uv` installer** — `scripts/install_skills.py` globs `plugins/*/skills/*/SKILL.md`.
- **Raw browsing** — the tree reads as a clean by-domain catalog on GitHub.

To **add a domain**: create `plugins/<domain>/.claude-plugin/plugin.json` and add a
matching entry to `marketplace.json`. To **add a skill**: create
`plugins/<domain>/skills/<name>/SKILL.md`.

## Layout

- `plugins/<domain>/skills/<name>/SKILL.md` — canonical skills (the product). Helper
  scripts go in `plugins/<domain>/skills/<name>/scripts/`; supporting files (references,
  assets) sit beside `SKILL.md`.
- `plugins/<domain>/.claude-plugin/plugin.json` — the domain's plugin manifest.
- `.claude-plugin/marketplace.json` — lists every domain plugin.
- `scripts/` — repo machinery (NOT skills): installer, validator, tests.
- `docs/` — architecture notes for this repo.
- `.github/workflows/validate.yml` — CI gate on every PR and push to `main`.

## SKILL.md contract

```yaml
---
name: <kebab-case-name>          # MUST equal the folder name
description: <short trigger phrase: when should the agent load this skill>
metadata:
  version: "YYYY-MM-DD"          # recommended; validator warns if absent
---

# <Skill Title>

<Operational, terse body. Steps the agent runs. Prefer calling helper scripts
under scripts/ for repeatable logic.>
```

- `name` and `description` are **required and non-empty**. Claude Code itself only
  requires `description`; we also enforce `name == folder` so the marketplace and the
  `uv` installer agree on identity.
- `description` is a **router trigger** the agent uses to decide whether to load the
  skill — keep it short and specific, not full documentation.
- Optional Claude Code frontmatter (`allowed-tools`, `disable-model-invocation`) is
  permitted but not required.
- Skill bodies stay operational and terse, not essay-like.

## Editing rules

- **This repo is PUBLIC.** No secrets, tokens, credentials, API keys — and no PHI /
  patient data — ever. No internal hostnames or private URLs. Anonymized fixtures only.
- Edit the canonical skill here first. Never hand-edit a copy installed elsewhere —
  update here, then re-install / re-sync.
- Keep skills generally reusable; repo-specific product skills belong in the repo they
  describe.
- **Validate after every edit:** `uv run scripts/validate_skills.py`

## Tooling

Tooling is Python, executed via [`uv`](https://docs.astral.sh/uv/) (self-contained
scripts with PEP 723 inline dependencies — no virtualenv to manage). Works identically
on macOS, Windows, and Linux.

- `uv run scripts/validate_skills.py` — enforce the SKILL.md + manifest contract.
- `uv run scripts/install_skills.py --list` — list available skills.
- `uv run scripts/install_skills.py --claude` — install all into `~/.claude/skills`.
- `uv run scripts/test_install_skills.py` — installer guard tests.

## Git

Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`). GitHub Flow — branch → PR →
`main` (direct commits to `main` are fine in the early phase).
