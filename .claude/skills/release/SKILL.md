---
name: release
description: >
  Use this skill when the user asks to release a new version, publish to PyPI,
  bump the version, or cut a release. Handles the full release
  workflow: version bump, changelog update, commit, PR, merge, PyPI verify,
  and GitHub release.
user_invocable: true
---

# Release Workflow

This skill handles the full release pipeline for `testrail_api_module`.

## Prerequisites

- All code changes for the release are already merged into `development`
- You are on the `development` branch
- The `[Unreleased]` section in `CHANGELOG.md` has content
- `gh` is authenticated and has push access to the repo

## Arguments

The skill accepts an optional argument specifying the version bump type
or an explicit version number:

- `patch` (default) — e.g., 0.6.1 -> 0.6.2
- `minor` — e.g., 0.6.1 -> 0.7.0
- `major` — e.g., 0.6.1 -> 1.0.0
- An explicit version like `0.7.0` or `1.0.0`

If no argument is given, default to `patch`.

## Steps

### 1. Ensure you are on `development` and up to date

```bash
git checkout development
git pull origin development
```

### 2. Verify branches haven't drifted

```bash
git fetch origin --quiet
git log --oneline origin/main..origin/development | head
git log --oneline origin/development..origin/main | head
```

`development` should be **ahead** of `main`, never behind. If `main` has
commits not on `development`, stop and back-merge `main` into `development`
first (see `#107` / `#108` for the canonical pattern). Releasing without
fixing this drift would downgrade `pyproject.toml` and drop work.

### 3. Run the full multi-version test suite locally

```bash
uv run tox
```

All supported Python versions (3.11, 3.12, 3.13, 3.14) must pass. CI will
run the same matrix on the release PR, but verifying locally catches
regressions before opening the PR and saves a round-trip.

### 4. Determine and apply the new version

```bash
# Check current version
uv version --short

# Bump or set version
uv version --bump <patch|minor|major>
# OR for explicit version:
uv version <version>
```

Store the new version number for use in later steps. `uv version` updates
both `pyproject.toml` and `uv.lock`.

### 5. Update CHANGELOG.md

- Replace `## [Unreleased]` with `## [<version>] - <YYYY-MM-DD>` using today's date
- Verify the changelog block has content (at minimum a `### Added`,
  `### Changed`, or `### Fixed` section)
- Do NOT add a new empty `[Unreleased]` section — that's added in the
  next development cycle when the first PR after release lands

### 6. Commit on a release branch (not directly on `development`)

Auto-mode and convention both block direct commits to `development`.
Branch off, commit, push, PR back to `development`.

```bash
git checkout -b release-<version> development
git add pyproject.toml uv.lock CHANGELOG.md
PATH="$PWD/.venv/bin:$PATH" git commit -m "release: <version>"
git push -u origin release-<version>
```

Notes:

- Use `release-<version>` (single dash, no slash) — `release/<version>`
  collides with the stale `release` branch on origin
- `PATH=...` makes pre-commit hooks find the venv's `pre-commit` binary
- Stage only the three release files. `git add -A` can pick up untracked
  agent state or tooling config

If pre-commit hooks fail on fixable issues (ruff, trailing whitespace),
fix and re-stage. Never `--no-verify` to skip fixable issues. The
markdownlint config relaxes MD013/MD024/MD033/MD041 for this repo so
CHANGELOG edits should pass cleanly.

### 7. PR the release branch to `development`

```bash
gh pr create --base development --head release-<version> \
  --title "release: <version> version bump + changelog (prepare for main)" \
  --body "..."
```

Wait for CI (Tests x4: Python 3.11/3.12/3.13/3.14), then squash-merge.

```bash
gh pr merge <pr-number> --squash --delete-branch
```

This lands the version bump on `development`, satisfying the rule that
`development` is always ahead of `main`.

### 8. Open the actual release PR `development → main`

```bash
git checkout development && git pull
gh pr create --base main --head development --title "release: <version>" --body "..."
```

The PR body should summarize what's shipping. Wait for CI (all four
Test checks must pass — they're required by `main` branch protection).

### 9. Merge to `main`

```bash
gh pr view <pr-number> --json mergeStateStatus  # must be CLEAN
gh pr merge <pr-number> --merge  # preserves merge commit
```

Notes:

- Use `--merge` (not `--squash`) so the merge commit is preserved on `main`
- `enforce_admins: true` is set on `main`; the `--admin` flag is a no-op
  but harmless. CI must be green; you cannot bypass

The merge triggers `tag-release.yml`:

1. **Create version tag** — reads `uv version --short`, tags `v<version>`
2. **Build and deploy documentation** — GitHub Pages
3. **Build and publish to PyPI** — `uv build` + `twine upload`

### 10. Verify PyPI publish

```bash
gh run watch <tag-release-run-id> --exit-status

curl -s https://pypi.org/pypi/testrail-api-module/json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); \
    print('latest:', d['info']['version'])"

git fetch --tags --quiet
git tag --sort=-version:refname | head -3
```

Confirm: PyPI shows the new version and `v<version>` tag exists locally.

### 11. Create a GitHub release

PyPI and tag are not enough — also create a GitHub release so it
appears under <https://github.com/trtmn/testrail_api_module/releases>
and Watchers get notified.

```bash
gh release create v<version> --title "v<version>" --notes "$(cat <<'EOF'
## 🐛 Fixed
- <items, with issue refs>

## 🔧 Changed
- <items>

## 🔄 Maintenance
- <items>

## Install

\`\`\`bash
pip install testrail-api-module==<version>
\`\`\`

## Full changelog

See [CHANGELOG.md](https://github.com/trtmn/testrail_api_module/blob/v<version>/CHANGELOG.md#<anchor>) and the [PyPI page](https://pypi.org/project/testrail-api-module/<version>/).
EOF
)"
```

Use the same category headings as `CHANGELOG.md` (🐛 Fixed, ✨ Added,
🔧 Changed, 🚨 Breaking Changes, 🔄 Maintenance). The CHANGELOG anchor
follows GitHub's convention: `#<version>---<yyyy-mm-dd>` (lowercase,
hyphens, em-dash replaced with three hyphens).

### 12. Confirm

Report to the user:

- PR URL (release PR)
- Tag URL (`https://github.com/trtmn/testrail_api_module/releases/tag/v<version>`)
- PyPI URL (`https://pypi.org/project/testrail-api-module/<version>/`)
- GitHub release URL
- That `development` and `main` are now in sync (the release PR
  brought `development`'s state into `main`)

## Important Notes

- **Never push directly to `main`.** `enforce_admins: true` blocks it
  anyway; if it ever worked, you'd recreate the drift problem fixed in #107
- **Never push directly to `development`.** Auto-mode classifier blocks it;
  use a feature/release branch + PR
- **Branch naming**: `release-<version>` (single dash). `release/<version>`
  collides with the stale `release` branch
- **CHANGELOG order**: newest version on top, under the `## [Unreleased]`
  block if present, above the previous release block
- **Cannot re-publish** the same version to PyPI — if a version was
  already published, bump to a new one
- **`tag-release.yml` runs on PR-close-to-`main`** with
  `merged == true`. If the workflow doesn't run after a merge, check
  that the PR's base was actually `main` (not `development`)
