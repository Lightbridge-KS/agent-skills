# Architecture: Agent Skills Repository

This repo solves one problem: agent workflows (CLI usage, references, review checklists,
…) get hand-copied between projects and drift. The fix is a single canonical repository
plus cheap distribution into each agent's skills directory.

The design is adapted from a private RAMAAI team repo (itself adapted from the OpenClaw
`agent-skills` layout), with three changes for a **public, personal** collection:

1. **Dual distribution** — a Claude Code **plugin marketplace** *and* a `uv` installer,
   both reading the same files (see "Distribution model").
2. **Categorized by domain**, where **each domain is its own plugin** (see "Domain =
   plugin").
3. **Public hygiene** — MIT licensed; no secrets, PHI, or internal hostnames.

## Three ideas

1. **Single source of truth.** Every skill has exactly one canonical home:
   `plugins/<domain>/skills/<name>/SKILL.md`. Everything else derives from it.
2. **Cheap distribution.** Skills install into a target the agent reads from — via the
   plugin system, or a small installer that symlinks (dev) or copies (portable).
3. **Thin contract + enforcement gate.** Every skill follows a minimal frontmatter
   contract, checked by a validator that runs in CI on every change.

## Two namespaces

```
plugins/   →  content (the product): domains, each a plugin, each holding skills
scripts/   →  machinery (tooling that ships and checks content)
```

A folder under `plugins/<domain>/skills/` is a skill **iff it contains `SKILL.md`**.
Discovery is `glob("plugins/*/skills/*/SKILL.md")` — the filesystem is the index. No
registry, no manifest to keep in sync (beyond the marketplace listing of domains).

## Domain = plugin

This is the key decision that lets one tree serve three consumers without duplication.

Claude Code discovers a plugin's skills under `<plugin-root>/skills/<name>/SKILL.md`. By
rooting each domain plugin at `plugins/<domain>/`, the skill path becomes
`plugins/<domain>/skills/<name>/SKILL.md` — which is *also* a clean, browse-able
"categorized by domain" tree, and *also* what the `uv` installer globs.

```
plugins/coding/
  .claude-plugin/plugin.json        ← makes "coding" an installable plugin
  skills/conventional-commit/SKILL.md
```

Adding a domain = a new `plugins/<domain>/.claude-plugin/plugin.json` + an entry in
`.claude-plugin/marketplace.json`. Adding a skill = a new `SKILL.md` under that domain.

## The contract

`SKILL.md` opens with YAML frontmatter:

| Field         | Required | Purpose                                                |
| ------------- | -------- | ------------------------------------------------------ |
| `name`        | yes      | Stable identifier; **must equal the folder name** (kebab-case). |
| `description` | yes      | Router trigger — when should the agent load this skill? |
| `metadata`    | no       | Free-form map; `version: "YYYY-MM-DD"` recommended.    |

Claude Code itself only requires `description`; we additionally enforce `name == folder`
so the marketplace and `uv` installer agree on identity. `validate_skills.py` enforces the
machine-checkable half; `CLAUDE.md` carries the human half (no secrets, no PHI, terse
operational bodies).

## Distribution model

```
CANONICAL (this repo)                          CONSUMERS
─────────────────────                          ─────────
plugins/coding/skills/conventional-commit/
        │
        ├─ plugin marketplace ───────────────► /plugin install coding@lightbridge-skills
        ├─ symlink (uv installer, macOS/Linux) ─► ~/.claude/skills/conventional-commit  (live edits)
        └─ copy    (uv installer, Windows)      ─► ~/.codex/skills/conventional-commit   (static snapshot)
```

- **Plugin marketplace** — `.claude-plugin/marketplace.json` lists each domain plugin.
  Users add the marketplace once, then install/disable per domain.
- **Symlink** — live: editing the canonical skill is instantly visible. Default on
  macOS/Linux. Zero drift.
- **Copy** — static snapshot. Default on Windows (symlinks need admin/Developer Mode) and
  good for portable/locked-down setups. Re-run the installer to refresh.

`install_skills.py` resolves `--mode auto` to symlink/copy by OS, and guards `--force`
with a real-path check so it can never delete the canonical source.

## Why Python / uv

The two scripts are trivial (glob + symlink/copy, and frontmatter parsing), and `uv` gives
one cross-platform install with PEP 723 inline dependencies (`# /// script`) — `uv run`
fetches PyYAML on demand, no virtualenv to manage. Identical behavior on macOS, Windows,
and Linux.

## CI gate

`.github/workflows/validate.yml` runs on every PR and push to `main`:

1. `uv run scripts/validate_skills.py` — frontmatter + manifest contract.
2. `uv run scripts/test_install_skills.py` — installer guard tests.
3. `py_compile` — syntax check of the tooling.

## Future enhancements

- Auto-generate the README "Skills" table from frontmatter.
- Cut git tags once skills stabilize; populate `metadata.version` consistently.
- Per-skill plugins (finer-grained install) if any single skill outgrows its domain.
