# PyPI Publishing Guide

This guide explains how to publish new versions of `testrail-api-module` to PyPI using GitHub Actions and release tags.

## Overview

The project uses a GitHub Actions workflow that automatically builds and publishes to PyPI when you push a release tag. The workflow is triggered by tags matching semantic version patterns.

## Prerequisites

### 1. PyPI API Token

Before publishing, you need to set up a PyPI API token in your GitHub repository secrets:

1. **Create a PyPI API Token**:
   - Go to [PyPI Account Settings](https://pypi.org/manage/account/)
   - Navigate to "API tokens" section
   - Click "Add API token"
   - Give it a name (e.g., "GitHub Actions - testrail-api-module")
   - Set the scope to the project: `testrail-api-module`
   - Copy the token (it starts with `pypi-`)

2. **Add Token to GitHub Secrets**:
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI API token
   - Click **Add secret**

## Tag Format

The workflow accepts tags in two formats:

### Format 1: With 'v' Prefix (Recommended)
```
v0.1.0
v1.2.3
v2.0.0-beta.1
v0.5.1
```

### Format 2: Without Prefix
```
0.1.0
1.2.3
2.0.0-beta.1
0.5.1
```

### Supported Patterns

The workflow matches tags using these patterns:
- `v[0-9]+.[0-9]+.[0-9]+*` - Matches `v0.1.0`, `v1.2.3-beta`, etc.
- `[0-9]+.[0-9]+.[0-9]+*` - Matches `0.1.0`, `1.2.3-beta`, etc.

**Note**: The `*` at the end allows for pre-release versions like `v1.0.0-alpha.1` or `v2.0.0-rc.1`.

## Publishing Process

### Step 1: Update Version in `pyproject.toml`

Before creating a tag, ensure the version in `pyproject.toml` matches the tag you'll create:

```toml
[project]
version = "0.5.2"  # Update this to match your tag
```

### Step 2: Update CHANGELOG.md

Move entries from the `[Unreleased]` section to a new version section:

```markdown
## [0.5.2] - 2026-01-23

### ✨ Added
- Your new features here

### 🔧 Fixed
- Your bug fixes here
```

### Step 3: Commit Your Changes

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "Prepare release v0.5.2"
```

### Step 4: Create and Push the Tag

#### Option A: Using Git Commands

```bash
# Create an annotated tag (recommended)
git tag -a v0.5.2 -m "Release v0.5.2"

# Push the tag to GitHub
git push origin v0.5.2
```

#### Option B: Using GitHub Web Interface

1. Go to your repository on GitHub
2. Click **Releases** → **Create a new release**
3. Choose a tag:
   - Click **Choose a tag** → Type `v0.5.2` → **Create new tag: v0.5.2 on publish**
4. Fill in the release title and description
5. Click **Publish release**

**Note**: When you publish a release through GitHub's interface, it automatically creates and pushes the tag, which will trigger the workflow.

### Step 5: Monitor the Workflow

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. You should see a workflow run named "Publish to PyPI"
4. Click on it to monitor the build and publish process
5. The workflow will:
   - Checkout the code
   - Set up Python and uv
   - Install build dependencies
   - Build the package (creates wheel and source distribution)
   - Upload to PyPI

### Step 6: Verify on PyPI

After the workflow completes successfully:

1. Visit [PyPI project page](https://pypi.org/project/testrail-api-module/)
2. Verify your new version appears in the release history
3. Test installation: `pip install testrail-api-module==0.5.2`

## Version Numbering Guidelines

Follow [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features (backward compatible)
- **PATCH** (0.0.1): Bug fixes (backward compatible)

### Pre-release Versions

You can also publish pre-release versions:

- **Alpha**: `v1.0.0-alpha.1`, `v1.0.0-alpha.2`
- **Beta**: `v1.0.0-beta.1`, `v1.0.0-beta.2`
- **Release Candidate**: `v1.0.0-rc.1`, `v1.0.0-rc.2`

These are useful for testing before the final release.

## Troubleshooting

### Workflow Not Triggering

- **Check tag format**: Ensure the tag matches the patterns (`v0.1.0` or `0.1.0`)
- **Verify tag was pushed**: Run `git ls-remote --tags origin` to see remote tags
- **Check Actions tab**: Look for any workflow runs or errors

### Build Failures

- **Version mismatch**: Ensure `pyproject.toml` version matches the tag
- **Missing dependencies**: Check that all build dependencies are specified
- **Syntax errors**: Run `uv build` locally to test

### PyPI Upload Failures

- **Invalid token**: Verify `PYPI_API_TOKEN` secret is set correctly
- **Token permissions**: Ensure the token has upload permissions for the project
- **Version already exists**: PyPI doesn't allow re-uploading the same version
- **Package name conflict**: Verify the package name in `pyproject.toml` is correct

### Common Errors

**Error**: `HTTPError: 400 Client Error: File already exists`
- **Solution**: The version already exists on PyPI. Use a new version number.

**Error**: `HTTPError: 403 Client Error: Invalid or non-existent authentication information`
- **Solution**: Check that `PYPI_API_TOKEN` secret is set and the token is valid.

**Error**: `ValueError: Invalid version: '0.5.1'`
- **Solution**: Ensure the version in `pyproject.toml` is valid and matches the tag.

## Best Practices

1. **Always test locally first**: Run `uv build` and `twine check dist/*` before tagging
2. **Use annotated tags**: Include a message describing the release
3. **Keep versions in sync**: Tag version should match `pyproject.toml` version
4. **Update changelog**: Document all changes before releasing
5. **Test installation**: After publishing, test installing the new version
6. **Monitor workflow**: Watch the Actions tab to catch issues early

## Quick Reference

```bash
# 1. Update version in pyproject.toml
# 2. Update CHANGELOG.md
# 3. Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "Prepare release v0.5.2"

# 4. Create and push tag
git tag -a v0.5.2 -m "Release v0.5.2"
git push origin v0.5.2

# 5. Monitor workflow in GitHub Actions tab
# 6. Verify on PyPI
```

## Related Files

- **Workflow**: `.github/workflows/publish.yml`
- **Project config**: `pyproject.toml`
- **Changelog**: `CHANGELOG.md`
