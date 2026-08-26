# Logical Service Boundaries

Status: Draft for Phase 0 approval.

Project JARVIS begins as a modular monolith. These are contract boundaries, not
an instruction to deploy early microservices.

| Module | Owns | Must not own |
|---|---|---|
| Identity | Persona constitution, one identity, session continuity | Device credentials or tool execution |
| Core | Intent coordination and response lifecycle | Direct side effects or secret values |
| Policy gateway | Capabilities, permission tiers, approvals, idempotency | Model reasoning or business memory |
| Model router | Provider-neutral selection, budgets, fallback, cost records | Provider lock-in or unrestricted memory access |
| Memory | Canonical records, provenance, sensitivity, retention, correction | Credentials or action authority |
| Context | Minimum necessary context packages and trust labels | Canonical truth or permanent retention |
| Device gateway | Enrolment, authentication, sessions and revocation | Independent assistant identities |
| Audit | Redacted, durable security/action/route events | Secret or raw private payload storage |
| Secrets broker | OS-vault references and scoped credential release | Plaintext repository/config persistence |
| OpenJarvis adapter | Translation to the pinned upstream interfaces | JARVIS policy, identity or canonical memory |

## Side-effect invariant

Every request from every interface must pass through the same policy gateway
before reaching any tool. Absence, ambiguity, expiry or validation failure is a
denial. The model may propose an action; it cannot grant itself permission.

## Initial deployment

Core modules run in one local process and use one local canonical database.
Network services bind only to `127.0.0.1`. Separation into independent services
requires measured scaling, fault-isolation or security evidence and a new ADR.

