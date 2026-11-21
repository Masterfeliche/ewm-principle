# Stage 4 brief: Payment reconciliation system

**Track:** Go · **Mode:** 2, moving to 3 for skills you have proved · **Time:** 6–12 months (estimate) · Read `house-rules.md` first.

## The problem
A business sells things and is paid by mobile money. Its sales system says one thing and the payment notifications say another: a customer paid but no sale was recorded, a sale was recorded but the payment never arrived, the amount differs, the same notification came three times. A missed notification does not reverse the money; it leaves the transaction for someone to reconcile by hand. That hand work is what this system replaces.

## Goal
A system of several Go services (an API, a worker and a queue between them) that takes in payment notifications from your Stage 3 mock gateway and sales records from a client's system, removes duplicates, matches them, and reports what does not match. **It records and matches only. It never holds, moves or refunds money.**

## Build
1. **Clients.** Several client businesses use one system. Each has its own API key and webhook secret, and its data is kept apart in every query, job and cache entry.
2. **Sales ingestion.** A public HTTP API takes sales records one at a time or in batches (the client's sale id, the payment reference, amount in whole shillings, time). Every write takes an idempotency key; sending the same request again changes nothing and returns the first answer.
3. **Notification ingestion.** A webhook endpoint receives callbacks from the mock gateway. The signature is verified on the raw body before anything else. The event is stored and acknowledged quickly; the work happens later.
4. **Queue.** Accepted events are published to NATS or Kafka. Storing an event and publishing it cannot come apart: use an outbox or an equivalent you can defend. Consumers are safe to be given the same message again.
5. **Worker.** A separate service consumes events, removes duplicates, applies them to a payment's state (pending, paid, failed, expired, ambiguous) so that the result is the same whatever order they arrive in, and tries to match payments to sales.
6. **Background jobs.** With River or asynq: a job that queries the gateway's status endpoint for payments stuck in pending or ambiguous (the status query wins over a callback), a nightly reconciliation run per client, and report building. Each job has retries and a clear final-failure path. Write down why you chose River or asynq.
7. **Matching.** Match on reference and amount, with stated rules for the cases that do not match cleanly. Every mismatch gets a category: paid with no sale, sale with no payment, amounts differ, duplicate sale, payment after failure, never confirmed. A person can resolve a mismatch with a note; the original records are never edited.
8. **Internal API.** The API service and the worker or matcher talk over gRPC or Connect with a protobuf contract. The public API has an OpenAPI description that is generated from the code or checked against it in CI.
9. **Redis.** Use it for one thing it is good at here (fast duplicate checks, the idempotency-key store, or a cache for the report) and state what happens when it is empty or down. PostgreSQL stays the source of truth.
10. **Report.** An endpoint and a small page per client: totals matched, each mismatch by category, the age of the oldest unresolved item. Kiswahili and English, Kiswahili by default.
11. **Tracing and metrics.** OpenTelemetry traces that follow one notification from webhook to queue to worker to job to database, across services. Metrics for ingest rate, queue lag, job failures, match rate and time to match.
12. **Runtime.** pprof on an internal port only, never the public one. `GOMEMLIMIT` set below each container's memory limit, with the reason for the number. Every service drains on SIGTERM. One profiling write-up: a CPU or heap profile taken under a small storm, what it showed, what you changed.
13. **Delivery.** Each service is a distroless image. CI runs lint, race tests, govulncheck and the contract checks. A staging deployment with compose or on a server, including the mock gateway.
14. **Reading.** Read the routing and middleware code of chi and of Gin, and write one page: how each sits on `net/http`, and what you would have to change in your handlers to move to each.

## Edge cases you must handle
- The same "paid" notification arrives three times.
- "Failed" arrives after "paid" for the same payment.
- No notification ever arrives; the sale exists and the customer says they paid.
- A notification arrives before the sale it belongs to, by seconds or by a day.
- Two sales carry the same payment reference.
- The amounts differ by a small sum, and by a large one.
- A client sends the same batch of sales twice, and sends two different batches with the same idempotency key.
- The worker is killed after applying an event but before acknowledging the message.
- The queue is down for ten minutes while notifications keep arriving.
- Redis is flushed while the system is running.
- A job for client A must never read client B's records (prove it cannot).
- A notification with a valid signature from the wrong client's secret.

## It works when
- [ ] Replaying any notification or any sales request any number of times, in any order, leaves the system in the same state; a test proves it.
- [ ] After a storm from the mock gateway with late, duplicate, out-of-order and missing callbacks, the report explains every mismatch you planted and invents none.
- [ ] Killing any one service at any moment loses no accepted event.
- [ ] No test or query can cross clients.
- [ ] One notification can be followed in a single trace across every service and the queue.
- [ ] A dashboard shows queue lag, job failures, payment states and match rate.
- [ ] No amount is a float anywhere, including in the protobuf and JSON contracts.
- [ ] Nothing in the system can start, move or refund a payment; the README says so in its first paragraph.
- [ ] CI is green, and the OpenAPI and protobuf contracts cannot drift from the code without failing it.

## Stretch change (transfer check)
A second payment source appears: a daily statement file from a bank, with its own columns and reference format. Add it as another source of payment records without changing the matching code or the report.

## Rebuild from memory (a week later)
Without looking: write the consumer function that applies one payment event so that duplicates and out-of-order delivery are harmless, with its table-driven tests for the orderings above.

## Know before real use
Reconciling a real business's payments means handling real customers' phone numbers and payment records, which brings data-protection duties, and connecting to a real provider needs a registered business and a contract with that provider or an aggregator. A reconciliation tool must stay on the recording side of the line: the moment software holds or moves other people's money it needs a licence or a licensed partner. Stay on your mock gateway and invented clients. See `resources/research/East Africa software problems for PHP projects.md`; it is not legal advice.

## Evidence to record
Items for `go.background-jobs`, `go.pgx-sqlc`, `go.project-structure`, `go.lint-vuln`, `go.api-contracts`, `go.messaging`, `go.otel`, `go.profiling`, `go.runtime-tuning`, `go.reading-frameworks`, `core.caching-queues`, `core.observability`, `core.docker`, `core.ci` and `core.linux-deploy`. Ask an experienced developer to review the ingestion, deduplication and client-separation code; mark that item `verified_by: human`.
