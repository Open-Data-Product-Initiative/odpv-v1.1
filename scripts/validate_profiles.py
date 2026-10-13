#!/usr/bin/env python3
"""Validate ODPV interoperability profiles without SDK runtime dependencies."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

from vocab_utils import iter_terms, load_yaml


ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = ROOT / "source" / "profiles"
PROFILE_FORMAT = "ODPV-Profile-1.0"
PROFILE_STATUSES = {"draft", "stable", "deprecated", "retired"}
MAPPING_KINDS = {"semanticMapping", "fieldBinding", "transformation"}
MAPPING_STATUSES = {"draft", "reviewed", "deprecated"}
SKOS_RELATIONS = {"exactMatch", "closeMatch", "broadMatch", "narrowMatch", "relatedMatch"}


def load_profile(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("profile must be a YAML mapping")
    return data


def validate_profile(path: Path, term_ids: set[str]) -> list[str]:
    try:
        profile = load_profile(path)
    except Exception as exc:  # noqa: BLE001
        return [f"{path.name}: could not parse profile: {exc}"]

    errors: list[str] = []
    for field in ("profileFormat", "id", "title", "version", "status", "vocabulary", "externalStandard", "purpose", "scope", "mappings"):
        if field not in profile:
            errors.append(f"{path.name}: missing required field {field}")

    if profile.get("profileFormat") != PROFILE_FORMAT:
        errors.append(f"{path.name}: profileFormat must be {PROFILE_FORMAT}")
    if profile.get("status") not in PROFILE_STATUSES:
        errors.append(f"{path.name}: unknown profile status {profile.get('status')!r}")

    vocabulary = profile.get("vocabulary")
    if not isinstance(vocabulary, dict) or vocabulary.get("id") != "ODPV" or not vocabulary.get("version") or not vocabulary.get("baseUri"):
        errors.append(f"{path.name}: vocabulary must identify ODPV with version and baseUri")

    external = profile.get("externalStandard")
    if not isinstance(external, dict) or not all(external.get(field) for field in ("name", "version", "specification")):
        errors.append(f"{path.name}: externalStandard must include name, version, and specification")

    scope = profile.get("scope")
    if not isinstance(scope, dict) or not scope.get("includes") or not scope.get("excludes"):
        errors.append(f"{path.name}: scope must include non-empty includes and excludes")

    mappings = profile.get("mappings")
    if not isinstance(mappings, list) or not mappings:
        errors.append(f"{path.name}: mappings must be a non-empty array")
        return errors

    seen_mapping_ids: set[str] = set()
    for mapping in mappings:
        if not isinstance(mapping, dict):
            errors.append(f"{path.name}: every mapping must be a mapping object")
            continue
        mapping_id = mapping.get("id", "<missing id>")
        if mapping_id in seen_mapping_ids:
            errors.append(f"{path.name}: duplicate mapping id {mapping_id}")
        seen_mapping_ids.add(mapping_id)
        for field in ("id", "kind", "odpvTerm", "externalReference", "rationale", "evidence", "status"):
            if not mapping.get(field):
                errors.append(f"{path.name}:{mapping_id}: missing required field {field}")
        if mapping.get("kind") not in MAPPING_KINDS:
            errors.append(f"{path.name}:{mapping_id}: unknown mapping kind {mapping.get('kind')!r}")
        if mapping.get("odpvTerm") not in term_ids:
            errors.append(f"{path.name}:{mapping_id}: unknown ODPV term {mapping.get('odpvTerm')!r}")
        if mapping.get("status") not in MAPPING_STATUSES:
            errors.append(f"{path.name}:{mapping_id}: unknown mapping status {mapping.get('status')!r}")
        if mapping.get("kind") == "semanticMapping":
            if mapping.get("relation") not in SKOS_RELATIONS:
                errors.append(f"{path.name}:{mapping_id}: semanticMapping requires a valid SKOS relation")
            if mapping.get("direction") not in {"bidirectional", "odpvToExternal", "externalToOdpv"}:
                errors.append(f"{path.name}:{mapping_id}: semanticMapping requires a valid direction")
        if mapping.get("kind") == "transformation":
            if mapping.get("direction") not in {"odpvToExternal", "externalToOdpv"}:
                errors.append(f"{path.name}:{mapping_id}: transformation requires a one-way direction")
            if not mapping.get("implementationNotes"):
                errors.append(f"{path.name}:{mapping_id}: transformation requires implementationNotes")
    return errors


def main() -> int:
    term_ids = {term["id"] for _section, term in iter_terms(load_yaml())}
    profile_paths = sorted(PROFILE_DIR.glob("*.yaml"))
    if not profile_paths:
        print("ERROR: No profiles found", file=sys.stderr)
        return 1

    errors = [error for path in profile_paths for error in validate_profile(path, term_ids)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    mapping_count = sum(len(load_profile(path)["mappings"]) for path in profile_paths)
    print(f"Profiles OK profiles={len(profile_paths)} mappings={mapping_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
