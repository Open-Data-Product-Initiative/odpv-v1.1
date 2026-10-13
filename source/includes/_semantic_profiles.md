# Interoperability Profiles

ODPV interoperability profiles connect the shared vocabulary to established external standards without redefining either side. A profile is a versioned mapping contract: it identifies the ODPV and external-standard versions, its scope, reviewed mapping assertions, and the direction required for any transformation.

The initial profiles are **draft** semantic artifacts. They are ready for implementation feedback, but a mapping becomes stable only after maintainers review its meaning, examples, and SDK conformance support together.

| Profile | External standard | Intended role |
| --- | --- | --- |
| [`ODPV-DCAT-3`](/profiles/dcat-3.yaml) | [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) | Catalog discovery and federation |
| [`ODPV-ODCS-3`](/profiles/odcs-3.yaml) | [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/) | Contract-semantic bindings |
| [`ODPV-OPENLINEAGE-1`](/profiles/openlineage-1.yaml) | [OpenLineage](https://openlineage.io/docs/spec/object-model/) | Declared and observed lineage alignment |
| [`ODPV-PROV-O`](/profiles/prov-o.yaml) | [PROV-O](https://www.w3.org/TR/prov-o/) | Provenance representation |
| [`ODPV-ODRL-2`](/profiles/odrl-2.yaml) | [ODRL 2.2](https://www.w3.org/TR/odrl-model/) | Rights-policy expression |

The common [profile schema](/schema/odpv.profile.schema.json) and [profile governance guide](/profiles/README.md) define the profile format and the meaning of its mapping types.

## Mapping Types

Profiles use three different mapping types. They must not be conflated.

| Mapping type | Meaning | Example |
| --- | --- | --- |
| `semanticMapping` | A reviewed SKOS relationship between two concepts. | `Dataset` `exactMatch` `dcat:Dataset` |
| `fieldBinding` | An ODPV concept is represented by a field or section in another format. | `SLA` in ODCS `slaProperties` |
| `transformation` | Converting the representation needs direction or an intermediary object. | `produces` to PROV generation through an Activity |

`exactMatch` is reserved for concepts that are interchangeable in the profile's scope. When that cannot be demonstrated, use `closeMatch`, another narrower SKOS relationship, or a field binding instead.

## Ownership Boundary

ODPV owns the semantic profile files, mapping rationale, evidence, and lifecycle. The [Open Data Product Agent SDK](https://github.com/Open-Data-Product-Initiative/odp-agent-sdk) owns profile resolution, validation, transformation, conformance reports, and integration templates.

An SDK implementation MUST retain the profile id, version, mapping type, and direction in its result. In particular, observed OpenLineage events MUST NOT be reported as proof of an ODPV business outcome or data-contract compliance.
