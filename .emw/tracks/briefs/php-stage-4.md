# Stage 4 brief: Duka POS for many shops

**Track:** PHP (Laravel) · **Mode:** 2, moving to 3 for skills you have proved · **Time:** 6–12 months (estimate) · Read `house-rules.md` first.

## The problem
A shop needs to record sales, take mobile-money payments and issue fiscal receipts, in one cheap tool that works when the connection is poor. Each of those is hard alone. Together they are a real production system.

## Goal
One Laravel system serving many shops, with their data kept apart, built entirely against **mocks you write** and provider **sandboxes**. Nothing here touches real money or the real tax authority.

## Build
1. **Tenancy.** Many shops on one system. Tenant scoping is enforced in one place, and jobs, caches and files are tenant-aware.
2. **Sales.** Products, stock, a fast sale screen, cash and mobile-money sales, refunds as reversing entries. Reuse your Stage 1 libraries and Stage 2 ledger ideas.
3. **A mock payment gateway (yours).** A separate small app that accepts a payment request and later calls your webhook. It must be able to send callbacks **late, twice, out of order, and not at all**, on demand, because sandboxes do not do this.
4. **Payments.** One `PaymentGateway` contract with drivers: your mock, plus at least one real sandbox (AzamPay, M-Pesa or Airtel) if you can get access. A payment state machine: started, pending, paid, failed, ambiguous. Webhook signatures verified on the raw request body. A command that polls the status of stuck payments.
5. **Reconciliation.** A nightly job that matches payments against sales and lists what does not match.
6. **A mock TRA receipt service (yours).** It issues a token, accepts a signed XML receipt and a daily summary, and rejects bad signatures and repeated receipt numbers.
7. **A fiscal receipt client.** It signs receipt XML, keeps receipt counters correct when several tills sell at once, queues receipts when the service is unreachable, posts the daily summary, and prints a QR code on the receipt.
8. **Offline tolerance.** A sale recorded while offline is queued and synced later, exactly once.
9. **Operations.** Subscription billing per shop (invoices only, no card processing), Pulse or Nightwatch monitoring, an audit log, data export and delete per shop, Redis caching with a stated invalidation rule for each cached item.
10. **A package.** Extract one piece (phone handling, the QR code, or the receipt client) into its own tested Composer package and use it from the app.
11. **Quality.** PHPStan at level 8 or higher, CI, and a staging deployment with Horizon.

## Edge cases you must handle
- The same "paid" webhook arrives three times.
- "Failed" arrives after "paid" for the same payment.
- No webhook ever arrives; the customer says they paid.
- Two tills issue receipts in the same second.
- The receipt service is down for an hour; then comes back.
- A sale synced from offline arrives twice.
- A job for shop A runs with shop B's settings (prove it cannot).
- A shop asks for all its data, then asks for it to be deleted.

## It works when
- [ ] A test suite proves no query, job or cache entry can cross tenants.
- [ ] Replaying any webhook any number of times leaves the system in the same state.
- [ ] Receipt numbers per shop have no gaps and no repeats under concurrent load, shown by a test.
- [ ] Every outbound call (payment, receipt, SMS) goes through the queue with retries and a clear final-failure path.
- [ ] The reconciliation report explains every mismatch you plant.
- [ ] A dashboard shows queue depth, failed jobs, slow requests and payment states.
- [ ] The package has its own tests and a tagged release.

## Stretch change (transfer check)
Add a second payment driver with a different callback format and different status names, without changing the sale or reconciliation code.

## Rebuild from memory (a week later)
Without looking: write the webhook handler that is safe to call repeatedly, with its tests for duplicate and out-of-order delivery.

## Know before real use
Going live needs a registered business, a contract with a payment aggregator, an approved route for fiscal receipts with a taxpayer's credentials, and data-protection registration. The receipt format details available publicly come from community code, not official documents; get the official specification before any real integration.

## Evidence to record
Items for `laravel.multitenancy`, `laravel.payments-webhooks`, `laravel.caching`, `laravel.queues-notifications`, `laravel.monitoring`, `laravel.packages`, `laravel.internals`, `php.static-analysis`, `core.caching-queues` and `core.observability`. Ask an experienced developer to review the payment and tenancy code; mark that item `verified_by: human`.
