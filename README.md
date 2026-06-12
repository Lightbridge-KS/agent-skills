# Agent Skills

Reusable [Claude Code](https://docs.claude.com/en/docs/claude-code) **skills** for coding
agents, grouped by domain — **radiology**, **coding**, and **data science**. Written once,
shared everywhere.

Each domain is a self-contained Claude Code **plugin** you can install on its own. The same
files also install into any agent's `skills/` directory through a small cross-platform
script — so you can use them with or without the plugin system.

## Install

### Option A — Claude Code plugin marketplace (recommended)

```text
/plugin marketplace add Lightbridge-KS/agent-skills
/plugin install coding@lightbridge-skills
/plugin install radiology@lightbridge-skills
/plugin install data-science@lightbridge-skills
```

`/plugin marketplace update lightbridge-skills` refreshes the catalog later.

### Option B — `uv` installer (any agent, symlink or copy)

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

Install a single skill or a whole domain, into any agent's directory:

```sh
uv run scripts/install_skills.py --claude coding/conventional-commit   # one skill
uv run scripts/install_skills.py --claude --domain coding             # all of a domain
uv run scripts/install_skills.py --codex                              # ~/.codex/skills
uv run scripts/install_skills.py --target ~/some/dir                  # custom target
```

`--mode` defaults to `auto`: **symlink** on macOS/Linux (edits in this checkout are live),
**copy** on Windows (symlinks need admin / Developer Mode). Override with
`--mode symlink|copy`. `--force` replaces an already-installed skill (guarded so it can
never delete the source).

## Skills

| Plugin / domain | Skill | What it does |
| --------------- | ----- | ------------ |
| `coding` | `conventional-commit` | Write well-formed Conventional Commits messages. |
| `radiology` | `dicom-tag-reference` | Look up common DICOM tags and their meaning. *(starter)* |
| `data-science` | `chart-chooser` | Pick the right chart type for a dataset and question. *(starter)* |

Skills marked *(starter)* are minimal seeds — replace or expand them.

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
