# Phase 0 Checklist

Last updated: 2026-08-26

Legend: `[x]` verified, `[~]` draft/partial, `[ ]` open.

## Repository and foundation

- [x] Public-safe repository scaffold prepared and published.
- [x] GitHub repository visibility verified as public and documented in ADR-0002.
- [x] Protected `main` requires pull requests and the `foundation` CI check;
  administrator bypass, force pushes and deletion are disabled.
- [x] Immutable stable and newer OpenJarvis candidate commits resolved.
- [x] Source identity/layout assessment completed without executing upstream code.
- [x] Both exact candidates installed and imported in an isolated keyless Linux sandbox.
- [x] Privacy-safe laptop inventory reviewed; raw evidence remains local/private.
- [x] Laptop-development and larger-PC test/cutover strategy accepted in ADR-0003.
- [x] Fail-closed Windows exact-candidate evaluation harness created and tested statically.
- [ ] Stable and newer immutable OpenJarvis candidates executed and compared.
- [ ] OpenJarvis baseline accepted at an exact commit SHA.
- [x] Upstream patch register created; current patch count is zero.
- [x] Fail-closed dev, staging and production profiles created and schema-tested.
- [ ] Staging and production operating procedures approved.

## Governance and architecture

- [x] Major functions mapped to authoritative services/layers.
- [~] Persona constitution v1 proposed.
- [~] Permission/action taxonomy v1 proposed.
- [~] Canonical memory/world-model v1 proposed.
- [~] Model-routing and device-endpoint contracts proposed.
- [~] OpenJarvis versus JARVIS ownership boundary proposed.
- [~] ADR template and initial foundation ADR drafted.
- [~] Permission, memory, endpoint, route, event and audit schemas drafted.
- [ ] Proposed specifications reviewed and approved.
- [x] Golden scenario/evaluation suite skeleton created.
- [~] Backup/recovery design created; restore drill remains open.
- [ ] Incident and credential-rotation runbooks tested.

## Security and data

- [~] Threat model v1 proposed; owner review remains open.
- [~] Data-classification and retention v1 proposed; owner review remains open.
- [ ] Complete action inventory mapped to approved permission tiers.
- [ ] OS-backed secrets broker proven on Avi's computer.
- [ ] Memory lifecycle, provenance, correction and deletion rules approved.
- [ ] Prompt-injection, tool-bypass, secret-leak and egress tests passed.

## Routing and resilience

- [~] Provider-neutral model-route contract drafted.
- [ ] Zero-paid-key local inference proven on Avi's computer.
- [ ] Cost accounting and daily/monthly limits proven.
- [ ] Quota, outage, network and budget fallback proven.
- [ ] Cloud context minimisation proven.

## Phase 0 exit gates

| Gate | Evidence | Status |
|---|---|---|
| P0-GATE-1 | Every major function belongs to a named service/layer | Evidence drafted; approval open |
| P0-GATE-2 | Every action mapped to an approved permission tier | Open |
| P0-GATE-3 | Canonical memory classes and lifecycle approved | Open |
| P0-GATE-4 | Threat model reviewed and mitigations assigned | Open |
| P0-GATE-5 | Upstream versus JARVIS ownership split approved | Open |

**Phase 1 remains blocked while any gate is open.**
