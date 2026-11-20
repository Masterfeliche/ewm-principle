# Example: Multi-Tenant Invoice Access

This is an illustrative design exercise, not a drop-in implementation.

## Scenario
A garage-management SaaS has two garages. Both can have an invoice with reference `INV-001`. A staff member authenticated under Garage A requests that invoice.

## Core invariant
A user may access an invoice only when the invoice's tenant/garage identifier matches the tenant associated with the authenticated server-side identity and the user is authorized for the requested action.

## Unsafe pattern
Looking up an invoice by a user-provided reference alone can return another garage's invoice when references are not globally unique. Hiding links in the UI is not authorization.

## Safe conceptual sequence
1. Authenticate the staff member.
2. Resolve their authorized garage membership from trusted server-side identity and membership data.
3. Query the invoice by both invoice reference and authorized garage ID.
4. Apply any additional role / permission rule.
5. Return the result or a consistent not-found / forbidden response according to the product's security policy.
6. Test cross-tenant access, duplicate references, list endpoints, exports, background jobs and direct object identifiers.

## Learning exercise
Write framework-specific pseudocode and tests. Explain why a tenant ID supplied freely by the browser is not sufficient evidence of authorization. Do not assume a specific ORM, framework, or database.
