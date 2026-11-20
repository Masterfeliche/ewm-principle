# Stage 4 brief: Group and small-SACCO records platform

**Track:** .NET (ASP.NET Core) · **Mode:** 2, moving to 3 for skills you have proved · **Time:** 6–12 months (estimate) · Read `house-rules.md` first.

## The problem
Most small SACCOs have no core records system, and savings groups want their own rules and statements their members can check. The research report gives the figures. Proper books, loan arrears and member statements are each manageable alone. Together, for many groups at once, they are a real production system.

## Goal
One ASP.NET Core system serving many groups and small societies, with their data kept apart, built entirely against **a mock gateway you write** and simulators. **It never holds money:** the group's bank or wallet does, and the system records what happened.

## Build
1. **Tenancy.** Many groups on one system. Tenant scoping is enforced in one place, and background work, messages and caches are tenant-aware.
2. **Ledger.** Your Stage 2 ledger on top of a double-entry ledger: a chart of accounts per group, every movement posted as a journal entry that balances, nothing edited after posting.
3. **Loans.** Loan ageing and arrears by age band, and bad-loan and capital ratios as reports. Bands and limits are settings.
4. **A mock payment gateway (yours).** A separate small app that tells your system a member has paid a contribution into the group's account. It must be able to send notifications **late, twice, out of order, and not at all**, on demand, because sandboxes do not do this.
5. **Payment notifications.** One gateway contract with your mock as the first driver. A state machine for each expected contribution: expected, pending, confirmed, failed, ambiguous. Signatures verified on the raw request body. A worker that asks the gateway about stuck items; when a notification and a status answer disagree, the status answer wins. A confirmed notification *records* a contribution in the ledger and does nothing else.
6. **Reconciliation.** A nightly job that matches notifications against ledger entries and lists what does not match.
7. **Statements by SMS** through a simulator, in the member's language, with an opt-out.
8. **Background services.** SMS, status checks and reconciliation run in hosted background services, outside the request, with retries, a clear final-failure path and a clean stop on SIGTERM.
9. **Messaging.** RabbitMQ or Azure Service Bus between the web app and the workers, with an outbox so that a ledger posting and its message never part company.
10. **Outbound calls.** Every HTTP call to the gateway or the SMS simulator goes through the standard resilience handler, with retries switched off for any write that is not safe to repeat.
11. **Caching.** HybridCache with Redis, with a stated invalidation rule for each cached item, and rate limiting on the notification endpoint.
12. **Observability.** OpenTelemetry logs, metrics and traces. An Aspire AppHost that starts the whole system locally (app, workers, database, cache, broker, mock gateway) with its dashboard.
13. **Releases.** An EF Core migration bundle built in CI and run as a one-shot job before the rollout, never from the app's start-up. One schema change done in two steps (expand, then contract). Health checks. A staging deployment as containers.
14. **Operations.** An audit log, and data export and delete per group.
15. **Licence check.** List every NuGet package with its licence in the README. MediatR, AutoMapper and MassTransit became paid products; prefer what the platform ships, and write mediator and mapping code by hand as patterns.

## Edge cases you must handle
- The same "confirmed" notification arrives three times.
- "Failed" arrives after "confirmed" for the same contribution.
- No notification ever arrives; the member says they paid.
- A notification carries a reference that matches no member, or members in two groups.
- The broker delivers the same message twice.
- Two officers post to the same account in the same second.
- A worker is stopped half-way through a batch of statements.
- The SMS simulator is down for an hour, then comes back: nobody gets the same statement twice.
- A job for group A runs with group B's rules (prove it cannot).
- A group asks for all its data, then asks for it to be deleted.

## It works when
- [ ] A test suite proves no query, background job, message or cache entry can cross tenants.
- [ ] Replaying any notification any number of times leaves the ledger in the same state.
- [ ] Every journal entry balances, and each group's trial balance is zero after concurrent postings, shown by a test.
- [ ] No request sends an SMS or calls the gateway directly; both go through background work with retries and a final-failure path.
- [ ] The reconciliation report explains every mismatch you plant.
- [ ] One trace follows a notification from the endpoint through the broker and the worker to the ledger posting.
- [ ] Migrations run only from the bundle, and a release to staging drops no requests.
- [ ] The README lists each package's licence, and nothing in the build needs a paid licence key.

## Stretch change (transfer check)
Add a second gateway driver with a different notification format and different status names, without changing the ledger or the reconciliation code.

## Rebuild from memory (a week later)
Without looking: write the notification handler that is safe to call repeatedly, with its tests for duplicate and out-of-order delivery.

## Know before real use
Holding or moving members' money needs a Bank of Tanzania licence or a licensed partner, and SACCOs are regulated societies with their own reporting rules. A real SMS sender name and real members' data need a registered business and data-protection registration. See `resources/research/East Africa software problems for PHP projects.md`; it is not legal advice.

## Evidence to record
Items for `aspnet.multitenancy`, `aspnet.payment-notifications`, `aspnet.caching`, `dotnet.background-services`, `dotnet.migrations-release`, `dotnet.messaging`, `dotnet.resilience`, `dotnet.observability-aspire`, `core.caching-queues` and `core.observability`. Ask an experienced developer to review the notification, ledger and tenancy code; mark that item `verified_by: human`.
