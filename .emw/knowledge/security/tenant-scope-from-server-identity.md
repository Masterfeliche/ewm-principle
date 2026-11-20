---
id: "KB-SEC-0001"
title: "Derive tenant scope from server-side identity on every object access"
status: "proposed"
confidence: "high"
category: "security"
scope: "shared-framework"
summary: "Never trust a client-supplied tenant or object id alone; resolve tenant from the authenticated session and filter every read and write by it."
context: "Multi-tenant web APIs and back offices where several customers share one database or schema."
problem: "An endpoint such as GET /invoices/{id} returns or changes another tenant's record when a user edits the id."
root_cause_or_principle: "Broken object level authorization: the server checks that the user is logged in but not that the object belongs to the user's tenant."
recommended_approach: "Resolve tenant_id from the authenticated principal on the server, apply it as a mandatory filter in the data-access layer (not per controller), and return 404 for objects outside the tenant."
alternatives:
  - "Database row-level security keyed on a session variable set per request"
  - "Schema-per-tenant or database-per-tenant isolation"
technologies: ["Any web backend", "SQL databases"]
versions: []
tags: ["multi-tenancy", "authorization", "idor", "bola"]
applicability: "Any system where more than one customer's data is reachable through the same API or UI."
evidence:
  - type: "authoritative-source"
    description: "OWASP API Security Top 10 (2023), API1 Broken Object Level Authorization"
    uri: "https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/"
  - type: "authoritative-source"
    description: "OWASP Cheat Sheet: Insecure Direct Object Reference Prevention"
    uri: "https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html"
limitations:
  - "Admin and support tooling that legitimately crosses tenants needs a separate, audited path."
  - "Background jobs and exports have no request session; they must carry tenant explicitly and be tested separately."
  - "Unguessable ids (UUIDs) reduce discovery but are not an authorization control."
related_entries: []
related_adrs: []
source_project: ""
created_at: "2026-11-20"
last_reviewed: "2026-11-20"
review_trigger: "A new OWASP API Top 10 edition, or a project adopting row-level security."
supersedes: []
superseded_by: ""
---

# Derive tenant scope from server-side identity on every object access

## Summary
Resolve the tenant from the authenticated session on the server and enforce it on every read and write. A tenant id or object id sent by the client is input, not proof of access.

## Context and applicability
Shared-database multi-tenant systems: SaaS back offices, ERPs, invoicing, any API where customers share tables.

## Problem or question
A logged-in user of tenant A requests `/invoices/123`, where invoice 123 belongs to tenant B, and receives it.

## Observation / root cause / principle
OWASP lists this as the top API risk (API1, Broken Object Level Authorization). Authentication succeeded, but nothing checked that the object belongs to the caller's tenant.

## Recommended approach
1. Put `tenant_id` on the server-side principal at login. Never read it from a header, body or query string for authorization.
2. Enforce the tenant filter in one place (repository/data-access layer, ORM global filter, or database row-level security) so a new endpoint cannot forget it.
3. Return 404, not 403, for objects outside the tenant, so ids cannot be probed.
4. Test: the same id across two tenants; direct object access; list, search and export paths; background jobs; admin exceptions.

## Alternatives and trade-offs
- Row-level security in the database gives defence in depth but needs care with connection pooling.
- Schema or database per tenant isolates strongly but costs more to migrate and operate.

## Evidence and provenance
- OWASP API Security Top 10 2023, API1 (authoritative source).
- OWASP IDOR Prevention Cheat Sheet (authoritative source).

## Limitations and caveats
See frontmatter. Cross-tenant admin paths must be explicit and audited.

## Related knowledge
- `.emw/core/verification-policy.md` (Multi-tenancy checks)

## Maintenance
- Review trigger: new OWASP edition.
- Status is `proposed`: a human reviewer should confirm the sources and change it to `verified`.
