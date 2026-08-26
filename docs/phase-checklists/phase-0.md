# Phase 0 Checklist

Last updated: 2026-08-26

Legend: `[x]` verified, `[~]` draft/partial, `[ ]` open.

## Repository and foundation

- [~] Private repository scaffold prepared locally.
- [ ] Private GitHub repository created and visibility verified.
- [ ] Protected `main` and required review/CI configured.
- [ ] Stable and newer immutable OpenJarvis candidates executed and compared.
- [ ] OpenJarvis baseline accepted at an exact commit SHA.
- [x] Upstream patch register created; current patch count is zero.
- [~] Development evaluation policy created.
- [ ] Staging and production profiles approved.

## Governance and architecture

- [~] Logical service boundaries drafted.
- [~] ADR template and initial foundation ADR drafted.
- [~] Permission, memory, endpoint, route, event and audit contracts drafted.
- [ ] Owners assigned and decisions approved.
- [ ] Backup/restore and incident runbooks tested.

## Security and data

- [~] Threat-model skeleton created.
- [~] Data-classification proposal created.
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
| P0-GATE-1 | Named owner for every function and control | Open |
| P0-GATE-2 | Every action mapped to an approved permission tier | Open |
| P0-GATE-3 | Canonical memory classes and lifecycle approved | Open |
| P0-GATE-4 | Threat model reviewed and mitigations assigned | Open |
| P0-GATE-5 | Upstream versus JARVIS ownership split approved | Open |

**Phase 1 remains blocked while any gate is open.**

