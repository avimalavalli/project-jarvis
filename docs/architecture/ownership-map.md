# Phase 0 Service Ownership Map

Version: 1.0 proposed.

This map assigns every major function to one authoritative service or layer.
It is technical ownership, not a deployment instruction; the modules initially
run as a modular monolith.

| Function | Authoritative service/layer | Derived consumers |
|---|---|---|
| Persona and JARVIS identity | Identity | Core, endpoints |
| Active conversation/session | Core | Device gateway, audit |
| Endpoint enrolment and revocation | Device gateway | Core, policy |
| Intent coordination | Core | Router, memory, policy |
| Model selection and fallback | Model router | Core, audit |
| Provider implementation | Model adapter | Model router |
| Canonical personal/world records | Memory | Context, search indexes |
| Minimum-context assembly | Context | Model router |
| Permissions and confirmations | Policy gateway | Tool adapters, audit |
| Side-effect execution | Tool adapter after policy grant | Audit |
| Secret lookup and release | Secrets broker | Approved adapter only |
| Durable security/action history | Audit | Inspector/operations |
| Internal event vocabulary | Events | Core, audit, future proactivity |
| OpenJarvis translation | OpenJarvis adapter | Core/router/tool adapters |
| Retrieval index | Derived index adapter | Context; rebuildable from canonical memory |
| Environment configuration schema | Configuration layer | All modules |
| Backup and restore coordination | Operations layer | Memory, audit, configuration |

## Collision rule

If two modules appear to own the same canonical state, implementation stops and
an ADR resolves the conflict. Caches and indexes must name their authoritative
source and rebuild path.

