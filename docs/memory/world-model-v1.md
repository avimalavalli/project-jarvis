# Canonical Memory and World Model v1

Status: Proposed for Phase 0 approval. No personal data is stored yet.

## Canonical record classes

| Class | Purpose | Examples |
|---|---|---|
| Person | Stable identity and permitted relationship context | Contact, team member, driver, sponsor representative |
| Project | Bounded body of work with state and ownership | Project JARVIS, GridFlow, racing programme |
| Goal | Desired outcome, horizon and success conditions | Career or project objective |
| Commitment | Promise or obligation with owner and due state | Follow-up, task, deadline |
| Decision | Chosen option, rationale, evidence and reversibility | Architecture or career decision |
| Event | Time-bounded occurrence with sources | Meeting, race, message, deployment |
| Resource | Referenced document, file, account or asset | Blueprint, repository, contract |
| Device | Trusted endpoint state | PC, phone, watch, home node |
| Observation | Unconfirmed input awaiting promotion | Extracted claim, sensor event, inferred relationship |

## Record invariants

Every record has a stable ID, type, subject, payload, provenance, confidence,
sensitivity, status, timestamps and retention policy. Applicable records link
to contradictions, predecessors and successors.

`Observation` is not canonical truth. Promotion requires a policy appropriate
to source trust, sensitivity and consequence. Important inferred personal facts
require confirmation or corroboration.

## Lifecycle

1. Ingest source as untrusted evidence.
2. Classify sensitivity and source trust.
3. Extract candidate observations without overwriting canonical records.
4. Detect possible duplicates and contradictions.
5. Promote, quarantine or reject according to policy.
6. Retrieve only the minimum permitted records for a task.
7. Correct by supersession; preserve provenance and audit history.
8. Delete from canonical and derived stores under the approved deletion rule.

## Storage boundaries

- Canonical records live in the JARVIS-owned encrypted store.
- Embeddings, RAG databases and search indexes are derived and rebuildable.
- Secrets never become memory records.
- Raw conversation is not retained indefinitely by default.
- Cloud models never receive unrestricted database access.

## Initial acceptance tests

- Correct and stale facts can coexist without the stale fact winning.
- A correction is traceable to its source and superseded record.
- Deleting a record removes it from derived retrieval results.
- A sensitive unrelated record is not included in a cloud context package.
- Malicious retrieved text cannot promote itself or request a tool action.

