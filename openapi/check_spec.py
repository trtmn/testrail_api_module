#!/usr/bin/env python3
"""Validate the TestRail OpenAPI spec and check it for drift.

Two independent checks:

1. **Schema validation** -- the spec is parsed and validated against the
   OpenAPI 3.1 meta-schema with ``openapi-spec-validator``.
2. **Drift detection** -- every endpoint string reachable from the wrapper's
   ``BaseAPI._get`` / ``BaseAPI._post`` / ``BaseAPI._api_request`` calls must
   appear as a path in the spec. This is the "best-effort" drift guard called
   for in issue #104: it catches the common failure mode where a new wrapper
   method ships without a corresponding spec path (or vice versa).

Run directly (``python openapi/check_spec.py``) or via the pytest wrapper in
``tests/test_openapi_spec.py``. Exits non-zero on any failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO_ROOT / "openapi" / "testrail.yaml"
SRC_DIR = REPO_ROOT / "src" / "testrail_api_module"

# Matches self._get("x") / self._post("x") and
# self._api_request("GET"|"POST", "x"); the endpoint may be an f-string.
_GET_POST = re.compile(r'self\._(?:get|post)\(\s*f?"([^"]+)"')
_API_REQUEST = re.compile(
    r'self\._api_request\(\s*"(?:GET|POST)"\s*,\s*f?"([^"]+)"'
)
# A {placeholder} path segment.
_PLACEHOLDER = re.compile(r"\{[^}]+\}")


def normalize(endpoint: str) -> str:
    """Reduce an endpoint to a comparable, parameter-agnostic path.

    ``get_case/{case_id}`` -> ``/get_case/{}``. The special
    ``get_user_by_email&email={email}`` form (TestRail routes the path inside a
    query string, so extra args use ``&``) is truncated at the ``&``.
    """
    endpoint = endpoint.split("&", 1)[0]
    endpoint = _PLACEHOLDER.sub("{}", endpoint)
    return "/" + endpoint.strip("/")


def wrapper_endpoints() -> set[str]:
    """Collect every endpoint string used by the wrapper, normalized."""
    endpoints: set[str] = set()
    for path in sorted(SRC_DIR.glob("*.py")):
        if path.name == "base.py":
            continue
        text = path.read_text()
        for match in _GET_POST.finditer(text):
            endpoints.add(normalize(match.group(1)))
        for match in _API_REQUEST.finditer(text):
            endpoints.add(normalize(match.group(1)))
    return endpoints


def spec_paths(spec: dict) -> set[str]:
    """Collect every path in the spec, normalized the same way."""
    return {normalize(p) for p in spec.get("paths", {})}


def load_spec() -> dict:
    import yaml  # local import so the import error is actionable

    with SPEC_PATH.open() as handle:
        return yaml.safe_load(handle)


def validate_schema(spec: dict) -> list[str]:
    """Return a list of schema-validation error messages (empty == valid)."""
    from openapi_spec_validator import validate
    from openapi_spec_validator.validation.exceptions import (
        OpenAPIValidationError,
    )

    try:
        validate(spec)
    except OpenAPIValidationError as exc:  # pragma: no cover - error path
        return [str(exc)]
    return []


def check_drift() -> tuple[set[str], set[str]]:
    """Return (missing_from_spec, extra_in_spec)."""
    spec = load_spec()
    wrapper = wrapper_endpoints()
    paths = spec_paths(spec)
    missing = wrapper - paths
    extra = paths - wrapper
    return missing, extra


def main() -> int:
    spec = load_spec()

    schema_errors = validate_schema(spec)
    if schema_errors:
        print("FAIL: spec does not validate against OpenAPI 3.1:")
        for err in schema_errors:
            print(f"  - {err}")
        return 1
    print(
        f"OK: {SPEC_PATH.relative_to(REPO_ROOT)} is a valid OpenAPI 3.1 spec."
    )

    missing, extra = check_drift()
    wrapper = wrapper_endpoints()
    print(
        f"OK: matched {len(wrapper)} wrapper endpoints against "
        f"{len(spec_paths(spec))} spec paths."
    )

    if missing:
        print("\nFAIL: wrapper endpoints with no matching spec path:")
        for ep in sorted(missing):
            print(f"  - {ep}")
        return 1

    if extra:
        # Extra spec paths are a warning, not a failure: the spec may document
        # endpoints the wrapper does not (yet) expose.
        print("\nWARN: spec paths not used by the wrapper (informational):")
        for ep in sorted(extra):
            print(f"  - {ep}")

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
