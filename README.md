# Project JARVIS

Private, local-first personal intelligence built around one persistent JARVIS
identity across trusted devices.

## Current phase

**Phase 0 — Foundation and governance.** Phase 1 is blocked until all five
Phase 0 gates in `docs/phase-checklists/phase-0.md` are closed with reviewed
evidence.

This repository currently contains control documents, draft contracts, a
zero-capability foundation-evaluation policy, and validation tests. It does not
yet contain a working assistant, enabled tools, cloud credentials, personal
memory, or remote device access.

## Non-negotiable doctrine

- One JARVIS identity; many endpoints.
- Local-first core operation with no mandatory paid API key.
- Replaceable model providers behind a provider-neutral router.
- Deny-by-default tools and minimum privilege.
- Governed canonical memory with provenance and correction.
- Secrets remain outside source, prompts, ordinary memory, logs, and audit.
- Existing PC first; hardware follows measured workloads.
- Reliability and privacy before cinematic presentation.

## Foundation posture

OpenJarvis is being evaluated as a pinned, replaceable engine/agent/tool
substrate. JARVIS owns identity, policy enforcement, secrets, canonical memory,
cost controls, device trust, and durable audit. No upstream version has yet been
accepted.

## Verify the Phase 0 scaffold

```bash
python scripts/check_phase0.py
python -m unittest discover -s tests -v
```

No model download, cloud key, container runtime, or network service is required
for these checks.

