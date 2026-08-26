# OpenJarvis and JARVIS Ownership Boundary

Version: 1.0 proposed.

| Capability | OpenJarvis candidate responsibility | JARVIS-owned authority |
|---|---|---|
| Model engines | Backend implementations and engine interfaces | Route policy, budgets, privacy and fallback |
| Agent primitives | Loop/registry mechanics | Identity, mission policy and permissions |
| Tools and MCP | Transport and adapter mechanics | Capability grants, confirmation, verification and audit |
| Retrieval | Loaders and retrieval backends | Canonical memory, provenance, lifecycle and correction |
| Security helpers | Scanners, RBAC helpers and sandbox hooks | Mandatory outer policy boundary and fail-closed defaults |
| Server/API | Internal protocol compatibility | Binding policy, device authentication and remote gateway |
| Events/traces | Local hooks and trace primitives | Durable event vocabulary, audit integrity and retention |
| Skills/connectors | Runtime/loading candidates | Allowlist, provenance, scopes and review |
| Voice/vision | Candidate components in their later phases | Identity, consent, privacy and retention policy |
| Credentials | No accepted authority | OS-vault-backed JARVIS secrets broker |

## Upstream rule

Use adapters, plugins, MCP/tool servers, skills and configuration before any
upstream modification. A fork requires a recorded patch with owner, rationale,
tests, upstream reference and removal condition. The initial patch count is
zero.

## Quarantined until dedicated phase approval

Unrestricted shell/file/browser tools, automatic memory promotion, continuous
operators, external analytics, remote server exposure, unreviewed skills,
connectors, cameras and autonomous self-learning remain disabled.

