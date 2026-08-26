# ADR-0002: Public source and private data boundary

- Status: Accepted
- Date: 2026-08-26
- Owner: Avi
- Blueprint constraints: D-003, D-005, D-006, D-008, D-009

## Context

The repository owner chose to make `avimalavalli/project-jarvis` public. Public
source can improve auditability and upstream collaboration, but JARVIS will
eventually handle highly personal information. Repository visibility must never
be confused with permission to publish that information.

## Decision

The application code, non-secret contracts, generic security controls, tests
and architectural decisions may be public.

The following are prohibited from this repository and its issues, pull
requests, Actions artefacts and logs:

- The canonical blueprint PDF unless separately reviewed for publication.
- Personal memory, communications, contacts, routines and private media.
- Credentials, tokens, recovery material and device identities.
- Private runtime configuration, databases, backups and production logs.
- Raw prompts, traces or evaluation fixtures containing personal information.

Private runtime state remains local and encrypted. Secrets remain in the OS
credential vault. If a future deployment needs non-public operational code or
configuration, it receives a separate private repository and an explicit
interface; public and private content are not mixed in one Git history.

## Verification

- CI scans tracked text for common credential patterns.
- `.gitignore` excludes ordinary local secret and runtime files.
- Security review must inspect every new fixture, log and Actions artefact.
- Any suspected disclosure triggers credential rotation and Git-history
  remediation; simply deleting the latest file is not sufficient.

## Consequences

Architecture and safety code may be inspected publicly. Operational discipline
must be stronger because a mistaken commit becomes immediately visible.

