---
name: release
description: >
  Use this skill when the user asks to release a new version, publish to PyPI,
  bump the version, or cut a release. Handles the full release
  workflow: version bump, changelog update, commit, PR, and merge.
user_invocable: true
---

# Release Workflow

This skill handles the full release pipeline for `testrail_api_module`.

## Prerequisites

- All code changes for the release are already committed or staged
- You are on a feature branch (not `main`)
- The `[Unreleased]` section in `CHANGELOG.md` has content

## Arguments

The skill accepts an optional argument specifying the version bump type
or an explicit version number:

- `patch` (default) — e.g., 0.6.1 -> 0.6.2
- `minor` — e.g., 0.6.1 -> 0.7.0
- `major` — e.g., 0.6.1 -> 1.0.0
- An explicit version like `0.7.0` or `1.0.0`

If no argument is given, default to `patch`.

## Steps

### 1. Determine the new version

```bash
# Check current version
uv version --short

# Bump or set version
uv version --bump <patch|minor|major>
# OR for explicit version:
uv version <version>
```

Store the new version number for use in later steps.

### 2. Update CHANGELOG.md

- Read `CHANGELOG.md`
- Replace `## [Unreleased]` with `## [<version>] - <YYYY-MM-DD>`
  using today's date
- Verify the changelog entry has content (at minimum an Added,
  Changed, or Fixed section)
- Do NOT add a new empty `[Unreleased]` section — that will be
  done in the next development cycle

### 3. Commit all changes

- Stage all changes: `git add -A`
- Commit with a descriptive message summarizing the release
- If pre-commit hooks fail:
  - Fix the issues (ruff, trailing whitespace, etc.)
  - Re-stage and retry the commit
  - If only pre-existing issues remain (markdownlint line lengths,
    bandit config errors, mypy duplicate module), use `--no-verify`
  - Never use `--no-verify` to skip fixable issues like ruff errors

### 4. Push and create PR

```bash
git push -u origin <branch-name>

gh pr create --title "<summary> v<version>" --body "$(cat <<'EOF'
## Summary
<bullet points summarizing changes>

## Test plan
- [ ] CI tests pass across Python 3.11, 3.12, 3.13
- [ ] Docs build succeeds

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 5. Wait for CI and merge

```bash
# Watch CI checks (timeout 5 minutes)
gh pr checks <pr-number> --watch

# Merge after CI passes (use --admin to bypass review requirement)
gh pr merge <pr-number> --admin --merge
```

Note: This repo does not allow squash merges. Always use `--merge`.

### 6. Confirm

Report to the user:

- PR URL
- That the merge is complete
- Tagging and PyPI publishing are handled automatically by
  GitHub Actions after merge

## Important Notes

- GitHub Actions handles tagging and PyPI publishing automatically
  after the PR is merged — do NOT manually create tags
- You cannot re-publish the same version to PyPI — if a version was
  already published, you must bump to a new version
- Branch protection on `main` requires PRs; use `gh pr merge --admin`
  to bypass the review requirement
- Always use `--merge` (not `--squash`) when merging PRs
