# Implementation plan: lessons for PHP Stages 2–5

**Status:** proposed, 23 Nov 2026 · **Follows:** the Stage 0 and PHP Stage 1 lessons (PR #15)

## 1. Goal and scope
Give PHP Stages 2–5 the same kind of step-by-step lessons that Stage 0 and Stage 1 now have,
so that a learner is taught every skill a stage brief demands before the brief demands it.

**In scope:**
- lesson sets for PHP Stages 2, 3, 4 and 5;
- the tooling that keeps lessons correct and lets learners track progress through them;
- how each set is verified and reviewed.

**Out of scope here:** lessons for the .NET, Go and Python tracks. Section 9 says how this plan
prepares for them.

**Target:** each stage's lessons are merged before the first learner reaches that stage. The
first learner is on Stage 0/1 now, so Stage 2 is needed in roughly 2–4 months, and each later
stage gives 3+ months of slack.

## 2. What the briefs demand that the earlier outline missed
I first sketched a 57-lesson outline for Stages 2–5. Checked line by line against the four
briefs, it left out skills the projects cannot be built without. Every lesson set below is
derived from the brief first, the outline second.

| Stage | Brief requires | Missing from the outline |
|---|---|---|
| 2 | Duplicate form submits recorded once; corrections by reversing entries; balances as sums; per-owner data; pagination; Kiswahili/English switch; migrations from the CLI; backups | Idempotent forms, append-only ledgers, authorization and IDOR, pagination, translation, a migration runner, backup and restore |
| 3 | CSV import that is safe to run twice; an unmatched-payments review list; PDF receipts in queued jobs; scheduled reminders; API docs generated from code; guardian ↔ student many-to-many; deploying with workers and the scheduler | Idempotent import, PDFs, the scheduler, API documentation, deploying workers |
| 4 | A *separate* mock gateway app with controllable failure modes; signed XML receipts; gap-free receipt counters under concurrency; offline sync exactly once; polling stuck payments; per-shop export and delete | Building a mock service, XML signatures, gap-free counters, offline sync, polling |
| 5 | A webhook storm and receipt race *during* the load test; reconciliation after the test; a written report; the go-regional stretch | Turning the storm and race into tests; presenting the report |

## 3. The lessons, stage by stage
New lessons added to cover section 2 are marked ★. Each lesson names the brief item it serves,
so nothing is taught that the project does not need, and nothing the project needs is untaught.

### Stage 2 — Web and database, built by hand (16 lessons, Mode 1)
| # | Lesson | Serves |
|---|---|---|
| 1 | Why OOP: refactor `hesabu` into classes | Classes for everything after |
| 2 | Interfaces, enums, `readonly`, composition, dependency injection by hand | Container, testable handlers |
| 3 | PHP on the web: `php -S`, one front controller, a `Request` object around the superglobals | Framework item 1 |
| 4 | Views that escape by default (XSS) | Framework item 6; the `<script>` edge case |
| 5 | A router with parameters, 404 and 405 | Framework item 2; **the rebuild item** |
| 6 | Middleware: a pipeline, "must be logged in" | Framework item 3 |
| 7 | A small service container | Framework item 4 |
| 8 | Designing the ledger's database; PDO and prepared statements (SQL injection) | Framework item 5 |
| 9 ★ | A migration runner on the command line; transactions | Framework item 5 |
| 10 ★ | Money ledgers: append-only records, reversing entries, balances as sums | App items 2–3; the balance rule |
| 11 | Forms, validation, CSRF middleware, post-redirect-get, ★ duplicate-submit tokens | The CSRF and two-tabs edge cases |
| 12 | Sessions, cookies, `password_hash`, login, session regeneration | App item 1 |
| 13 ★ | Authorization: scoping every query to the owner, IDOR, a second role | "Another owner's ID" edge case; the stretch change |
| 14 ★ | Pagination, translations (Kiswahili default), light pages | App items 5–6 |
| 15 | Config and secrets, error handling and logging; **Debugging 3** (Xdebug in the browser); PHPStan level 5 and Pint | Quality items |
| 16 | Deploying: a Linux server, nginx and PHP-FPM, HTTPS, ★ backups with a tested restore | App item 7 |

### Stage 3 — Laravel and professional habits (20 lessons, Mode 2)
| # | Lesson | Serves |
|---|---|---|
| 1 | Laravel: `artisan`, folder structure, config; what replaces each piece of your Stage 2 framework | Orientation |
| 2 | Routes, controllers, Blade, form requests | Everything after |
| 3 | Eloquent and migrations; Pest with a fresh database from here on | Data, tests |
| 4 | Relationships including many-to-many, eager loading, N+1, factories, seeders | Guardians ↔ students |
| 5 | Authentication with a starter kit; roles, gates, policies, and a test per policy | Item 1 |
| 6 | **Debugging 4:** logs, `tinker`, Telescope | |
| 7 ★ | The fee ledger: immutable payments, balances, database transactions, changing fee structures safely | Items 3–5 |
| 8 ★ | CSV import: validation, matching by reference, safe to import twice, a review list | Item 4 |
| 9 | Queues and jobs: retries, backoff, failed jobs, unique jobs (never two reminders) | Items 6–7 |
| 10 | Notifications and SMS through the Africa's Talking simulator; language per guardian; opt-out | Item 6 |
| 11 ★ | PDF receipts in a queued job; file storage | Item 7 |
| 12 ★ | The scheduler and scheduled commands | Reminders before due dates |
| 13 | REST API: resources, Sanctum tokens, pagination, versioning | Item 8 |
| 14 ★ | API documentation generated from code; API tests | Item 8 |
| 15 | One front end: Livewire or Inertia (see decision D1) | |
| 16 | Team workflow: branches, pull requests, code review; working with AI agents professionally | Human-verified PR review |
| 17 | Local environment with Docker (Sail) or DDEV | Item 9 |
| 18 | CI: GitHub Actions running Pest, Pint and Larastan | Item 9 |
| 19 ★ | Deploying Laravel: queue workers kept alive, the scheduler's cron, safe deploys | Item 10 |
| 20 | Working in an existing codebase: read, trace and fix a messy Laravel app | Junior job reality |

### Stage 4 — Production engineering (19 lessons, Modes 2–3, "case study" format)
| # | Lesson | Serves |
|---|---|---|
| 1 | Domain modelling and architecture decision records for a POS | Planning the system |
| 2 | Multi-tenancy: scoping in one place; tenant-aware jobs, caches and files; an isolation test suite | Item 1 |
| 3 | Concurrency: transactions, locking, `SELECT … FOR UPDATE`, races on stock | Item 2 |
| 4 ★ | Gap-free counters under concurrency | Receipt numbers |
| 5 | Double-entry bookkeeping and reconciliation | Item 5 |
| 6 ★ | Building a separate mock service that fails on demand (late, twice, out of order, never) | Item 3 |
| 7 | Payments: a gateway contract with drivers; a payment state machine | Item 4 |
| 8 | Webhooks: signatures on the raw body, idempotency, out-of-order events; ★ polling stuck payments | Item 4; **the rebuild item** |
| 9 ★ | XML and digital signatures; a mock receipt service | Items 6–7 |
| 10 | Outbound calls: queues, retries, timeouts, a clear final-failure path | All outbound calls |
| 11 ★ | Offline sync exactly once: idempotency keys end to end | Item 8 |
| 12 | Redis caching with a stated invalidation rule per item; rate limiting | Item 9 |
| 13 | Queues in production: Horizon, priorities, tenant-aware jobs | Item 11 |
| 14 | Monitoring: Pulse or Nightwatch, structured logs, audit log, alerts | Item 9 |
| 15 ★ | Per-tenant data export and delete | Item 9; data protection |
| 16 | Security review: OWASP Top 10 against your own system, `composer audit`, secrets | Reviewer sign-off |
| 17 | Reading the framework; extracting and releasing a package | Item 10 |
| 18 | PHPStan level 8 and Rector | Item 11 |
| 19 | Production operations: staging, zero-downtime deploys, migrating live data, a restore drill, incident response | Item 11 |

### Stage 5 — Systems and scale (13 lessons, Modes 2–4, "experiment" format)
| # | Lesson | Serves |
|---|---|---|
| 1 | Writing a performance target; capacity and cost | Item 1 |
| 2 | k6: scripts, ramp-up, thresholds, checks | Item 2; **the rebuild item** |
| 3 | Profiling: OPcache, memory, a slow request | Fixes |
| 4 | The database under load: `EXPLAIN`, indexes, N+1, connection limits and pooling | Things to look for |
| 5 | Caching under load: stampedes and consistency | Things to look for |
| 6 | Queues under load: worker counts, slow providers, isolation | Things to look for |
| 7 ★ | The webhook storm and the receipt race as repeatable tests, with reconciliation after | Items 3–4 |
| 8 | Octane and FrankenPHP: state leaking between requests, worker limits | Item 6 |
| 9 | Scaling out: stateless servers, read replicas, replication lag | Fixes |
| 10 | Tracing with OpenTelemetry across request, job and outbound call | Item 5 |
| 11 | Failure testing: timeouts, retries, circuit breakers | Robustness |
| 12 | Designing for poor connectivity | House rule 8 |
| 13 ★ | Writing and presenting the performance report (teaching it is the M4 evidence) | Item 8 |

**Total: 68 lessons** (16 + 20 + 19 + 13). That is 11 more than the earlier outline, all from section 2.

## 4. The lesson format changes as the learner grows
The Stage 0–1 format (idea → worked example → predict → exercises → bug) is right for Mode 1.
Copying it into Stage 4 would treat a near mid-level engineer like a beginner, which the
research on expertise warns against. The format fades:

| Stages | Format | Worked example | The learner produces |
|---|---|---|---|
| 2 | Same as Stage 1 | Full, on a different problem | All the code |
| 3 | "Plan together" | Partial: the shape, with the core left out | A short plan, then the core logic; the agent may scaffold what was already hand-written once |
| 4 | "Case study" | A failure story from a similar system and the reading to do | A design note or ADR, then the build, then a test that reproduces the failure |
| 5 | "Experiment" | How to measure, not what to change | Hypothesis → measurement → change → measurement |

Every format keeps: a goal, "done when", a planted problem to find, and the evidence command.

## 5. Phases
Each phase is one pull request. Each phase is reviewed and merged before the next begins.

### Phase A — Learn from the first learner (2–3 weeks, running alongside B)
The first real learner is using Stage 0–1 now. Before writing 68 more lessons in the same
format, find out what works.
- Add a short feedback line to each lesson's "Done when": "What was unclear?"
- After about 5 lessons, review the feedback and the time actually taken, and fix the format.
- **Exit:** a list of format changes, applied to Stage 0–1 and adopted for Stage 2.

### Phase B — Tooling (1 PR, before any new lessons)
1. **Lesson progress.** `emw_track.py lesson done <n>` records finished lessons in the stage state,
   and `status` shows "Lesson 5 of 18" and the next lesson's title. Tests included.
2. **Lesson lint in `emw_check`.**
   - the `lessons:` file exists;
   - every lesson has the required sections for its stage's format;
   - every "Record" command names a skill that the stage lists;
   - every relative link resolves.
3. **Code checks in CI.**
   - Every `php` block that starts with `<?php` passes `php -l`.
   - Blocks marked as runnable are executed and their output is compared with the lesson's stated output.
   - The SQL blocks run against SQLite (Stage 0) and MySQL (Stage 2 on).
4. **Exit:** CI fails if a lesson's code stops parsing or its stated output stops matching.

### Phase C — Stage 2 lessons (needed in ~2–4 months)
1. Write the 16 lessons and the README, including a ledger-specific worked example (a different
   business from the shop, for example a church harambee).
2. **Verify** in a Docker environment with PHP 8.4, MySQL and nginx: every worked example runs, and
   every planted bug produces the stated symptom.
3. **Feasibility build.** Build the Stage 2 project privately (see decision D3), using *only* what
   the lessons teach. Anything you have to look up elsewhere is a missing lesson.
4. **Security review** of lessons 4, 8, 11, 12 and 13 by an experienced PHP developer.
5. **Exit:**
   - every brief item maps to a lesson;
   - the feasibility build passes the brief's "It works when";
   - the review comments are resolved;
   - CI is green.

### Phase D — Stage 3 lessons
As Phase C, plus:
- pin and state the Laravel version;
- prepare the "messy existing codebase" for lesson 20, as a separate repository;
- verify against the Africa's Talking simulator;
- an experienced Laravel developer reviews the format change to "plan together".

### Phase E — Stage 4 lessons
As Phase D, plus:
- the mock gateway and mock receipt service from lessons 6 and 9 are built during verification;
- a test for every edge case in the brief;
- the payments, tenancy and XML-signature lessons are reviewed by someone who has run payments in production.

### Phase F — Stage 5 lessons
As Phase E, plus a reference load-test run on stated machine sizes. The lessons quote real
measurements, labelled with the machine and date, never invented numbers.

### Order and dependencies
```
A (feedback) ─┐
B (tooling) ──┴─> C (Stage 2) ─> D (Stage 3) ─> E (Stage 4) ─> F (Stage 5)
```
C can start once B's lint and CI checks are merged. Never write two stages at once: each
stage's feasibility build shapes the next.

## 6. Verification standard (every phase)
- [ ] Every brief requirement and edge case maps to at least one lesson (a table in the stage README).
- [ ] Every code block parses; every runnable block's stated output is the real output.
- [ ] Every "Predict" answer was checked by running it.
- [ ] Every planted bug produces the symptom the lesson describes.
- [ ] Versions are stated (PHP, Laravel, database), with the date checked.
- [ ] A feasibility build exists and passes the brief using only the lessons.
- [ ] A named human reviewer signed off the security-sensitive lessons.
- [ ] `emw_check --strict` and all tests pass in CI.

## 7. Risks
| Risk | Effect | Mitigation |
|---|---|---|
| Laravel and package versions move | Lessons break silently | Pin versions; the CI code checks; a yearly review date in each README |
| Lessons become a course that replaces thinking | Learners copy the worked examples | Worked examples stay on different problems; the format fades from Stage 3; exercises stay hints-only |
| Wrong security advice | Learners ship vulnerable apps | Human security review is an exit gate for Phases C and E |
| Real-provider details change (AzamPay, M-Pesa, TRA) | Integrations fail | Lessons teach against mocks the learner builds; real sandboxes are optional, as in the briefs |
| Deployment needs money (a server, a domain) | Learners get stuck at Stage 2 | Offer a free path (a local VM, or a free tier) next to a paid one; see decision D4 |
| Writing outpaces feedback | 68 lessons in a format that does not work | Phase A first; one stage at a time |

## 8. Decisions needed from the maintainer
| # | Decision | Recommendation |
|---|---|---|
| D1 | Livewire or Inertia as the Stage 3 default front end | **Livewire**: one language, lighter for cheap phones; Inertia as an elective |
| D2 | Database from Stage 2 on | **MySQL/MariaDB**: what most PHP hosting in the region offers; PostgreSQL noted where it differs |
| D3 | Where feasibility builds live | **A private repository**: briefs promise no solution code, so these never go in this repo |
| D4 | Deployment target for lessons | A cheap VPS as the main path, with a free local-VM path for learners without a card |
| D5 | Who does the human reviews | Name at least one PHP and one Laravel reviewer before Phase C starts |

## 9. Preparing for the other tracks
Stage 0 is already shared. From Stage 2 on, the concepts in these lessons are language-neutral:
- **Shared concepts:** HTTP, SQL design, security, ledgers, idempotency, concurrency, queues and load testing.
- **Language-specific:** the code.

When the first non-PHP track gets lessons, move those concept sections into
`.emw/tracks/lessons/core-concepts/` and link them from each language's lessons, rather than
writing them four times. Do not do that extraction now: one track is not enough to know where
the seams are.
