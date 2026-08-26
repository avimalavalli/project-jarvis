# Data Classification and Retention

Version: 1.0 proposed. P0-GATE-3 remains open until owner review.

| Class | Examples | Default location | Cloud use | Retention |
|---|---|---|---|---|
| Public | Published facts and public documents | Local/cache | Allowed when task requires | Source-dependent |
| Internal | Project plans and ordinary operational metadata | Local | Minimum necessary | Purpose-bound |
| Personal | Contacts, routines, goals and communications | Local encrypted store | Explicit policy and minimisation | User-controlled |
| Sensitive | Financial, legal, health, precise location, private media | Local encrypted store | Denied unless explicitly authorised for task | Shortest practical |
| Restricted | Credentials, recovery material, private keys, raw auth tokens | OS credential vault only | Never placed in model context | Until revoked/rotated |

## Canonical memory minimum fields

Every canonical record must include an ID, type, subject, source/provenance,
created and updated times, confidence, sensitivity, retention rule, status,
and links to superseding or contradictory records where applicable.

Derived embeddings and retrieval indexes are rebuildable and are never the
canonical record. Deletion from canonical memory must propagate to derived
stores and backups according to an approved deletion policy.
