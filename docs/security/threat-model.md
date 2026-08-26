# Threat Model

Version: 1.0 proposed. P0-GATE-4 remains open until owner review.

## Assets

- JARVIS identity and persona constitution.
- Canonical memory and world state.
- Secrets and delegated capabilities.
- Device identities and active sessions.
- Action permissions and approval evidence.
- Audit history, backups and recovery material.
- Personal communications, files, audio, images and future camera streams.

## Trust boundaries

- Human to endpoint.
- Endpoint to device/session gateway.
- Core to models, including local models.
- Core to retrieved content and memory indexes.
- Policy gateway to tools and external systems.
- Secrets broker to OS credential vault.
- Local system to any cloud provider.
- Running system to skills, packages, models and updates.

## Initial threat register

| Threat | Default treatment | Verification still required |
|---|---|---|
| Prompt injection in web, files, mail or tool output | Mark external content untrusted; it cannot grant capabilities | Adversarial retrieval/tool-output tests |
| Agent/tool bypass | Policy gateway is the sole side-effect path | Entry-point and direct-call bypass tests |
| Memory poisoning or false certainty | Provenance, confidence, contradiction and promotion rules | Memory lifecycle tests |
| Secret leakage | OS vault and broker; redact prompts/logs/audit | Canary-secret tests |
| Excess cloud disclosure | Minimum-context packages and sensitivity policy | Egress inspection tests |
| Unauthorised remote access | Loopback only until device gateway exists | Listener and authentication tests |
| Lost or stolen endpoint | Short sessions and rapid revocation | Enrolment/revocation drill |
| Supply-chain compromise | Pins, hashes, allowlists and reviewed updates | Lockfile/model/skill provenance checks |
| Unsafe retry or duplicate action | Idempotency key and explicit retry policy | Failure-injection tests |
| Camera/physical-world privacy | Disabled until dedicated permissions and visible state exist | Later-phase privacy and disable-mode tests |

## Open work

Owners, likelihood, impact, mitigations, residual risk and review dates must be
assigned before this threat model can satisfy P0-GATE-4.
