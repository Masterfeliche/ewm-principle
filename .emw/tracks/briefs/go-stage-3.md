# Stage 3 brief: Mock mobile-money gateway and callback storm

**Track:** Go · **Mode:** 2, plan together and you write the core logic · **Time:** 3–6 months (estimate) · Read `house-rules.md` first.

## The problem
A mobile-money payment is confirmed by a callback that the provider sends later. In real use callbacks arrive late, twice, or never, and a timeout is not a failure. Provider sandboxes do not reproduce these failures, so developers first meet them in production, with real customers. The research report's conclusion is that the most useful thing a learner can build is a mock gateway that misbehaves on purpose.

## Goal
A Go service that accepts payment requests and later calls the caller's webhook, and that can, on demand, deliver callbacks **late, twice, out of order or never**, at a rate you set. It is real infrastructure: learners on the PHP, .NET and Python tracks should be able to run it and test their payment code against it. Inside, it is your concurrency project: a worker pool, cancellation, graceful shutdown, and clean race and leak checks. You also bring your Stage 2 parcel desk up to the same professional standard.

## Build
**The gateway:**
1. **Payment request.** An endpoint accepts a request (amount in whole shillings, payer phone in international format, the caller's own reference, a callback URL) and answers at once with a gateway reference and the status "pending". No money exists anywhere; say so in the response documentation.
2. **Outcome.** Each payment later becomes paid, failed or expired. How long that takes and how often each happens are settings.
3. **Status query.** An endpoint returns the true current state of a payment. When a callback and the status query disagree, the status query is right; document that for your users.
4. **Callbacks.** A bounded worker pool delivers callbacks to the caller's URL with a timeout on every call. A failed delivery is retried with growing delays up to a limit, then recorded as undelivered.
5. **Misbehaviour profiles.** Per caller, and changeable while running, set the share of callbacks that are: delayed (with a range), sent twice or more, sent in the wrong order (for example "failed" after "paid", or an older event after a newer one), and never sent. A seed makes a run repeatable.
6. **Storm.** An admin endpoint starts a storm: a stated number of payments and callbacks at a stated rate for a stated time, and can stop it. Stopping cancels the work promptly.
7. **Signing.** Every callback is signed over the exact bytes of the body with a secret shared with the caller, and carries a timestamp and an event id. Document how a receiver verifies it, and include a tiny receiver in the repository for your own tests.
8. **Durability.** Pending payments and unsent callbacks are stored in PostgreSQL. If the process is killed, on restart nothing that should be delivered is lost; a callback may be sent again after a crash, and you say so.
9. **Graceful shutdown.** On SIGTERM the service stops accepting new requests, lets in-flight deliveries finish within a time limit, leaves the rest stored for the next start, and exits. Every goroutine has a clear way to end.
10. **Observability.** `slog` lines with the payment reference and event id; an endpoint with counts (accepted, delivered, duplicated, delayed, dropped, failed deliveries, pool in use).
11. **Concurrency rules.** `context` is passed everywhere. Shared state is guarded or owned by one goroutine. Time-dependent code (delays, retries, expiry) is tested with a virtual clock, not with real sleeps.

**Professional habits, on both this service and the Stage 2 parcel desk:**
1. A CI pipeline on every push: a format check, `go vet`, golangci-lint v2 with staticcheck, `go test -race -cover`, and govulncheck.
2. A static binary in a distroless container image, built by ko or a multi-stage build, running as a non-root user.
3. Integration tests against a real PostgreSQL in a container.
4. Deployed on a VPS or a container platform, with a compose file so another learner can run gateway, database and sample receiver with one command.
5. A README in Kiswahili and English that another track's learner can follow: how to start it, the request and callback formats, how to verify a signature, and how to turn each kind of misbehaviour on.

## Edge cases you must handle
- The caller's webhook is slow, returns an error, or hangs until your timeout.
- The caller's webhook is down for longer than all your retries.
- The same caller reference is sent in two payment requests (the network dropped and they tried again).
- A storm is stopped half-way; then another is started at once.
- SIGTERM arrives during a storm.
- The process is killed without warning during a storm, then restarted.
- A profile is changed while callbacks for that caller are queued.
- Two workers pick up the same callback.
- A callback URL that points at the gateway itself, or at an internal address.
- More callbacks are due than the pool can send: the backlog is bounded and visible, and memory does not grow without limit.

## It works when
- [ ] `go test -race ./...` is clean, including a test that runs a storm.
- [ ] After a storm ends and the pool drains, the goroutine leak profile shows no leaked goroutines, and the goroutine count returns to its idle level.
- [ ] With a fixed seed, a run delivers the same mix of late, duplicate, out-of-order and missing callbacks each time, and the counts endpoint matches the profile within a tolerance you state.
- [ ] Tests for delays, retries and expiry run in milliseconds of real time.
- [ ] Killing the process mid-storm loses no payment and no due callback, shown by a test or a written procedure.
- [ ] Shutdown finishes within its time limit every time.
- [ ] The sample receiver rejects a callback whose body was changed by one byte.
- [ ] The CI pipeline is green on the main branch for both repositories, and both run from distroless images.
- [ ] A learner from another track (or a peer acting as one) has pointed their own code at your gateway using only the README.

## Stretch change (transfer check)
Add a second callback format with different field names and different status words, chosen per caller, without changing the worker pool or the misbehaviour code. Then add one new kind of misbehaviour you have not built (for example a callback with the right signature but a wrong amount) as a new profile setting.

## Rebuild from memory (a week later)
Without looking: write a bounded worker pool that takes jobs from a channel, stops promptly when its context is cancelled, waits for running jobs on shutdown, and returns the first error, with a test that passes under the race detector.

## Know before real use
This is a test tool. Never present it as a payment service, never give it a real provider's name or branding, and never point it at people's real phone numbers. Real providers differ from each other and from your mock; the timings and rules in the research report come partly from third-party sources, so check each provider's own documentation before any real integration. If you deploy on a platform that only gives a container CPU while a request is in flight, background delivery will starve; read the platform's rules or use a VPS. See `resources/research/East Africa software problems for PHP projects.md` and `resources/research/Go ecosystem mastery path.md`.

## Evidence to record
Items for `go.concurrency`, `go.cancellation-shutdown`, `go.context-logging`, `go.testing`, `go.race-leak-testing`, `go.generics-iterators`, `go.lint-vuln`, `go.containers`, `core.testing`, `core.docker` and `core.ci`. For `go.generics-iterators`, record where you used a type parameter or an iterator in this project and where you decided not to. Ask a mentor or peer to review the worker pool and shutdown code in a pull request and to try to make it leak or race; mark that item `verified_by: human`.
