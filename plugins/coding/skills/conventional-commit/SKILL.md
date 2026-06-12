---
name: conventional-commit
description: >
  Write a well-formed Conventional Commits message for staged changes. Use when
  the user asks to commit, write a commit message, or mentions "conventional
  commit"; also use to fix or reword an existing message to the spec.
metadata:
  version: "2026-06-12"
---

# Conventional Commit

Produce a commit message that follows [Conventional Commits 1.0.0](https://www.conventionalcommits.org/).

## Format

```
<type>(<optional scope>): <description>

<optional body>

<optional footer(s)>
```

- **Subject line** ≤ 50 chars, imperative mood ("add", not "added"/"adds"), no
  trailing period.
- **Body** (optional) wraps at 72 chars; explain *what* and *why*, not *how*.
- Blank line between subject, body, and footers.

## Types

| Type | Use for |
| ---- | ------- |
| `feat` | a new feature (user-facing) |
| `fix` | a bug fix |
| `docs` | documentation only |
| `style` | formatting, whitespace — no code-behavior change |
| `refactor` | code change that neither fixes a bug nor adds a feature |
| `perf` | performance improvement |
| `test` | adding or correcting tests |
| `build` | build system or dependencies |
| `ci` | CI configuration |
| `chore` | maintenance that doesn't touch src or tests |
| `revert` | reverts a previous commit |

## Breaking changes

Either append `!` after the type/scope, or add a footer — or both:

```
feat(api)!: drop support for Node 16

BREAKING CHANGE: the minimum supported runtime is now Node 18.
```

## Steps

1. Inspect what is staged: `git diff --staged` (if nothing staged, ask before
   running `git add`).
2. Pick the single most accurate `type`; add a `scope` only when it sharpens
   meaning (a module, package, or area name).
3. Write the subject, then a body if the change needs rationale.
4. Add footers for issue refs (`Refs: #123`, `Closes: #123`) or breaking changes.
5. Show the message for confirmation, then commit:
   `git commit -m "<subject>" -m "<body>"`.

## Examples

```
feat(installer): add --domain flag to install a whole plugin at once

fix: guard --force so it can never delete the canonical source

docs(readme): document plugin-marketplace install path

refactor(validate): extract frontmatter parsing into a helper
```
