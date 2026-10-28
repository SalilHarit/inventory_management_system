# Database architecture decision records

<!-- reading-sequence:start -->
[Previous: Decision register](../decision-register.md) | [Next: ADR 0001: schema evolution](0001-schema-evolution.md)
<!-- reading-sequence:end -->

[Documentation index](../../README.md) | [Project home](../../../README.md) | [Decision register](../decision-register.md) | [Migration workflow](../../../db/README.md)

Each record states context, options, decision, consequences, validation and related migration. Stable IDs are never reused. Supersede old records instead of rewriting the historical rationale.

| ADR | Topic | Status |
| --- | --- | --- |
| [0001](0001-schema-evolution.md) | SQL migrations and decision tracking | Accepted for initial tooling; installed, not database-applied |
| [0002](0002-physical-entry-and-financial-evidence.md) | Physical entry independent of bills | Product requirement accepted; schema proposal unimplemented |

Template:

```text
ID and title:
Date:
Status: proposed / accepted / implemented / superseded
Decision owner and actual contributors:
Problem / context:
Options considered:
Decision and rationale:
Consequences and risks:
Affected tables and invariants:
Migration filename(s):
Validation performed / remaining:
Supersedes / superseded by:
```

Use the [decision register](../decision-register.md) for broader project decisions. These ADRs provide focused database reasoning as specific tables become concrete.

<!-- reading-sequence:start -->
[Previous: Decision register](../decision-register.md) | [Next: ADR 0001: schema evolution](0001-schema-evolution.md)
<!-- reading-sequence:end -->
