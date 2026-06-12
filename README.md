# Agent Skills

Reusable **skills** for AI coding agents — [Claude Code](https://docs.claude.com/en/docs/claude-code),
[Codex](https://developers.openai.com/codex/), [OpenCode](https://opencode.ai/), and any other
agent that reads skills from a directory — grouped by domain. Written once, shared everywhere.

A skill is a plain `SKILL.md` (plus optional helper files), so it works with any
skill-aware agent. The two install paths below project the same source files into whichever
agent you use.

## Install

### Option A — `uv` installer (any agent)

The portable path: installs skills into any agent's `skills/` directory by **symlink** (live
edits) or **copy** (static snapshot). Works with Claude Code, Codex, OpenCode, and friends.

Requires [`uv`](https://docs.astral.sh/uv/) (one cross-platform install):

```sh
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```sh
git clone https://github.com/Lightbridge-KS/agent-skills.git
cd agent-skills

uv run scripts/install_skills.py --list               # what's available
uv run scripts/install_skills.py --claude --dry-run   # preview, no writes
uv run scripts/install_skills.py --claude             # install all into ~/.claude/skills
```

Pick the agent (or any directory), and install a single skill or a whole domain:

```sh
uv run scripts/install_skills.py --claude     # ~/.claude/skills   (Claude Code)
uv run scripts/install_skills.py --codex      # ~/.codex/skills    (Codex)
uv run scripts/install_skills.py --agents     # ~/.agents/skills   (OpenCode & others)
uv run scripts/install_skills.py --target ~/some/dir                    # custom target

uv run scripts/install_skills.py --codex coding/example-skill     # one skill
uv run scripts/install_skills.py --codex --domain coding               # a whole domain
```

`--mode` defaults to `auto`: **symlink** on macOS/Linux (edits in this checkout are live),
**copy** on Windows (symlinks need admin / Developer Mode). Override with
`--mode symlink|copy`. `--force` replaces an already-installed skill (guarded so it can
never delete the source).

> Check your agent's docs for the directory it reads skills from, then point `--target` at
> it if it isn't one of the shortcuts above.

### Option B — Claude Code plugin marketplace (Claude Code only)

If you use Claude Code, you can install whole domains as plugins, with no clone:

```text
/plugin marketplace add Lightbridge-KS/agent-skills
/plugin install coding@lightbridge-skills
```

`/plugin marketplace update lightbridge-skills` refreshes the catalog later.

## Skills

| Domain | Skill | What it does |
| ------ | ----- | ------------ |
| `coding` | `commit-push-pr` | Commit, push, and create/update a draft PR in one guided flow. |
| `coding` | `c4-architect` | Turn requirements into Simon Brown's C4 (C1–C3) architecture diagrams. |
| `coding` | `explain-system-architecture` | Reverse-engineer an existing codebase into one architecture doc with Mermaid diagrams. |
| `coding` | `explain-ux-design` | Document a codebase's user-facing surface (API/UX) — the system from outside the boundary. |

## Add a skill

1. Create `plugins/<domain>/skills/<name>/SKILL.md` (`name` must equal the folder name).
   See the contract and rules in [`CLAUDE.md`](CLAUDE.md).
2. Put any helper scripts in `plugins/<domain>/skills/<name>/scripts/`.
3. Validate: `uv run scripts/validate_skills.py`
4. Open a PR. CI runs the validator and installer tests on every PR.

To add a whole new domain, create `plugins/<domain>/.claude-plugin/plugin.json` and add a
matching entry to [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

## Validate

```sh
uv run scripts/validate_skills.py        # SKILL.md + manifest contract
uv run scripts/test_install_skills.py    # installer guards
```

## Layout

```text
.claude-plugin/marketplace.json   # lists each domain as a plugin
plugins/
  <domain>/
    .claude-plugin/plugin.json    # the domain's plugin manifest
    skills/<name>/SKILL.md        # source of truth — one folder per skill
scripts/                          # repo machinery (not skills)
  install_skills.py
  validate_skills.py
  test_install_skills.py
docs/architecture.md              # how and why this repo is structured
```

See [`docs/architecture.md`](docs/architecture.md) for the design rationale.

## License

[MIT](LICENSE) © Kittipos S. ([Lightbridge-KS](https://github.com/Lightbridge-KS))
