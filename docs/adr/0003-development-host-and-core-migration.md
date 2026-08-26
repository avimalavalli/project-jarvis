# ADR-0003: Development Host and Core Migration

- Status: Accepted
- Date: 2026-08-26
- Decision owners: Avi and Project JARVIS engineering

## Context

Early development must use existing hardware. Avi has chosen to develop on the
laptop and use the larger PC for repeatable compatibility and performance tests.
The blueprint requires one persistent JARVIS identity rather than independent
assistants on each device.

## Decision

- The laptop is the initial development host.
- The larger PC is a test target until measured workloads justify promoting it,
  or another measured machine, to the always-on JARVIS Core.
- Both machines test the same reviewed repository commits and public-safe
  configuration contracts.
- Private identity, canonical memory, secrets and audit state have exactly one
  authoritative active home. They are never copied through the public Git
  repository.
- A Core migration requires a verified encrypted backup, restore test, explicit
  cutover, endpoint re-registration and confirmation that the former Core is no
  longer writing canonical state.
- Displays remain optional endpoints. Turning them off cannot make JARVIS
  unusable.
- Hardware purchases remain deferred until workload benchmarks demonstrate a
  specific constraint.

## Consequences

This approach keeps early work inexpensive and portable while preventing the
laptop and PC from becoming divergent assistants. Tests must be repeated on the
larger PC; laptop results cannot be silently treated as PC evidence. Until the
cutover procedure is proven, neither machine is approved as a permanent Core.
