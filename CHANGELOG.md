# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Entries for **0.7.4 and earlier** are hand-written. From **0.7.5
> onward**, this file is maintained by
> [release-please](https://github.com/googleapis/release-please), which
> prepends new blocks above the most recent release based on
> Conventional Commits.

## [0.8.2](https://github.com/trtmn/testrail_api_module/compare/v0.8.1...v0.8.2) (2026-07-22)


### 🔄 Maintenance

* **deps:** bump actions/setup-python from 6 to 7 in the actions group ([#199](https://github.com/trtmn/testrail_api_module/issues/199)) ([9c4a13c](https://github.com/trtmn/testrail_api_module/commit/9c4a13c54c74ffa281ee297b91f8f981a714cbd6))
* **deps:** bump pip from 26.1 to 26.1.2 ([74e986e](https://github.com/trtmn/testrail_api_module/commit/74e986e28d57663d337338e33177071384361b20))
* **deps:** bump the uv group with 3 updates ([#198](https://github.com/trtmn/testrail_api_module/issues/198)) ([4c2b3ca](https://github.com/trtmn/testrail_api_module/commit/4c2b3ca7ab74113656a64e968602179ac5a8b3fc))
* pass a PAT to release-please-action to avoid bot-PR approval gate ([#197](https://github.com/trtmn/testrail_api_module/issues/197)) ([323d70b](https://github.com/trtmn/testrail_api_module/commit/323d70b8cc803c122341e6ed0ebb08e46093851b)), closes [#196](https://github.com/trtmn/testrail_api_module/issues/196)

## [0.8.1](https://github.com/trtmn/testrail_api_module/compare/v0.8.0...v0.8.1) (2026-07-09)


### 🔄 Maintenance

* **deps:** bump actions/checkout from 6 to 7 in the actions group ([#190](https://github.com/trtmn/testrail_api_module/issues/190)) ([432b6b0](https://github.com/trtmn/testrail_api_module/commit/432b6b0017c6c4523873f22dd54355bff67f3472))
* **deps:** bump msgpack from 1.1.2 to 1.2.1 ([#191](https://github.com/trtmn/testrail_api_module/issues/191)) ([4dcd8e8](https://github.com/trtmn/testrail_api_module/commit/4dcd8e86f186d94fc9cca91bc9ae3e6d8b640f64))
* **deps:** bump pydantic-settings from 2.14.1 to 2.14.2 ([#192](https://github.com/trtmn/testrail_api_module/issues/192)) ([c468d7e](https://github.com/trtmn/testrail_api_module/commit/c468d7e13f84225ae9fa5d0a885b2ad3562a5dc4))
* **deps:** bump the uv group with 2 updates ([#189](https://github.com/trtmn/testrail_api_module/issues/189)) ([9583b80](https://github.com/trtmn/testrail_api_module/commit/9583b801ea9dd6aeb09413f492b1724c644209ad))
* gate PyPI publish and docs deploy on the test matrix ([dc31c1a](https://github.com/trtmn/testrail_api_module/commit/dc31c1a14fe94b17a04cf82df12b99b3a515fa32))
* gate PyPI publish and docs deploy on the test matrix ([0a32f93](https://github.com/trtmn/testrail_api_module/commit/0a32f93a0e8474a3a3f9d20f013b44cd6a4ccf1a))

## [0.8.0](https://github.com/trtmn/testrail_api_module/compare/v0.7.6...v0.8.0) (2026-06-10)


### ⚠ BREAKING CHANGES

* correct transport layer (param serialization, retries, 2xx, sessions) and rewrite attachments/BDD file transfer ([#167](https://github.com/trtmn/testrail_api_module/issues/167))
* GroupsAPI.get_groups and GroupsAPI.add_group no longer accept project_id; add_group/update_group accept user_ids instead of description; LabelsAPI.add_label takes title instead of name and no longer accepts color.

### ✨ Added

* add community-authored OpenAPI 3.1 spec for the TestRail API ([#183](https://github.com/trtmn/testrail_api_module/issues/183)) ([25ccea8](https://github.com/trtmn/testrail_api_module/commit/25ccea80eb316e43da0dbfb86d8e1b2780141daf))


### 🐛 Fixed

* cases.py API parity (get_cases filters, history, copy/move/delete_cases) ([#179](https://github.com/trtmn/testrail_api_module/issues/179)) ([c10f850](https://github.com/trtmn/testrail_api_module/commit/c10f8500f54615767268344bcfc47a558503787f))
* correct groups endpoint scoping and labels payload fields ([#165](https://github.com/trtmn/testrail_api_module/issues/165)) ([d332829](https://github.com/trtmn/testrail_api_module/commit/d3328295fa324774912d8960393939b681d69c82)), closes [#142](https://github.com/trtmn/testrail_api_module/issues/142)
* correct transport layer (param serialization, retries, 2xx, sessions) and rewrite attachments/BDD file transfer ([#167](https://github.com/trtmn/testrail_api_module/issues/167)) ([999e4e2](https://github.com/trtmn/testrail_api_module/commit/999e4e28ccb251d66259aad43f955fe845a17169)), closes [#134](https://github.com/trtmn/testrail_api_module/issues/134) [#135](https://github.com/trtmn/testrail_api_module/issues/135) [#136](https://github.com/trtmn/testrail_api_module/issues/136) [#137](https://github.com/trtmn/testrail_api_module/issues/137) [#138](https://github.com/trtmn/testrail_api_module/issues/138) [#139](https://github.com/trtmn/testrail_api_module/issues/139)
* make example script Python 3.11-compatible and pagination-aware ([#173](https://github.com/trtmn/testrail_api_module/issues/173)) ([cc0ba31](https://github.com/trtmn/testrail_api_module/commit/cc0ba31aac7785c40ebb282dc3ee51f2a3fa9932))
* projects, milestones, suites, and variables API parity ([#181](https://github.com/trtmn/testrail_api_module/issues/181)) ([408bf5b](https://github.com/trtmn/testrail_api_module/commit/408bf5b94d86c3e0636fa5b4a9de4abd613d109f)), closes [#143](https://github.com/trtmn/testrail_api_module/issues/143)
* results, tests, statuses, and datasets API parity ([#180](https://github.com/trtmn/testrail_api_module/issues/180)) ([48863cd](https://github.com/trtmn/testrail_api_module/commit/48863cd68a6e145b511baa860e4e07d7dbd89eb6))
* run_report uses POST not GET per TestRail API spec ([#176](https://github.com/trtmn/testrail_api_module/issues/176)) ([5f4ffe8](https://github.com/trtmn/testrail_api_module/commit/5f4ffe850e46cb42f0b088bb6294cfeac4cea332))
* runs and plans payload/endpoint parity ([#169](https://github.com/trtmn/testrail_api_module/issues/169)) ([aa9116c](https://github.com/trtmn/testrail_api_module/commit/aa9116c5c0dbe01b8e2a0f667d0f84db44b42c2e)), closes [#141](https://github.com/trtmn/testrail_api_module/issues/141) [#101](https://github.com/trtmn/testrail_api_module/issues/101)
* sections move_section null semantics and pagination params ([#166](https://github.com/trtmn/testrail_api_module/issues/166)) ([64097be](https://github.com/trtmn/testrail_api_module/commit/64097be2d3169776d3b48e9752c6f83b8aacac5c)), closes [#145](https://github.com/trtmn/testrail_api_module/issues/145)
* shared_steps endpoint parity (filters, delete keep_in_cases) ([#178](https://github.com/trtmn/testrail_api_module/issues/178)) ([26614b1](https://github.com/trtmn/testrail_api_module/commit/26614b17090557ce5aa51362e6ae661ae7899741))
* URL-encode get_user_by_email and add project_id to get_users ([#164](https://github.com/trtmn/testrail_api_module/issues/164)) ([6938361](https://github.com/trtmn/testrail_api_module/commit/69383618d81009f282971423080ee578e36edbe9)), closes [#144](https://github.com/trtmn/testrail_api_module/issues/144)


### 🔧 Changed

* migrate remaining _api_request calls to _get/_post ([#182](https://github.com/trtmn/testrail_api_module/issues/182)) ([2683fbf](https://github.com/trtmn/testrail_api_module/commit/2683fbf2cbc8888ed241522e303d0cf41cacd8f7)), closes [#156](https://github.com/trtmn/testrail_api_module/issues/156)


### 🔄 Maintenance

* add consumer usage guide and fix stale skill API references (Closes [#96](https://github.com/trtmn/testrail_api_module/issues/96)) ([#184](https://github.com/trtmn/testrail_api_module/issues/184)) ([dace6b3](https://github.com/trtmn/testrail_api_module/commit/dace6b30b846d866eff0a6ce961d48b7a710e4dc))
* add per-entity attachment API examples to README ([#175](https://github.com/trtmn/testrail_api_module/issues/175)) ([891c826](https://github.com/trtmn/testrail_api_module/commit/891c826491cd1962a3a5bccf45a2f5623a0a89bc))
* add ruff and mypy gates; migrate deprecated ruff config keys ([#163](https://github.com/trtmn/testrail_api_module/issues/163)) ([0f934bd](https://github.com/trtmn/testrail_api_module/commit/0f934bde7669c6e53b758ab2a4468d2bd8cda31f))
* add trove classifiers and fix author metadata ([#157](https://github.com/trtmn/testrail_api_module/issues/157)) ([64fdd40](https://github.com/trtmn/testrail_api_module/commit/64fdd40247d8028f7a865577f592d72ddc5821a8))
* **deps:** bump ruff from 0.15.14 to 0.15.15 in the uv group ([c6b244f](https://github.com/trtmn/testrail_api_module/commit/c6b244f85df2c1d72e10b06d1d386d3d340cee74))
* fix README errors and remove stale planning docs ([1e927aa](https://github.com/trtmn/testrail_api_module/commit/1e927aa25bcadd18f585e749b546e6be74f996dd))
* fix README errors and remove stale planning docs ([818a4ea](https://github.com/trtmn/testrail_api_module/commit/818a4ea2b70cf6a7b65e125e74354b9405216921))
* remove .cursor/ IDE artifacts from repository ([#172](https://github.com/trtmn/testrail_api_module/issues/172)) ([cdae504](https://github.com/trtmn/testrail_api_module/commit/cdae5046e5bf3c67581260d1e7a356cb554d05f5)), closes [#171](https://github.com/trtmn/testrail_api_module/issues/171)
* remove orphaned __main__.pyi and sync stub __all__ lists ([#177](https://github.com/trtmn/testrail_api_module/issues/177)) ([36935eb](https://github.com/trtmn/testrail_api_module/commit/36935ebfd551bfe208c70015a8faa3b0d3e64260))
* stop tracking generated docs/ and remove stale publishing guide ([#174](https://github.com/trtmn/testrail_api_module/issues/174)) ([af9682e](https://github.com/trtmn/testrail_api_module/commit/af9682e6e2c5c6b2b823c8ce2bc58eb40f282f51))
* untrack stale dist/ artifacts and fix .gitignore ([#158](https://github.com/trtmn/testrail_api_module/issues/158)) ([bf8a6d5](https://github.com/trtmn/testrail_api_module/commit/bf8a6d5ea8eb7f076f6cd9a88774dd1e279772c1))

## [0.7.6](https://github.com/trtmn/testrail_api_module/compare/v0.7.5...v0.7.6) (2026-05-22)


### 🔄 Maintenance

* **deps:** bump googleapis/release-please-action in the actions group ([#126](https://github.com/trtmn/testrail_api_module/issues/126)) ([eb20d49](https://github.com/trtmn/testrail_api_module/commit/eb20d49692490e0ffd9f8bc522758e8d51bed0ae))

## [0.7.5](https://github.com/trtmn/testrail_api_module/compare/v0.7.4...v0.7.5) (2026-05-22)

> Bootstrap release for the release-please pipeline. The auto-generated changelog was hand-trimmed to keep only commits that actually landed after v0.7.4. Future releases will be fully automatic.

### ✨ Added

* migrate release flow to release-please ([#125](https://github.com/trtmn/testrail_api_module/issues/125)) ([90a54da](https://github.com/trtmn/testrail_api_module/commit/90a54dabce8975f929ecbf8223ea9b3fc7969a93))

### 🔄 Maintenance

* auto-create GitHub release after PyPI publish ([#123](https://github.com/trtmn/testrail_api_module/issues/123)) ([302b435](https://github.com/trtmn/testrail_api_module/commit/302b4354cfde2f417d7a73807134e46b1a76d350))
* set bootstrap-sha to v0.7.4 commit so release-please only scans new commits ([#128](https://github.com/trtmn/testrail_api_module/issues/128)) ([66d2def](https://github.com/trtmn/testrail_api_module/commit/66d2def59e30d6c4750b093c0688f05aeaa5f230))

## [0.7.4] - 2026-05-22

### 🔄 Maintenance

* Bump GitHub Actions to drop Node.js 20 deprecation warnings on CI runs
  (#116):
  * `actions/checkout` 4 → 6
  * `astral-sh/setup-uv` 4 → 7
  * `actions/setup-python` 5 → 6
  * `actions/configure-pages` 5 → 6
  * `actions/upload-pages-artifact` 3 → 5
  * `actions/deploy-pages` 4 → 5
* Bump Python dependencies via Dependabot's uv group (#117). The
  `requests` bump is to the runtime dep (the HTTP library that powers
  `BaseAPI`); the rest are dev-only:
  * `requests` 2.33.0 → 2.34.2 (runtime)
  * `pytest-cov` 7.0.0 → 7.1.0
  * `mypy` 1.19.1 → 2.1.0
  * `pre-commit` 4.5.1 → 4.6.0
  * `ruff` 0.14.11 → 0.15.14
  * `bandit` 1.9.3 → 1.9.4

## [0.7.3] - 2026-05-22

### 🔄 Maintenance

* Bump transitive `Pygments` from 2.19.2 to 2.20.0 to resolve a low-severity
  ReDoS advisory (CVE-2026-4539 / GHSA-5239-wwwm-4pmq). Pygments is
  dev-only — pulled in by `pdoc`, `pytest`, and `rich` — so this does
  not affect published-wheel users (#114, #115).
* Commit `.github/dependabot.yml` codifying the previously UI-only
  Dependabot configuration: weekly updates for both the `uv` ecosystem
  and `github-actions`, with both ecosystems grouped into a single PR
  each (#114, #115).
* Document the new release workflow in `.claude/skills/release/SKILL.md`:
  pre-release drift check, local `tox` run, two-PR flow
  (release-branch → development → main), PyPI verification, and
  GitHub release creation (#113).

## [0.7.2] - 2026-05-22

### 🐛 Fixed

* `ResultsAPI.add_results_for_cases` return type annotation corrected from
  `dict[str, Any]` to `list[dict[str, Any]]` to match the TestRail API, which
  returns an unpaginated list of result objects. Both `results.py` and
  `results.pyi` updated; regression test pins the annotation via
  `typing.get_type_hints` (#100, #102).
* TRAM logo on the PyPI project page (was rendering as a broken-image
  placeholder). README now references the logo by absolute
  `raw.githubusercontent.com` URL so PyPI's renderer can resolve it
  (#109, #110).

### 🔄 Maintenance

* Gitignore `.claude/agent-memory/`, `.claude/agents/`, and `.1password/`
  to prevent accidental commits of agent state and local tooling config
  containing absolute `/Users/<name>/` paths (#105, #106).
* Back-merge `main` into `development` to reconverge branches after the
  0.7.1 release work landed directly on `main`. Adds `enforce_admins`
  branch protection on `main` and a required Tests status check
  (Python 3.11/3.12/3.13/3.14) to prevent future drift (#107, #108).

## [0.7.1] - 2026-04-14

### 🔧 Changed

* Rebrand project title to **TRAM — TestRail API Module** in README
* Add TRAM logo to README
* Remove `| None` return types from 14 older submodules — methods raise on failure, never return `None`
* Improve class docstrings across all submodules with descriptive summaries
* Standardize docstring format (Args/Returns/Raises sections, remove old-style type annotations)
* Add `**kwargs: Any` type annotations to all `update_*()` methods and `base.py` helpers

### ✨ Added

* Add `__all__` exports to 18 submodules that were missing them

### 🔄 Maintenance

* Remove `mypy[dev]` from runtime dependencies (was only needed in dev)
* Remove redundant `autopep8` and `flake8` from `dependency-groups` (ruff handles both)
* Bump version to 0.7.1
* Fix release skill post-merge sync step to fetch `main` and merge back into `development`
* Add `.venv-*/` and `.1password/` patterns to `.gitignore`
* Enable parallel test execution in `tox.ini` (`parallel = auto`)
* Add Python 3.14 to supported versions (`tox.ini`, CI matrix, docs)

## [0.7.0] - 2026-02-19

### 🚨 Breaking Changes

* Removed 63 fabricated API methods across 18 submodules that do not exist in the official TestRail API:
  * **attachments**: removed `get_attachment_content`
  * **groups**: removed `add_group_to_suite`, `remove_group_from_suite`, `get_group_cases`, `get_group_suites`
  * **milestones**: removed `get_milestone_stats`
  * **priorities**: removed `get_priority`, `add_priority`, `update_priority`, `delete_priority`, `get_priority_counts`, `get_priority_stats`
  * **projects**: removed `get_project_stats`, `get_project_activity`, `get_project_attachments`, `add_project_attachment`
  * **reports**: removed `get_report`, `add_report`, `update_report`, `delete_report`, `get_report_results`
  * **result_fields**: removed `get_result_field`
  * **roles**: removed `get_role`, `add_role`, `update_role`, `delete_role`
  * **runs**: removed `get_run_stats`
  * **sections**: removed `get_section_cases`, `get_section_stats`
  * **statuses**: removed `get_status`, `add_status`, `update_status`, `delete_status`, `get_status_counts`, `get_status_history`
  * **suites**: removed `get_suite_cases`, `get_suite_stats`, `get_suite_runs`
  * **templates**: removed `get_template`, `add_template`, `update_template`, `delete_template`, `get_template_fields`, `add_template_field`, `update_template_field`, `delete_template_field`
  * **tests**: removed `get_test_results`, `add_test_result`, `add_test_results`
  * **users**: removed `add_user`, `update_user`, `delete_user`, `get_user_activity`, `get_user_projects`, `get_user_roles`
  * **variables**: removed `get_variable`, `get_variable_groups`, `add_variable_group`, `update_variable_group`, `delete_variable_group`

### 🔄 Maintenance

* Adopted git-flow branching strategy: `development` as integration branch, `main` for releases only
* Added `development` branch to CI test triggers
* Updated release skill to follow dev→main PR workflow
* Require GitHub issue before starting work; branch names must include issue number (e.g., `81-description`)
* Require updating GitHub issues with progress comments throughout work
* Close issues when PR merges to `development` with passing CI
* Changed default branch to `development` so `Closes #N` auto-closes issues

### 🐛 Fixed

* Fixed PyPI Stats badge broken link in README (trailing slash)

## [0.6.6] - 2026-02-19

### 🐛 Fixed

* Fixed 29 mypy strict-mode type errors in `cases.py`: return-type mismatches, missing annotations, unreachable code, and None-safety issues

## [0.6.5] - 2026-02-19

### 🐛 Fixed

* Fixed GitHub Source badge and docs link in README using hyphens instead of underscores for repo name

## [0.6.4] - 2026-02-19

### 🔄 Maintenance

* Automated release workflow: version tags are now created automatically by GitHub Actions when a PR is merged to `main`, which then triggers docs deployment and PyPI publishing in a single pipeline
* Added `tag-release.yml` workflow; `publish.yml` is now manual-only

## [0.6.3] - 2026-02-19

### 🐛 Fixed

* Fixed incorrect version number in README breaking changes heading (was v0.7.0, should be v0.6.2)

## [0.6.2] - 2026-02-19

### 🚨 Breaking Changes

* **Configurations API rewritten** to match the official two-level group/config structure:
  * Removed: `get_configuration`, `get_configurations`, `add_configuration`, `update_configuration`, `delete_configuration`
  * Added: `get_configs`, `add_config_group`, `add_config`, `update_config_group`, `update_config`, `delete_config_group`, `delete_config`
* **Results API restructured** to match official endpoint names:
  * Renamed: `add_result(run_id, case_id, ...)` → `add_result_for_case(run_id, case_id, ...)`
  * Changed: `add_result(test_id, ...)` now adds a result by test ID (new signature)
  * Changed: `get_results(test_id, ...)` now gets results by test ID (was an alias for `get_results_for_run`)
  * Fixed: `add_results(run_id, ...)` now calls `add_results/{run_id}` (was incorrectly calling `add_results_for_cases`)
  * Removed: `add_result_for_run` (not a real TestRail endpoint)
* **Cases API**: Renamed `get_case_history` → `get_history_for_case` to match official endpoint
* **Plans API**: Removed `get_plan_stats` (not a real TestRail endpoint)

### ✨ Added

* **Labels API** (new module): `get_label`, `get_labels`, `add_label`, `update_label`, `delete_label`
* **Plans**: `add_plan_entry`, `update_plan_entry`, `delete_plan_entry`
* **Cases**: `add_case_field`, `update_cases` (bulk), `delete_cases` (bulk)
* **Sections**: `move_section` (requires TestRail 6.5.2+)
* **Users**: `get_current_user` (requires TestRail 6.6+)
* **Statuses**: `get_case_statuses` (requires TestRail Enterprise 7.3+)
* **Datasets**: `add_dataset`, `update_dataset`, `delete_dataset` (requires TestRail Enterprise 7.6+)

### 🔧 Changed

* Updated all `.pyi` type stubs to match new method signatures
* Updated `__init__.py` to wire the new Labels module
* Rewrote test suites for Configurations, Results, Plans, and Cases to match updated APIs
* Added test suite for new Labels module

## [0.6.1] - 2026-02-19

### ✨ Added

* **CI test workflow**: Added GitHub Actions workflow to run tests across Python 3.11, 3.12, 3.13
* **PyPI publish gating**: PyPI publish workflow now depends on docs build and test workflows passing

### 🔧 Changed

* Removed mypy and ruff from CI test workflow (handled by pre-commit)
* Removed lint env from `tox.ini`
* Excluded orphaned `__main__.pyi` from mypy checks

## [0.6.0] - 2026-02-19

### 🚨 Breaking Changes

* **MCP Server removed**: Removed all MCP (Model Context Protocol) server functionality
  * Removed `mcp_server.py`, `mcp_tools.py`, `mcp_utils.py`, `mcp_prompts.py` and type stubs
  * Removed `cli.py` and `__main__.py` entry points
  * Removed `testrail-mcp-server` CLI script
  * Removed `fastmcp` dependency
  * Removed MCP-related tests and documentation
  * Impact: The package is now a pure Python API wrapper without MCP server capabilities

### ✨ Added

* `CLAUDE.md` and `AGENTS.md` for AI-assisted development guidance
* Claude Code skill for TestRail Python API integration

### 🐛 Fixed

* Fixed multi-line f-string syntax in `cases.py` and `base.py` for Python 3.11 compatibility (f-strings with `{` at end of line require Python 3.12+)

### 🔄 Maintenance

* Added `.claude/settings.local.json` to `.gitignore`
* Added pre-commit hook to block direct commits to main
* Untracked `.claude/settings.local.json` from git history

## [0.5.6] - 2026-01-27

## [0.5.5] - 2026-01-27

## [0.5.4] - 2026-01-27

## [0.5.3] - 2026-01-27

### 🔧 Changed

* **Refactored `build_and_release.py` to use GitFlow workflow**: The script now follows a proper GitFlow branching model:
  * **dev branch → main**: Version bump happens here (because main is protected), then changes are merged to main
  * **main → release**: When ready to release, merge main into release branch (version already set from dev→main)
  * **release branch**: Version tags are created and pushed on the release branch
  * The script automatically detects which branch you're on and adapts its behavior accordingly
  * PRs are now fully created (not drafts) before showing the URL
  * Impact: Provides a clear, structured workflow for managing releases with proper branch separation and version bumping on dev branch where main is protected
* **Build and Release Script Version Management**: Updated `build_and_release.py` to use `uv` for version management instead of manual file manipulation
  * Replaced manual `pyproject.toml` file parsing and regex-based version updates with `uv version` command
  * `get_current_version()` now uses `uv version --short` to read the current version
  * `update_version_in_pyproject()` now uses `uv version <version>` to update the version
  * Removed dependency on `toml` package for version management
* **Build and Release Script Interactive Mode**: Made `build_and_release.py` interactive with user confirmation prompts at each major step
  * Added `confirm_step()` helper function for consistent user prompts
  * Added `--non-interactive` flag to skip all prompts for automation/CI scenarios
* **Build and Release Script PR Creation**: Added pull request creation functionality to `build_and_release.py`
  * Automatically commits version and changelog changes
  * Creates a pull request to merge changes into the release branch
  * Uses GitHub CLI (`gh`) if available, otherwise provides manual instructions
* **Build and Release Script Tag Management**: Refactored tag creation to be opt-in and release-branch-only
  * Added `--tag` option that only works when on the release branch
  * Tag creation validates current branch matches release branch
* **Build and Release Script Version Bumping**: Added interactive version bump prompts
  * When `--version` is not provided, script prompts user to select bump type
  * Uses `uv version --bump` to automatically calculate and update the new version

### 🐛 Fixed

* Fixed `build_and_release.py` to automatically create a release branch when run on protected branches
* **Bandit Test File Scanning**: Updated bandit security scanner to include test files in security checks
* **Pytest Collection Warnings**: Fixed 86 pytest collection warnings caused by pytest attempting to collect classes from source code
* **Test Case Type Mapping**: Fixed test expectations in `test_get_required_case_fields_type_mapping` to match actual implementation

### ✨ Added

* **Pre-commit Hooks Configuration**: Added pre-commit framework to automatically run code quality checks on every commit
  * Configured hooks for Python linting and formatting (ruff)
  * Added type checking with mypy
  * Included markdown linting
  * Added security checks with bandit
  * **Credential Detection**: Added detect-secrets hook to prevent credentials from being committed
* **Repository Ruleset for Main Branch Protection**: Created GitHub repository ruleset to prevent direct pushes to main branch
* **Build and Release Script**: Added comprehensive `build_and_release.py` script to automate the release process

## [0.5.2] - 2026-01-23

### ✨ Added

* **Automated PyPI Publishing Workflow**: Added GitHub Actions workflow for automated PyPI publishing on release tags
* **MCP Prompts for Common TestRail Actions**: Added 10 reusable MCP prompts that provide guided workflows for common TestRail operations

### 🔧 Changed

* **Documentation Publishing Workflow**: Updated GitHub Pages workflow to trigger on release tags instead of main branch pushes

## [0.5.1] - 2026-01-23

### ✨ Added

* **Enhanced MCP Tool Descriptions**: Added prominent guidance in `testrail_cases` tool description to proactively guide LLMs to discover required fields before creating test cases
* **Improved Error Handling for TestRail API Validation Errors**: Enhanced error messages when TestRail API returns validation errors
* **Custom Field Normalization and Pre-Validation**: Added automatic normalization and validation of custom fields before sending to TestRail API
* **Enhanced Field Discovery Tools**: Improved `get_required_case_fields` method with format examples and better context
* **Field Requirements Caching**: Automatic caching of TestRail field requirements to reduce API calls
* **Validate-Only Mode**: New `validate_only` parameter for `add_case()` method
* **MCP Debug Logging**: Added comprehensive debug logging for MCP server components
* **Required Fields Query Method**: New `get_required_case_fields()` method for querying required fields
* **Dynamic Field Options Query**: New `get_field_options()` method for discovering valid field values
* **Dynamic Type Hints**: Field type hints now derive from TestRail config dynamically
* **Example Script for iPhone Test Cases**: Created `examples/create_10_iphone_cases_mcp.py` script

### 🔧 Changed

* **add_case Validation Disabled by Default**: Changed default value of `validate_required` parameter from `True` to `False`
* **Reduced MCP Server Log Verbosity**: Consolidated tool registration logs for cleaner output
* **Improved Error Messages**: Enhanced error handling for common MCP and API usage errors
* **Enhanced add_case Validation**: Comprehensive validation and error reporting

### 🐛 Fixed

* **Stub Generation Script**: Fixed `generate_stubs.py` to handle cases where `stubgen` executable is not in PATH
* **MCP Delete Operations JSON Error**: Fixed "Invalid JSON response" error when deleting test cases via MCP server
* **Field Validation Bug in add_case**: Fixed critical bug where required custom fields were incorrectly reported as missing
* **MCP Custom Fields Handling**: Fixed issue where custom fields passed as top-level parameters were not properly nested
* **MCP Parameter Serialization**: Fixed issue where MCP tool parameters were being serialized as Python dict strings
* **MCP Server Entry Point**: Fixed MCP configuration to use correct entry point
* **MCP Tool Parameter Schema**: Fixed JSON parsing errors when calling MCP tools
* **MCP Parameter Handling Simplification**: Further refined parameter handling in MCP tools
* **MCP Tool Params Parsing**: Fixed issue where `params` parameter was being received as a JSON string
* **Section Context Resolution**: Added suite fallback when section data lacks `project_id`
* **Case Creation Validation**: Fixed `add_case` method to properly validate required fields
* **Field Cache Empty State Bug**: Fixed critical bug where empty field cache caused validation bypass
* **Project-Specific Required Fields**: Fixed validation to correctly detect required fields from TestRail API
* **Template-Aware Required Field Validation**: `add_case` now resolves section context and validates required fields against the effective template
* **CLI Logging Side Effects**: `setup_logging()` no longer globally disables Python logging
* **Setuptools Deprecation Warning**: Updated `pyproject.toml` license format to use SPDX expression
* **Development dependency resolution**: Removed invalid `stubgen` dev dependency
* **MCP noisy INFO logs**: Suppressed `mcp.server.*` INFO output in debug/verbose mode

### 🔄 Maintenance

* **Gitignore Updates**: Added `.cursor/mcp.json` to `.gitignore`

### 📚 Documentation

* **Installation Instructions**: Streamlined and improved MCP server installation instructions

## [0.5.0] - 2026-01-14

### ✨ Added

* **MCP Server Integration**: Built-in Model Context Protocol server for AI assistant integration (Cursor, Claude Desktop, etc.)
* **FastMCP Integration**: Complete FastMCP integration as a core dependency
* **CLI Functionality**: Command-line interface for running the MCP server
* **Dynamic Version Retrieval**: Version now dynamically retrieved from `pyproject.toml`

### 🔧 Changed

* **Tool Architecture**: Transitioned from ~132 individual tools to 22 module-based tools
* **Project Name**: Changed package name from `testrail_api_module` to `testrail-api-module` for PyPI consistency
* **Dependency Organization**: Reorganized dependencies with clearer separation between runtime and development dependencies

### 📚 Documentation

* **MCP Usage Guide**: New comprehensive guide for using the MCP server
* **README Updates**: Enhanced documentation with MCP installation instructions

### 🔄 Maintenance

* Updated license year to 2026
* Removed legacy `requirements.txt` in favor of `pyproject.toml`
* Cleaned up outdated test scripts

## [0.4.0] - 2024-12-19

### 🚨 Breaking Changes

* **Exception Handling**: Methods now raise specific exceptions instead of returning `None`
* **Return Types**: Consistent return types - no more `Optional` wrappers
* **Method Signatures**: Updated parameter handling for better type safety

### ✨ Added

* **Enhanced Error Handling**: Comprehensive exception hierarchy (`TestRailAPIError`, `TestRailAuthenticationError`, `TestRailRateLimitError`, `TestRailAPIException`)
* **Performance Improvements**: HTTP session with connection pooling, automatic retry logic, configurable request timeouts
* **Better Type Safety**: Comprehensive type annotations throughout
* **Migration Guide**: Complete migration guide for upgrading from v0.3.x

### 🔧 Changed

* **Base API Client**: Complete rewrite with modern patterns
* **Authentication**: Streamlined authentication with proper validation
* **Parameter Handling**: Consistent parameter handling across all modules

### 🐛 Fixed

* **URL Construction**: Proper URL encoding and parameter handling
* **Session Management**: Proper HTTP session management with connection pooling

### 🔄 Migration Required

```python
# OLD (v0.3.x)
result = api.cases.get_case(123)
if result is None:
    print("Error occurred")

# NEW (v0.4.0)
try:
    result = api.cases.get_case(123)
    print(f"Case: {result['title']}")
except TestRailAPIError as e:
    print(f"Error: {e}")
```

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for complete migration instructions.

## [0.3.3] - Previous Version

### Features

* Basic TestRail API wrapper
* Support for all TestRail API endpoints
* Type hints for better IDE support
* Support for both API key and password authentication

### Limitations

* Methods returned `None` on errors
* No specific exception types
* Basic error handling
* No connection pooling
