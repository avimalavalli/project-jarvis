# Risk Register

Last updated: 2026-08-26

| ID | Risk | Severity | Owner | Treatment | Status |
|---|---|---:|---|---|---|
| R-001 | Public `main` could accept uncontrolled changes | High | Avi | Required PR plus `foundation` check; admin bypass, force pushes and deletion disabled | Closed — controls verified |
| R-002 | Existing-PC resources may constrain local inference | High | Avi | Privacy-safe inventory reviewed; run workload benchmarks before choosing models or hardware | Partially mitigated — benchmarks open |
| R-003 | OpenJarvis stable/newer candidates differ | High | Unassigned | Test exact immutable candidates | Open |
| R-004 | Tool/confirmation bypass | Critical | Unassigned | Sole policy gateway plus bypass tests | Open |
| R-005 | Plaintext credential persistence | Critical | Unassigned | OS-vault broker and canary tests | Open |
| R-006 | Retrieval storage mistaken for canonical memory | High | Unassigned | JARVIS canonical schema; derived indexes only | Open |
| R-007 | Telemetry or listener leaks data | High | Unassigned | Telemetry off, loopback and egress tests | Open |
| R-008 | Sandbox unavailable or bypassed | High | Unassigned | Prove isolation; never silently run unsandboxed | Open |
| R-009 | Dependency/model/skill supply-chain drift | High | Unassigned | Pins, hashes, provenance and review | Open |
| R-010 | Cloud budget or quota failure | High | Unassigned | Enforced budgets and local fallback | Open |
| R-011 | Backup, restore and revocation unproven | High | Unassigned | Run documented drills | Open |
| R-012 | Premature hardware/microservices | Medium | Unassigned | Existing PC and modular monolith first | Mitigated by design |
| R-013 | Phase 0 functions lack named owners | High | Avi | Assign accountable owners | Open |
| R-014 | Laptop and larger PC diverge into separate JARVIS identities | Critical | Avi | One canonical state authority; verified backup/restore and explicit Core cutover per ADR-0003 | Mitigated by design; drill open |
| R-015 | Windows-only shell behaviour differs from static/Linux validation | Medium | Project JARVIS engineering | Fail closed, capture actual-PC evidence and add a regression control for each discrepancy | Open — first discrepancy corrected; rerun pending |
