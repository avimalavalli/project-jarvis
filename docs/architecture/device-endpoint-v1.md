# Device Endpoint Contract v1

Status: Proposed for Phase 0 approval.

## Identity rule

Endpoints are authenticated surfaces of one JARVIS identity. They do not own
separate personas or canonical memories.

## Endpoint record

An endpoint declares a stable device ID, device type, trust state, supported
input/output capabilities, owner/shared classification, session expiry and last
seen time. Hardware identifiers and secrets are not exposed to models.

## Trust lifecycle

`pending` → explicit enrolment → `trusted` → optional `suspended` → `revoked`.
A revoked endpoint cannot refresh a session or retrieve private context.

## Session policy

- Sessions are short-lived and bound to endpoint trust and user state.
- Capabilities are granted per endpoint and task, not inherited globally.
- Shared or guest endpoints default to public/non-sensitive output.
- Device loss triggers revocation and credential rotation where applicable.
- Remote access remains disabled until the secure device gateway is built.

## Handoff invariant

Conversation continuity is stored by Core. A handoff transfers a session
reference and permitted context, not a duplicate assistant or full memory dump.

