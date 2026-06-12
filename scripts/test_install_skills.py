#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Behavioral tests for the install_skills.py guards.

Each test spins up a throwaway repo layout (plugins/<domain>/skills/<name>/) in a
temp dir and drives install_skills.py as a subprocess.

    uv run scripts/test_install_skills.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "install_skills.py"
SKILL_MD = "---\nname: sample\ndescription: sample\n---\n"


def make_repo(base: Path) -> Path:
    """Create a minimal repo with one skill at plugins/demo/skills/sample/SKILL.md."""
    repo = base / "repo"
    (repo / "scripts").mkdir(parents=True)
    skill_dir = repo / "plugins" / "demo" / "skills" / "sample"
    skill_dir.mkdir(parents=True)
    (repo / "scripts" / "install_skills.py").write_bytes(SCRIPT.read_bytes())
    (skill_dir / "SKILL.md").write_text(SKILL_MD)
    return repo


def run_install(repo: Path, *args: str) -> subprocess.CompletedProcess:
    """Run the installer copied into a throwaway repo so REPO_ROOT resolves to that repo."""
    return subprocess.run(
        [sys.executable, str(repo / "scripts" / "install_skills.py"), *args],
        capture_output=True,
        text=True,
    )


class InstallSkillsTest(unittest.TestCase):
    def test_force_skips_target_that_is_source(self):
        with tempfile.TemporaryDirectory() as dir_:
            repo = make_repo(Path(dir_))
            source_parent = repo / "plugins" / "demo" / "skills"

            # Target dir IS the skills dir, so the "target" resolves to the source.
            result = run_install(
                repo,
                "--target", str(source_parent),
                "--force", "sample",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("target is source, skipping", result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertTrue((source_parent / "sample" / "SKILL.md").exists())

    def test_force_copy_replaces_existing_symlink(self):
        with tempfile.TemporaryDirectory() as dir_:
            base = Path(dir_)
            repo = make_repo(base)
            target = base / "target"
            target.mkdir()
            source = repo / "plugins" / "demo" / "skills" / "sample"
            os.symlink(source, target / "sample")

            result = run_install(
                repo,
                "--target", str(target),
                "--force", "--mode", "copy", "sample",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("copy sample", result.stdout)
            self.assertFalse((target / "sample").is_symlink())
            self.assertTrue((target / "sample" / "SKILL.md").exists())
            self.assertTrue((source / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
