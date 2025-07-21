# Commit Conventions

This document outlines the commit message conventions used in the TestRail API Module project.

## Commit Template

The project uses a Git commit template located at `.git/commit-template.txt` that is automatically loaded when you run `git commit` (without the `-m` flag).

## Conventional Commit Format

All commit messages should follow the conventional commit format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **chore**: Changes to the build process or auxiliary tools and libraries
- **ci**: Changes to CI configuration files and scripts
- **build**: Changes that affect the build system or external dependencies

### Scopes

Scopes are optional but recommended for better organization:

- **api**: API-related changes
- **docs**: Documentation changes
- **tests**: Test-related changes
- **deps**: Dependency updates
- **ci**: CI/CD changes
- **build**: Build system changes

### Examples

```
feat(api): add support for custom fields in test cases
fix(cases): resolve issue with case deletion not working
docs: update README with new authentication examples
test(runs): add integration tests for test run creation
chore(deps): update requests library to 2.31.0
ci: add GitHub Actions workflow for automated testing
```

### Breaking Changes

Breaking changes should be indicated with `!` after the type/scope:

```
feat(api)!: change authentication method signature
```

### Commit Body

The commit body should explain:
- **What** the change does
- **Why** the change was made
- **How** it differs from previous behavior

Use imperative mood ("add" not "added" or "adds").

### Commit Footer

The footer should reference related issues:

```
Fixes #123
Closes #456
Related to #789
```

## Using the Template

1. Make your changes
2. Stage your changes: `git add .`
3. Commit without the `-m` flag: `git commit`
4. Your default editor will open with the template
5. Fill in the template following the conventions
6. Save and close the editor

## Benefits

Following these conventions provides:

- **Automated changelog generation**: Tools can parse conventional commits to generate changelogs
- **Better code review**: Clear understanding of what each commit does
- **Easier debugging**: Ability to quickly identify which commit introduced a change
- **Semantic versioning**: Automatic version bumping based on commit types
- **Professional appearance**: Consistent, clean commit history

## Tools

The project uses several tools that benefit from conventional commits:

- **bumpversion**: For semantic versioning
- **pytest**: For test organization
- **pdoc**: For documentation generation

## Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#-commit-message-format) 