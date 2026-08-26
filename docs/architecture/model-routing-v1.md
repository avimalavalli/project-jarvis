# Provider-Neutral Model Routing v1

Status: Proposed for Phase 0 approval.

## Contract

Core submits a provider-neutral request containing task class, required
capabilities, sensitivity, latency target, maximum cost, allowed providers,
local preference, context allowance and fallback policy. Provider-specific
types remain inside adapters.

## Selection order

1. Reject routes that violate sensitivity, endpoint or budget policy.
2. Prefer a capable local model for routine and private work.
3. Use a low-cost cloud model only when allowed and materially useful.
4. Escalate to a frontier model only when task difficulty justifies it.
5. On outage, quota, budget or network failure, select an allowed local route.
6. If no safe capable route exists, return an honest degraded response.

## Cost and evidence

Before dispatch, the router enforces daily and monthly budgets. After dispatch,
it records provider, model, reason, estimated/actual tokens and cost, latency,
error, retry and fallback. Consumer subscriptions are never treated as API
credit.

## Privacy

The context service constructs a minimum-purpose package from permitted records.
Restricted data and secrets are never routed to a model. Sensitive cloud
routing requires explicit policy and audit evidence.

## Replaceability test

Changing provider adapters must not change the Core request contract, JARVIS
identity, canonical memory or action permissions.

