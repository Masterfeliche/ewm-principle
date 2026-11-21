# EMW Learning Tracks Plan (Phase 8)

**Goal:** take a beginner from zero to shipping real software in one of four languages (PHP, .NET, Go, Python), using EMW's modes, ledgers and checks so that progress means "can do it without AI", not "finished a tutorial".

**Basis:** the four research reports in `resources/research/` (20 Nov 2026). Stage durations are estimates for 10–15 hours a week; no source measures them.

## 1. What the research says a track must do

1. **Deploy early.** All four reports found the market pays for skills beginners usually stop before: CI, static analysis, queues, a deployed system with monitoring. So every stage from Stage 2 ends in something deployed.
2. **Make the learner produce the code.** AI help without limits harms learning; hint-only help does not. Early stages run in Mode 1 with `/emw-practice`.
3. **Prove each stage.** A stage is passed by evidence (a shipped project plus checks without AI, one of them seen by a human), not by time spent.
4. **Teach what transfers.** SQL, HTTP, Git, testing, security, Docker, CI and monitoring are the same in all four languages. They are tracked once, as shared core skills, so a second language is much faster.
5. **Space the recall.** Rebuild-from-memory checks at 2 days, 1 week and 1 month.

## 2. Shared structure: six stages

| Stage | Name | Rough time | Ends with | AI mode (default) |
|---|---|---|---|---|
| 0 | Ground floor (same for all tracks) | 2–4 weeks | Git repo, a static page online, first SQL queries | Mode 1 |
| 1 | Language foundations | 2–3 months | A tested command-line tool | Mode 1 |
| 2 | Web and database, built by hand | 2–3 months | A small web app with login, deployed | Mode 1 |
| 3 | Main framework and professional habits | 3–6 months | A deployed multi-role app or API with CI: junior-employable | Mode 2 |
| 4 | Production engineering | 6–12 months | A system with background jobs, caching and monitoring: looks mid-level | Modes 2–3 |
| 5 | Systems, scale and a specialism | 12+ months, ongoing | A load-tested service with a written performance report | Modes 2–4 |

**Stage 0 (shared):** terminal basics, an editor, Git and GitHub, how the web works (HTTP requests, status codes, JSON), HTML and a little CSS, first SQL (`SELECT`, `JOIN`, `INSERT`), reading error messages, asking good questions.

### Shared core skills (tracked once, reused by every track)

| Skill id | Introduced | Target by Stage 3 | Target by Stage 5 |
|---|---|---|---|
| `core.git` | 0 | M3 | M3 |
| `core.http` | 0 | M3 | M4 |
| `core.sql` | 0 | M3 | M4 |
| `core.testing` | 1 | M3 | M4 |
| `core.security-basics` (injection, XSS, CSRF, password storage, secrets) | 2 | M3 | M4 |
| `core.docker` | 3 | M2 | M3 |
| `core.ci` | 3 | M2 | M3 |
| `core.linux-deploy` | 2 | M2 | M3 |
| `core.caching-queues` | 4 | M1 | M3 |
| `core.observability` (logs, metrics, traces) | 4 | M1 | M3 |
| `core.load-testing` | 5 | M0 | M3 |

### Stage gate (same rule for every stage)
A stage is passed when all of these hold:
1. **Shipped:** the stage project meets its brief, is in a public repo with a README, and (from Stage 2) is deployed.
2. **Levels:** every core skill of the stage is at its target level in `skill-ledger.yaml`.
3. **Human-verified:** at least one A0–A2 evidence item per stage is `verified_by: human` (a mentor, lead or peer reviewed the project or watched a check).
4. **Rebuild:** one key piece rebuilt from memory without AI, at least a week after first building it.
5. **Transfer:** one change the learner has not seen before, done at A0–A1.
6. `emw_check` passes.

## 3. The four tracks

Each stage lists what to learn, the project that proves it, and the main free or standard resources from the research.

### PHP track
*Best for: web products, freelance, WordPress and e-commerce. Fastest first results. Few junior openings, so the portfolio must look mid-level.*

| Stage | Learn | Project |
|---|---|---|
| 1 | PHP 8.5/8.6 with `strict_types`; arrays, functions, closures; Composer and PSR-4; first Pest tests | Command-line tool (for example a CSV report generator) with tests |
| 2 | Forms, sessions, cookies; PDO prepared statements; `password_hash`; XSS escaping and CSRF tokens; OOP (interfaces, enums, readonly, exceptions); a hand-built router and small container; PHPStan | Plain-PHP app with login and CRUD on a tiny framework you wrote, deployed on a cheap VPS |
| 3 | Laravel 13: routing, Eloquent, validation, auth and policies, queues, mail; Livewire or Inertia; Sanctum API; Pest 5, Pint, Larastan; Docker or DDEV; GitHub Actions | Deployed multi-role app plus a tested REST API with OpenAPI docs |
| 4 | Laravel in depth: PHPStan level 8+; Redis caching; Horizon queues with retries and idempotency; payments and signed webhooks; Reverb for real-time; Pulse or Nightwatch monitoring; profiling; Rector upgrades; writing a Laravel package; reading the framework source (container, request lifecycle, Eloquent) | Multi-tenant SaaS with billing, or a webhook-ingestion pipeline |
| 5 | Stateless scaling; indexes, replicas, connection pooling; Laravel Octane on FrankenPHP worker mode with leak monitoring; containers or Bref; OpenTelemetry; k6 | Load-tested production service with dashboards and a performance report |

**One framework:** Laravel is the only framework on this track. It is used by 64% of PHP developers and named in about a third of UK PHP job ads, and depth in one framework is worth more to a beginner than half-knowledge of two. The Stage 2 hand-built mini-framework is a one-off exercise to make Laravel's routing, container and middleware understandable, not a second framework. Symfony is an optional elective after Stage 4 for learners heading to enterprise, Drupal or Shopware work ("Symfony: The Fast Track").

Resources: php.net manual, PHP The Right Way, Program With Gio, Exercism PHP, Laracasts "Laravel From Scratch (2026)", the Laravel docs.

### .NET (C#) track
*Best for: salaried enterprise work, ERP and business systems, Azure. Steepest first three months; the platform then covers most of production for you.*

| Stage | Learn | Project |
|---|---|---|
| 1 | C# 14/15 on .NET 10 LTS: types, nullable reference types, collections, LINQ, classes and records, generics, exceptions, first `async/await`; `dotnet` CLI and NuGet; xUnit | Command-line tool with JSON file storage and tests |
| 2 | ASP.NET Core Minimal APIs and Razor Pages; middleware; dependency injection, configuration, logging; EF Core 10 and migrations on PostgreSQL; validation; cookie auth with Identity | Web app with login and CRUD plus a small JSON API, deployed as a Linux container |
| 3 | Integration tests (WebApplicationFactory, Testcontainers); analyzers with nullable warnings as errors; built-in OpenAPI; JWT and policy-based authorization; `dotnet publish` container builds; GitHub Actions; one front end (Blazor or React) | Deployed multi-role app with a CI pipeline |
| 4 | HybridCache and Redis; background services; messaging (Azure Service Bus or RabbitMQ with Wolverine or Rebus); resilience handlers; OpenTelemetry and Aspire; migration bundles; library licence checks (MediatR, AutoMapper, MassTransit are now paid) | Event-driven order or billing pipeline on Azure Container Apps, with tracing |
| 5 | Stateless scale-out; EF Core and SQL performance; connection pooling; Native AOT where it fits; Kubernetes or ACA autoscaling; `dotnet-counters`/`dotnet-trace`; k6 or NBomber | Load-tested service with a performance report; a specialism (Azure, legacy .NET Framework migration, AI services) |

Resources: Microsoft Learn C# paths, Exercism C#, "C# 14 and .NET 10" (Mark Price), Microsoft's ASP.NET Core and EF Core docs, the eShop reference app.

### Go track
*Best for: cloud infrastructure and high-concurrency services; highest UK median pay. Very few junior jobs: most Go developers learned it as a second language. A beginner can take this track, but should expect to enter through cloud or platform roles, or pair it with another track's Stage 3.*

| Stage | Learn | Project |
|---|---|---|
| 1 | Go 1.27: types, slices and maps, structs, interfaces, error wrapping (`errors.Is/As`), packages and modules; table-driven tests; `gofmt`, `go vet` | Command-line tool (for example a log analyser) with tests |
| 2 | `net/http` with the built-in router; JSON; `slog`; `html/template`; `context`; `database/sql` then pgx and sqlc; goose migrations; middleware; sessions or JWT | REST API plus a small server-rendered app on PostgreSQL, standard library only, deployed as one binary |
| 3 | Concurrency: goroutines, channels, `select`, cancellation, `sync`, errgroup; race detector, leak profile, `synctest`; golangci-lint v2, govulncheck; distroless containers; GitHub Actions; Cloud Run or a VPS | Concurrent worker pool or crawler, and the Stage 2 API hardened with CI |
| 4 | gRPC or Connect; OpenAPI generation; background jobs (River or asynq); NATS or Kafka; Redis; OpenTelemetry; pprof; graceful shutdown; `GOMEMLIMIT`; reading chi and Gin code | Multi-service system: API, worker and queue, with tracing |
| 5 | Kubernetes (deploy, then write a small controller); profile-guided optimisation; performance tuning; k6 or vegeta; a distributed-systems build | Load-tested service with a performance report, plus a rate limiter or key-value store; CKAD is the useful certificate |

Resources: A Tour of Go, Go by Example, Exercism Go, "Learning Go" 2nd ed., "Let's Go" and "Let's Go Further", "100 Go Mistakes".

### Python track
*Best for: AI, data, automation and APIs. Most job ads of the four, but mostly AI, data and cloud roles, and the most crowded entry level. The track therefore ends with an AI or data specialism.*

| Stage | Learn | Project |
|---|---|---|
| 1 | Python 3.14/3.15 with uv; data structures, functions, classes and dataclasses, exceptions, files; type hints from day one; pytest; Ruff | Automation command-line tool with tests |
| 2 | Django 6: models and ORM, migrations, auth, forms, templates with HTMX, admin; security defaults; PostgreSQL | Django app with login and CRUD, deployed |
| 3 | FastAPI with Pydantic v2 (pin the version); SQLAlchemy 2 and Alembic; async basics; mypy or pyright; multi-stage Docker builds with uv; GitHub Actions; pip-audit and supply-chain hygiene | Tested API service with OpenAPI docs and CI, deployed |
| 4 | Celery with Redis; caching; connection pooling and PgBouncer; fixing N+1 queries; OpenTelemetry, Sentry, structured logs; Gunicorn/Uvicorn worker models | Background pipeline in production (webhook ingest or report generation) with monitoring |
| 5 | Async and the GIL in depth, free-threaded builds, profiling with py-spy; Locust; a specialism: LLM applications with evaluation, or data engineering | Load-tested service with a performance report, plus an LLM-backed feature with an evaluation suite |

Resources: official Python tutorial, CS50P, "Automate the Boring Stuff" 3rd ed., Exercism Python, the Django tutorial, FastAPI docs, "Architecture Patterns with Python", "Fluent Python" 2nd ed.

## 4. How the tracks differ

| | PHP | .NET | Go | Python |
|---|---|---|---|---|
| Hardest stage for a beginner | 4 (static analysis, queues) | 1–2 (types, async, DI up front) | 3 (concurrency) | 3–4 (types, async, deployment) |
| First deployed app | Stage 2, cheap VPS | Stage 2, container | Stage 2, single binary | Stage 2, PaaS or VPS |
| Framework arrives | Stage 3 (Laravel) | Stage 2 (ASP.NET Core is the platform) | Never fully: standard library first | Stage 2 (Django), Stage 3 (FastAPI) |
| Job-ready point | End of Stage 3, portfolio must show Stage 4 habits | End of Stage 3 | End of Stage 4 for most roles | End of Stage 3, stronger with a Stage 5 specialism |
| Second-language shortcut | Stages 0–2 core skills carry over; Stage 1 takes weeks, not months | same | same; this is the usual way into Go | same |

## 5. Rules for AI use on a track
- **Stages 0–2:** Mode 1. The learner types everything; the agent gives hints one step at a time (`/emw-practice`). No complete solutions before an attempt.
- **Stage 3:** Mode 2. Plan together; the learner writes the core logic; the agent may scaffold boilerplate the learner has already written by hand once.
- **Stages 4–5:** Modes 2–3 for new concepts; Mode 4 only for skills already at M3.
- These are set through `mode-policy.yaml` and the skill levels, so `emw_check` enforces them.

## 6. Implementation steps

| Step | Change | Done when |
|---|---|---|
| 8a | Track file format: `.emw/tracks/<track>.yaml` (stages, skills with target levels, project brief path, gate) plus a JSON schema; `core.yaml` for shared skills and Stage 0 | `emw_check` validates a sample track and rejects a stage that names an unknown skill |
| 8b | Write the four track files and Stage 0 from this plan | All four pass the checker |
| 8c | Project briefs: `.emw/tracks/briefs/<track>-stage-N.md` (goal, requirements, edge cases, "works when", stretch change; no solution code) | 20 briefs plus the Stage 0 brief |
| 8d | Onboarding for learners: `/emw-track start <track>` creates a learner repo's skill ledger from the track; `/emw-track` shows current stage, what is next and what is due | A fresh repo started on a track passes `emw_check` |
| 8e | Gate and review checks in `emw_check`: stage gate rule from section 2; recall reviews due at 2 days, 1 week, 1 month | Planted cases: gate passed without human-verified evidence fails; an overdue review warns |
| 8f | Trial: one learner on Stage 0–1 of one track for four weeks; record friction and results as a knowledge entry | Entry written, whatever it shows |

Order: 8a → 8b (PHP first as the reference track) → 8c → 8d → 8e → 8f.

**Status (21 Nov 2026):** 8a is done. 8b and 8c are done for the shared core and all four tracks (`core.yaml`, `php.yaml`, `dotnet.yaml`, `go.yaml`, `python.yaml`, and 21 project briefs plus shared house rules under `briefs/`). The .NET, Go and Python projects come from the same East Africa research and differ from the generic projects in section 3. 8d is done (`.emw/tools/emw_track.py`, Prompt 12, `/emw-track`). 8e is part done: the stage gate is checked by `emw_track.py next`; the 2-day, 1-week and 1-month review schedule is not built. 8f is not started. The PHP project choices follow `resources/research/East Africa software problems for PHP projects.md`, which replaced the generic projects in section 3.

## 7. Open decisions
1. **Which track to build first.** Recommendation: PHP, as the reference, then copy its shape to the other three.
2. **Who verifies.** The gate needs a human. For a solo learner, name a mentor or peer, or use a recorded screen-share reviewed later.
3. **Hours per week.** Durations assume 10–15. A full-time learner could roughly halve Stages 1–3.
