"""Tests for the community-authored OpenAPI 3.1 spec (issue #104).

These guard two invariants:

* ``openapi/testrail.yaml`` validates against the OpenAPI 3.1 meta-schema.
* Every endpoint the wrapper actually calls has a matching path in the spec
  (drift detection).

The heavy lifting lives in ``openapi/check_spec.py`` so the same logic can run
both under pytest and as a standalone CLI / CI step.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECK_SPEC = REPO_ROOT / "openapi" / "check_spec.py"


def _load_check_spec():
    spec = importlib.util.spec_from_file_location("check_spec", CHECK_SPEC)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_spec = _load_check_spec()

# Skip gracefully if optional spec-tooling deps are absent (e.g. a minimal
# install without the dev extra).
pytest.importorskip("yaml", reason="PyYAML required for OpenAPI spec tests")
pytest.importorskip(
    "openapi_spec_validator",
    reason="openapi-spec-validator required for OpenAPI spec tests",
)


def test_spec_file_exists() -> None:
    """The spec file is present at the documented location."""
    assert check_spec.SPEC_PATH.is_file()


def test_spec_validates_as_openapi_31() -> None:
    """The spec validates against the OpenAPI 3.1 meta-schema."""
    spec = check_spec.load_spec()
    assert spec["openapi"].startswith("3.1")
    errors = check_spec.validate_schema(spec)
    assert errors == [], "OpenAPI validation errors:\n" + "\n".join(errors)


def test_every_wrapper_endpoint_has_a_spec_path() -> None:
    """Drift guard: each wrapper endpoint string appears as a spec path."""
    missing, _extra = check_spec.check_drift()
    assert not missing, (
        "Wrapper endpoints missing from openapi/testrail.yaml: "
        + ", ".join(sorted(missing))
    )


def test_wrapper_endpoints_were_discovered() -> None:
    """Sanity check that the extractor actually found endpoints."""
    endpoints = check_spec.wrapper_endpoints()
    # The wrapper exposes ~100 endpoints; guard against a broken extractor
    # silently matching nothing and making the drift test vacuous.
    assert len(endpoints) > 90
