# ADR-0001: OpenJarvis foundation strategy

- Status: Proposed
- Date: 2026-08-26
- Owners: Unassigned
- Blueprint constraints: D-003, D-004, D-005, D-006, OJ-001, OJ-002, OJ-003

## Context

OpenJarvis provides useful model-engine, agent, tool, MCP, memory-retrieval and
observability primitives. Its documented defaults and abstractions do not form
the complete JARVIS security, identity, secrets or canonical-memory boundary.

## Proposed decision

Use one exact OpenJarvis commit behind `adapters/openjarvis`. Keep upstream
unmodified. Create a fork only after a required patch is proven impossible to
deliver through an adapter, plugin, MCP/tool server, skill or configuration.

JARVIS owns identity, policy enforcement, secrets, canonical memory, device
trust, cost limits, data minimisation and durable audit.

## Candidates

- Stable release tag `v1.0.2`; exact commit still to be resolved and tested.
- Newer candidate commit `ccd66d5f13e61a70ed8b85f17686cdf967341850`;
  runtime and security tests still required.

## Verification required before acceptance

- Reproducible isolated install on Avi's computer.
- Zero-key local inference smoke test.
- No executable tools, connectors or automatic memory in evaluation mode.
- Loopback-only listener and no unapproved egress.
- External analytics disabled and no plaintext credential file created.
- Upstream tests plus JARVIS boundary/security tests pass.
- Windows compatibility, local performance and patch burden recorded.

## Reversal

The adapter contract permits replacing OpenJarvis without changing JARVIS Core
contracts or canonical data.

