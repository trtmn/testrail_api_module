---
name: release
description: >
  Use this skill when the user asks to release a new version, publish to PyPI,
  bump the version, or cut a release. The release pipeline is now driven by
  release-please. This skill describes how to interact with it.
user_invocable: true
---

# Release Workflow (release-please)

Releases for `testrail_api_module` are driven by
[release-please](https://github.com/googleapis/release-please). You do not
bump the version, edit the CHANGELOG, or create tags by hand. Doing those
things will confuse release-please.

## How it works

1. **Feature PRs land on `development`** with [Conventional Commits](https://www.conventionalcommits.org/) titles:
   - `feat: <short summary>` — minor version bump (✨ Added)
   - `fix: <short summary>` — patch version bump (🐛 Fixed)
   - `chore:`, `deps:`, `ci:`, `docs:`, `build:` — no version bump, but
     entries appear under the appropriate section (🔄 Maintenance)
   - `feat!: ...` or `BREAKING CHANGE:` in body — major version bump
2. **release-please-action watches `development`** (configured by
   `.github/release-please-config.json`) and keeps a single open PR titled
   `chore(main): release X.Y.Z` updated with every push. Its body shows
   the upcoming `CHANGELOG.md` block.
3. **Merging that release-please PR**:
   - Bumps `pyproject.toml` and writes the `[X.Y.Z]` CHANGELOG block on
     `development`
   - Tags the commit `vX.Y.Z`
   - Creates a GitHub release with the same notes
   - Triggers `release-please.yml`'s downstream jobs: publish to PyPI,
     deploy docs to GitHub Pages, open a sync PR `development → main`
4. **Merging the sync PR** brings `main` up to the new tag. `main` is a
   mirror; the tag itself lives on `development`.

## What this skill does

Almost nothing — the workflow does the work. Use this skill to:

### Cut a release now

If a release-please PR is open and CI on `development` is green, just
merge it. From the CLI:

```bash
gh pr list --base development --search "release-please in:title" \
  --json number,title --limit 1
# get the PR number, then:
gh pr merge <pr-number> --merge
```

Wait for `release-please.yml` to finish (it runs publish + docs +
sync-PR in parallel). Then merge the sync PR to `main`:

```bash
gh pr list --base main --head development --state open \
  --json number --limit 1 | jq -r '.[0].number' \
  | xargs -I{} gh pr merge {} --merge
```

### Check what the next release will contain

Look at the open release-please PR body:

```bash
gh pr list --base development --search "release-please in:title" \
  --json number,body --limit 1
```

The PR body has the exact upcoming CHANGELOG block.

### Force a specific version

Most of the time you don't. If you really need to (e.g., a major-version
bump that the commit history doesn't justify), edit
`.github/.release-please-manifest.json` on a feature branch and PR it to
`development`. release-please will pick up the new floor on the next run.

### PyPI token setup (one-time)

The publish jobs authenticate with the `PYPI_API_TOKEN` repository
secret. If it's missing or revoked:

1. Create a token at [PyPI Account Settings](https://pypi.org/manage/account/)
   → API tokens → Add API token, scoped to the `testrail-api-module`
   project (token starts with `pypi-`).
2. Add it on GitHub: **Settings → Secrets and variables → Actions →
   New repository secret**, name `PYPI_API_TOKEN`.

### Recover from a botched release

If the publish job fails after release-please has tagged + created the
GitHub release (e.g., PyPI rate-limited):

1. Don't re-run release-please — the tag already exists.
2. Re-run the `publish` job manually:
   `gh run rerun <run-id> --failed`
3. If PyPI is the problem, build and upload locally:
   `uv build && uv publish` (with the PyPI token in env).

## Important notes

- **Never** push to `main` directly or land a non-Conventional Commits
  PR title. release-please will silently classify the commit wrong and
  the next release will be wrong.
- **Never** edit `CHANGELOG.md` for an unreleased section by hand. The
  release-please PR is the source of truth for unreleased changes.
- **Existing CHANGELOG entries** (`[0.7.4]` and earlier) are
  hand-written and stay as-is. release-please writes 0.7.5+ in its own
  style above them. The stylistic seam is intentional.
- **Dependabot** is configured to commit with `deps:` and `ci:` prefixes
  in `.github/dependabot.yml`, so its PRs automatically classify
  correctly.
- **Sync PR to main**: the workflow opens at most one sync PR at a
  time. If you ship two releases in quick succession before merging the
  sync PR, the second release's job will detect the existing PR and
  skip — the open PR will still bring main up to the latest tag on
  merge.
