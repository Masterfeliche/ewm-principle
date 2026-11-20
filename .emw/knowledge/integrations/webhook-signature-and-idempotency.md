---
id: "KB-INT-0001"
title: "Verify webhook signatures and process events idempotently"
status: "proposed"
confidence: "high"
category: "integration"
scope: "shared-framework"
summary: "Treat a payment webhook as untrusted until its signature checks out, store the event id, and make processing safe to repeat and to receive out of order."
context: "Payment providers, mobile-money gateways and other services that report state changes by calling your HTTP endpoint."
problem: "Orders are marked paid twice, marked paid from a forged request, or flip back to pending when events arrive out of order."
root_cause_or_principle: "Providers deliver at least once and retry on timeouts, so duplicates and reordering are normal; the endpoint is public, so anyone can call it."
recommended_approach: "Verify the signature over the raw body with the provider's documented method, reject stale timestamps, record the provider event id with a unique constraint before acting, respond 2xx quickly, and apply state changes only forward (pending to paid, never back)."
alternatives:
  - "Ignore the webhook payload and fetch the authoritative status from the provider API using the id it names"
technologies: ["HTTP webhooks", "Payment gateways"]
versions: []
tags: ["payments", "webhooks", "idempotency", "signatures", "retries"]
applicability: "Any inbound callback that changes money, orders, or other state you cannot easily undo."
evidence:
  - type: "authoritative-source"
    description: "Stripe docs: receive webhook events, verify signatures, handle duplicate events, event ordering is not guaranteed"
    uri: "https://docs.stripe.com/webhooks"
  - type: "authoritative-source"
    description: "Stripe docs: idempotent requests"
    uri: "https://docs.stripe.com/api/idempotent_requests"
limitations:
  - "Signature schemes differ by provider; follow each provider's own documentation, not this summary."
  - "Some local gateways do not sign callbacks; then confirm status with a server-to-server query before acting."
  - "A redirect back to your site is never proof of payment."
related_entries: []
related_adrs: []
source_project: ""
created_at: "2026-11-20"
last_reviewed: "2026-11-20"
review_trigger: "Adopting a new payment provider or a provider changing its signing method."
supersedes: []
superseded_by: ""
---

# Verify webhook signatures and process events idempotently

## Summary
Webhooks arrive more than once, out of order, and possibly forged. Verify, deduplicate, then move state forward only.

## Context and applicability
Payment and mobile-money callbacks, shipping updates, any inbound event that changes durable state.

## Problem or question
Double fulfilment, forged "paid" calls, or a late `pending` event overwriting `paid`.

## Observation / root cause / principle
Stripe's documentation states that endpoints may receive the same event more than once and that delivery order is not guaranteed. The same is true of most providers that retry on timeout.

## Recommended approach
1. Verify the signature over the **raw** request body before parsing, using the provider's library or documented algorithm. Reject old timestamps.
2. Insert the provider event id into a processed-events table with a unique constraint. On conflict, return 2xx and stop.
3. Bind the event to the expected customer, tenant, amount and currency before changing state.
4. Allow only forward transitions. Ignore events that would move an order backwards.
5. Return 2xx fast; do slow work in a queue.
6. Reconcile periodically against the provider's API.

## Alternatives and trade-offs
Fetching status from the provider on every event is simpler to make correct but adds latency and API calls.

## Evidence and provenance
- Stripe webhooks documentation (authoritative source).
- Stripe idempotent requests documentation (authoritative source).

## Limitations and caveats
See frontmatter. Provider specifics override this entry.

## Related knowledge
- `.emw/core/verification-policy.md` (Payment-specific checks)

## Maintenance
- Status is `proposed`: a human reviewer should confirm the sources and change it to `verified`.
