# ODPV interoperability profiles

An ODPV interoperability profile is a versioned, machine-readable declaration of how ODPV terms can be used with one external standard. A profile is a companion artifact: it does not replace ODPV, the external standard, a catalog, a data contract, a lineage system, or a policy engine.

## Release status

**ODPV 1.1 is a stable release.** The vocabulary and every profile in this release are published stable artifacts. These files can be used as a stable basis for implementation and conformance.

The files in this directory are the semantic authority. The [Open Data Product Agent SDK](https://github.com/Open-Data-Product-Initiative/odp-agent-sdk) is the implementation authority for loading, validating, transforming, and reporting against them.

## Profile contract

Every profile conforms to [`odpv.profile.schema.json`](../schema/odpv.profile.schema.json) and identifies:

- the exact ODPV and external-standard versions it concerns;
- its scope and explicit exclusions;
- mappings with a rationale and source evidence; and
- whether each entry is a semantic mapping, a field binding, or a transformation.

The mapping kinds are intentionally separate:

| Kind | Meaning | Example |
| --- | --- | --- |
| `semanticMapping` | An ODPV term and external concept have a reviewed SKOS relationship. | `Dataset` `exactMatch` `dcat:Dataset` |
| `fieldBinding` | An ODPV concept is carried by a field or section in another format. It is not a claim of semantic equivalence. | `SLA` in ODCS `slaProperties` |
| `transformation` | A representation needs a directional conversion or an intermediary object. | `produces` represented by PROV generation through an Activity |

Only use `exactMatch` after a review establishes that concepts are interchangeable in the intended scope. Prefer `closeMatch` or a field binding when in doubt. A profile must never promote an external field name into an ODPV term.

## Status and lifecycle

These first profiles are `stable`: their mapping assertions, fixture examples, and SDK conformance support have been reviewed together. A semantic change to a stable mapping is breaking and requires a new profile version.

## SDK integration

The SDK should use the profile id and version as an explicit input. It may validate fields, transform documents, or emit reports, but it must preserve the profile's mapping kind and direction. In particular, it must not present observed lineage as proof of an ODPV value or contract claim.
