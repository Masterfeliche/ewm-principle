# Stage 4 brief: Payment notification pipeline

**Track:** Python (FastAPI and Celery) · **Mode:** 2, moving to 3 for skills you have proved · **Time:** 6–12 months (estimate) · Read `house-rules.md` first.

## The problem
The Stage 3 seller checks every payment by eye against a screenshot. A payment provider can send a notification for each payment instead, but notifications arrive late, twice, out of order, or not at all, and a timeout is not a failure. A system that trusts each notification as it arrives will mark orders paid twice, miss payments, and leave the seller with books that do not match the provider's statement.

## Goal
A background pipeline that takes in payment notifications, removes duplicates, matches them to the orders in your Stage 3 system, and reconciles every night, built entirely against **a mock gateway you write**. **It records and matches only. It never holds or moves money**, and nothing here touches a real provider.

## Build
1. **A mock payment gateway (yours).** A separate small service. It accepts a payment request, later calls your notification endpoint with a signed body, answers a status query, and produces a daily statement file. On demand it must send notifications **late, twice, out of order, and not at all**, because sandboxes do not do this.
2. **Ingest.** One endpoint that verifies the signature on the raw request body, stores the notification exactly as received, answers quickly, and hands the work to a Celery task. It does no matching itself.
3. **Deduplicate.** The same notification, however many times it arrives, is processed once. Say which field makes two notifications "the same" and why.
4. **Match.** Each payment is matched to an expected payment in the Stage 3 system by reference, amount and phone. A payment has a state machine you draw first: for example received, matched, unmatched, ambiguous, reversed. A matched payment moves the order on. Unmatched and ambiguous payments go to a review list.
5. **Missing notifications.** A scheduled task finds expected payments with no notification and asks the gateway for their status, waiting between attempts and never retrying at once. Where a notification and a status query disagree, the status query wins.
6. **Nightly reconciliation.** A scheduled task compares the gateway's statement, your stored notifications and your orders, and writes a report listing every difference with a reason.
7. **Retries and dead letters.** Tasks retry with backoff. A task that keeps failing ends in a dead-letter store with its error, does not block the queue, and can be replayed by a command after a fix.
8. **Caching.** Cache at least two things in Redis (for example the zone fee table and the dashboard counts), each with a written rule for when it is invalidated.
9. **Database.** PgBouncer in front of PostgreSQL. Write down the connection sum (replicas × processes × pool size) and show it stays under the database limit. Find and fix the N+1 queries in the reconciliation report and the order lists, with query counts before and after. Schema changes are expand-then-contract and run as one job before deploy.
10. **Monitoring.** OpenTelemetry traces that follow one payment from the ingest request through the task to the database; Sentry for errors; structured logs carrying one correlation id; a dashboard showing queue depth, task failures, dead letters, unmatched payments and the delay between a payment and its match. No personal data in logs or error reports.
11. **Workers.** State how many web processes and Celery workers you run, of which kind, and why. Workers shut down without losing a task.
12. **Quality.** Type checks, tests, CI with pip-audit and locked installs, and a staging deployment with the web service, workers, scheduler, Redis and PgBouncer.

## Edge cases you must handle
- The same "paid" notification arrives three times, two of them at the same moment.
- "Failed" arrives after "paid" for the same payment.
- No notification ever arrives; the customer says they paid.
- A notification arrives for a reference that matches no order, or matches two.
- The amount is less than, or more than, the order total.
- A notification arrives before the order it pays for has been saved.
- A notification with a bad signature, and one with a body that does not parse.
- A worker is killed half-way through a task.
- Redis is unreachable for a minute; then comes back.
- One poisoned notification fails every time it is tried.
- The gateway's status endpoint is down during the missing-notification check.
- The nightly reconciliation runs twice, or runs while notifications are still arriving.

## It works when
- [ ] Replaying any notification any number of times, in any order, leaves the system in the same state, shown by tests.
- [ ] No order is ever marked paid twice or left unpaid when the gateway's statement says paid; the reconciliation report explains every mismatch you plant.
- [ ] The ingest endpoint does no slow work; every outbound call (status query, SMS notice) runs in a task with retries and a clear final-failure path.
- [ ] A dead-lettered task can be inspected and replayed, and replaying it twice does no harm.
- [ ] Each cached item has a written invalidation rule and a test that stale data is not served after a change.
- [ ] The connection sum is written down and holds on staging; each N+1 fix has query counts before and after.
- [ ] One payment can be followed in a trace from request to task to database, and an error in a task reaches Sentry with its correlation id and no personal data.
- [ ] All money is whole shillings in integers; payment records are never edited or deleted, only corrected by a new record.
- [ ] The pipeline is live on staging against the mock gateway, with invented data only.

## Stretch change (transfer check)
Add a second gateway with a different notification format, a different signature scheme and different status names, without changing the matching or reconciliation code.

## Rebuild from memory (a week later)
Without looking: write the task that processes one notification so that it is safe to run repeatedly, with its tests for duplicate, concurrent and out-of-order delivery.

## Know before real use
Receiving real payment notifications needs a registered business and a contract with a payment aggregator, and some aggregators have no sandbox at all: never practise on one. The research report lists financial transaction data as sensitive and says sending personal data abroad needs a permit, which matters for hosted error tracking and logging as well as for the database. Real use also brings data-protection registration. See the report named in `house-rules.md`; it is not legal advice.

## Evidence to record
Items for `python.celery-redis`, `python.db-performance`, `python.telemetry`, `python.worker-models`, `python.supply-chain`, `python.sqlalchemy-alembic`, `core.caching-queues`, `core.observability`, `core.docker`, `core.ci` and `core.linux-deploy`. Ask an experienced developer to review the deduplication and matching code; mark that item `verified_by: human`.
