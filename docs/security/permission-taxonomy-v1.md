# Permission and Action Taxonomy v1

Status: Proposed for Phase 0 approval. Runtime tools remain disabled.

## Universal rules

- Default outcome is deny.
- Grants identify subject, tool, operation, resource scope, issue time, expiry
  and revocation status.
- A confirmation cannot broaden the proposed action after it is shown.
- Retries require the same idempotency key or a new approval.
- Every proposal, denial, approval, execution and verification is audited with
  secrets and private payloads redacted.

## Tiers

| Tier | Meaning | Examples | Required control |
|---|---|---|---|
| 0 — Observe | No side effect; permitted read of non-sensitive or explicitly scoped data | Public research, health status, read an approved project file | Existing read grant and endpoint trust |
| 1 — Reversible local | Low-impact change in a narrow local scope | Create a draft, write inside an approved workspace, launch an application | Session or task capability; verify state |
| 2 — Consequential | External, shared or operational change with meaningful impact | Create calendar event, send a pre-approved low-risk message, modify a repository branch | Exact action preview and explicit confirmation |
| 3 — High impact | Security, production, destructive, financial, legal, physical or sensitive-data action | Delete durable data, production deploy, payment, credential rotation, door/vehicle control | Step-up authentication, explicit confirmation, narrow capability, independent verification and rollback where possible |
| 4 — Prohibited | Outside the current safety envelope | Unrestricted shell, autonomous payments, bypassing security, covert surveillance, self-modifying production code | Blocked; requires a new blueprint/ADR decision before implementation |

## Phase restrictions

- Phase 0: all executable tools disabled.
- Phase 1: permission middleware may be exercised with mock tools only.
- Later phases may enable actions only when their phase gate and dedicated
  adversarial tests pass.
- Email send, locks, payments, cameras and unrestricted agents are not smuggled
  into an earlier tier merely because a provider API makes them easy.

## Mapping requirement

Every tool operation must declare exactly one tier before registration. Missing
or ambiguous mapping prevents registration. Resource sensitivity may raise a
tier but may never lower it.

