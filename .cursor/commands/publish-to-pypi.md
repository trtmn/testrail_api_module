# Publish to PyPI

## Overview

This command helps you publish a new version of `testrail-api-module` to PyPI by creating a release tag that triggers the GitHub Actions workflow.

## Prerequisites

Before using this command, ensure:

1. **PyPI API Token is configured**: The `PYPI_API_TOKEN` secret must be set in your GitHub repository (Settings → Secrets and variables → Actions)
2. **Version is updated**: The version in `pyproject.toml` should match the tag you'll create
3. **CHANGELOG is updated**: Move entries from `[Unreleased]` to a new version section

## Process

### 1. Verify Prerequisites

Check that you have:
- ✅ Updated `pyproject.toml` with the new version number
- ✅ Updated `CHANGELOG.md` with a new version section
- ✅ Committed all changes
- ✅ `PYPI_API_TOKEN` secret configured in GitHub

### 2. Determine Version Number

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features (backward compatible)
- **PATCH** (0.0.1): Bug fixes (backward compatible)

**Current version**: Check `pyproject.toml` for the current version.

### 3. Create the Release Tag

The tag format should be either:
- `v0.5.2` (with 'v' prefix - **recommended**)
- `0.5.2` (without prefix)

**Examples**:
- `v0.5.2` - Standard release
- `v1.0.0-alpha.1` - Pre-release (alpha)
- `v1.0.0-beta.1` - Pre-release (beta)
- `v1.0.0-rc.1` - Release candidate

### 4. Create and Push Tag

#### Using Git Commands (Recommended)

```bash
# Create an annotated tag with a message
git tag -a v0.5.2 -m "Release v0.5.2"

# Push the tag to trigger the workflow
git push origin v0.5.2
```

#### Using GitHub Web Interface

1. Go to your repository on GitHub
2. Click **Releases** → **Create a new release**
3. Choose a tag: Type `v0.5.2` → **Create new tag: v0.5.2 on publish**
4. Fill in release title and description
5. Click **Publish release**

### 5. Monitor the Workflow

1. Go to **Actions** tab in GitHub
2. Find the "Publish to PyPI" workflow run
3. Monitor the build and upload process
4. Wait for completion (usually 2-5 minutes)

### 6. Verify Publication

After the workflow completes:

1. Visit [PyPI project page](https://pypi.org/project/testrail-api-module/)
2. Verify the new version appears
3. Test installation: `pip install testrail-api-module==0.5.2`

## Tag Format Rules

The workflow accepts tags matching these patterns:
- `v[0-9]+.[0-9]+.[0-9]+*` - Matches `v0.1.0`, `v1.2.3-beta`, etc.
- `[0-9]+.[0-9]+.[0-9]+*` - Matches `0.1.0`, `1.2.3-beta`, etc.

**Valid examples**:
- ✅ `v0.5.2`
- ✅ `v1.0.0`
- ✅ `v2.0.0-alpha.1`
- ✅ `0.5.2`
- ✅ `1.0.0-beta.2`

**Invalid examples**:
- ❌ `release-0.5.2` (doesn't match pattern)
- ❌ `version_0.5.2` (doesn't match pattern)
- ❌ `v0.5` (missing patch version)

## Complete Workflow Example

```bash
# 1. Update version in pyproject.toml (e.g., 0.5.2)
# 2. Update CHANGELOG.md with new version section
# 3. Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "Prepare release v0.5.2"

# 4. Create and push tag
git tag -a v0.5.2 -m "Release v0.5.2"
git push origin v0.5.2

# 5. Monitor workflow in GitHub Actions tab
# 6. Verify on PyPI after workflow completes
```

## Troubleshooting

### Workflow Not Triggering

- **Check tag format**: Must match `v0.1.0` or `0.1.0` pattern
- **Verify tag was pushed**: `git ls-remote --tags origin`
- **Check Actions tab**: Look for workflow runs

### Build/Upload Failures

- **Version mismatch**: Tag version must match `pyproject.toml` version
- **Token issues**: Verify `PYPI_API_TOKEN` secret is set correctly
- **Version exists**: PyPI doesn't allow re-uploading the same version

### Common Errors

**"File already exists"**: Version already on PyPI - use a new version number

**"Invalid authentication"**: Check `PYPI_API_TOKEN` secret in GitHub

**"Invalid version"**: Ensure version in `pyproject.toml` is valid

## Best Practices

1. **Test locally first**: Run `python -m build` before tagging
2. **Use annotated tags**: Include descriptive messages
3. **Keep versions in sync**: Tag must match `pyproject.toml` version
4. **Update changelog**: Document changes before releasing
5. **Monitor workflow**: Watch Actions tab for issues

## Related Documentation

- **Full Guide**: See `docs/PYPI_PUBLISHING_GUIDE.md` for detailed instructions
- **Workflow File**: `.github/workflows/publish.yml`
- **Project Config**: `pyproject.toml`
- **Changelog**: `CHANGELOG.md`
