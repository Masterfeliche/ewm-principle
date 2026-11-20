# Modern PHP rewards learners who aim for production

In late 2026 PHP is a mature, strongly typed, annually released language. **PHP 8.6 shipped on 19 November 2026**, and PHP still runs about **68% of websites whose server-side language is known** ([php.net](https://www.php.net/releases/8.6/en.php); [W3Techs](https://w3techs.com/technologies/details/pl-php)). Two frameworks dominate. **Laravel 13** is used by 64% of PHP developers. **Symfony 8.1 / 7.4 LTS** supplies the components that almost everything else, Laravel included, is built on. Around them sits a professional toolchain: Composer 2.10 with malware blocking, PHPStan 2.3, Pest 5 / PHPUnit 13, Rector and PIE. Production runtimes now span two models: classic PHP-FPM, and persistent "worker mode" servers such as FrankenPHP, which became an official PHP Foundation project in 2025. The job market is the weak spot. Demand is stable but weighted toward seniors, and the share of job ads is shrinking: UK permanent ads citing PHP fell from 1.64% to 0.38% of IT ads in two years ([ITJobsWatch](https://www.itjobswatch.co.uk/jobs/uk/php.do)). So the best path for a newcomer has four stages. First, learn modern PHP 8.4+ without a framework, enough to see what frameworks hide. Second, go deep on Laravel. Third, add the professional quality toolchain early. Fourth, finish with a deployed, tested, load-tested system that looks mid-level, because the junior-to-mid jump is where careers now stall.

## PHP 8.6 tops a four-year support ladder that drops 8.2 in six weeks

PHP releases a new minor version every late November. Each branch gets **two years of active support (bug and security fixes) followed by two years of security-only fixes**, and every end date falls on 31 December ([php.net supported versions](https://www.php.net/supported-versions.php)). The source notes quoted these dates in different terms: the language notes used "active support" and the runtimes notes leaned on "security support". Checked against php.net's policy, both sets of figures are the same. The table below gives both columns, with status as of 20 November 2026.

| Branch | Released | Active support ends | Security support ends (EOL) | Status on 20 Nov 2026 |
|---|---|---|---|---|
| 8.1 and older | — | ended | ended | End of life |
| 8.2 | 8 Dec 2022 | 31 Dec 2024 | **31 Dec 2026** | Security only, EOL in 6 weeks |
| 8.3 | 23 Nov 2023 | 31 Dec 2025 | 31 Dec 2027 | Security only |
| 8.4 | 21 Nov 2024 | **31 Dec 2026** | 31 Dec 2028 | Active, moves to security-only in January |
| 8.5 | 20 Nov 2025 | 31 Dec 2027 | 31 Dec 2029 | Active |
| 8.6 | 19 Nov 2026 | 31 Dec 2028 | 31 Dec 2030 | Active (newest) |

Source: [php.net supported versions](https://www.php.net/supported-versions.php); [PHP 8.6 release](https://www.php.net/releases/8.6/en.php); [PHP 8.5 release](https://www.php.net/releases/8.5/en.php).

**A learner starting now should install PHP 8.5 or 8.6.** Treat 8.4 as the floor. PHPUnit 13, Pest 5 and Symfony 8 all require 8.4+ ([phpunit.de](https://phpunit.de/announcements/phpunit-13.html); [Pest 5](https://pestphp.com/docs/pest5-now-available); [Symfony Releases](https://symfony.com/releases)). Nobody has announced whether the next release will be 8.7 or 9.0. RFCs queue some breaking changes for "the next major version", but no PHP 9 date exists ([PHP RFC index](https://wiki.php.net/rfc)).

Real-world adoption lags the release table badly. On Packagist in July 2026, **8.4 was the most-used version at 32%**, followed by 8.3 at 24% and 8.5 at 16%. Only **113 of the top 1,000 packages require an actively supported PHP version** ([stitcher.io](https://stitcher.io/blog/php-version-stats-july-2026)). Across the public web, W3Techs reports roughly 24.5% of PHP sites still on PHP 7 and 7.3% on PHP 5 ([W3Techs](https://w3techs.com/technologies/details/pl-php)). One caution: the W3Techs PHP-8 share and the overall PHP share both read 68.1%, which may be an extraction artefact. That long legacy tail is a career fact in itself, since a great deal of paid PHP work is upgrade work.

### What "modern PHP" means in practice

The language a newcomer learns today has little in common with the PHP 5 that earned its reputation. Each release since 8.0 added a layer:

- **PHP 8.0 (2020):** named arguments, attributes, constructor property promotion, union types, `match`, the nullsafe `?->` operator and a JIT ([php.net 8.0](https://www.php.net/releases/8.0/en.php)).
- **PHP 8.1:** enums, readonly properties, first-class callables and Fibers ([php.net 8.1](https://www.php.net/releases/8.1/en.php)).
- **PHP 8.2:** readonly classes and DNF types, and dynamic properties deprecated ([php.net 8.2](https://www.php.net/releases/8.2/en.php)).
- **PHP 8.3:** typed class constants and `#[\Override]` ([php.net 8.3](https://www.php.net/releases/8.3/en.php)).
- **PHP 8.4:** **property hooks and asymmetric visibility** (`public private(set)`), which remove most getter and setter boilerplate ([php.net 8.4](https://www.php.net/releases/8.4/en.php)).
- **PHP 8.5:** the **pipe operator `|>`**, a built-in URI extension, "clone with" and `#[\NoDiscard]` ([php.net 8.5](https://www.php.net/releases/8.5/en.php)).
- **PHP 8.6:** **partial function application** with `?` placeholders (designed to pair with pipes), `\Time\Duration`, an `Io\Poll` API meant to underpin ReactPHP and AMPHP, `clamp()`, and secure session defaults on out of the box: strict mode, HttpOnly and SameSite=Lax ([php.net 8.6](https://www.php.net/releases/8.6/en.php)).

Not all of this weighs the same in daily work. Most everyday code uses strict types, promotion, enums, readonly, `match`, named arguments and attributes, the last mainly because frameworks lean on them for routing and validation. JIT, Fibers and lazy objects mostly live inside frameworks and libraries. Pipes and partial application will stay rare until 8.5 becomes the common minimum version.

PHP still has **no native generics**. That gap is why static analysis is cultural rather than optional. Collection types such as `array<int, User>` live in docblocks that PHPStan and Psalm enforce, even though the PHPDoc PSRs (PSR-5, PSR-19) remain drafts ([php-fig.org/psr](https://www.php-fig.org/psr/)). The living style standard is **PER Coding Style 3.1**, which replaces PSR-12 and prescribes a fixed file header that includes `declare(strict_types=1)` ([PER Coding Style](https://www.php-fig.org/per/coding-style/)). A useful mental model: modern PHP with PHPStan feels closer to TypeScript with `tsc` than to 2010-era PHP.

The PHP Foundation keeps the language moving on a thin budget. In 2025 its contract developers wrote **42% of php-src commits**, and the Foundation took in about $731K in donations against about $784K in spending ([PHP Foundation 2025 report](https://thephp.foundation/blog/2026/05/27/impact-and-transparency-report-2025/)). That funding reads as fragile next to how much of the web depends on PHP.

## Laravel wins the jobs while Symfony wins the dependency graph

**Laravel 13** (17 March 2026) needs PHP 8.3+. New majors arrive each year around Q1, each with 18 months of bug fixes and 2 years of security fixes. Laravel 12 became security-only in August 2026 ([Laravel 13 release notes](https://laravel.com/docs/13.x/releases)). Laravel 13's headline additions point in two directions:

- **AI-native features:** a first-party AI SDK (agents, embeddings, vector stores) and native pgvector similarity queries.
- **Framework features:** JSON:API resources, origin-aware CSRF middleware, and expanded attribute-based configuration ([Laravel 13 release notes](https://laravel.com/docs/13.x/releases)).

At Laracon US 2026, Taylor Otwell added **Laravel LSP**, a first-party language server ([Laravel News](https://laravel-news.com/laravel-lsp-a-first-party-language-server-announced-at-laracon-us-2026)).

Laravel's official starter kits give a beginner auth, registration and email verification on day one. They come in React, Vue and Svelte versions (on Inertia) and a Livewire/Flux version. The older Breeze and Jetstream kits no longer get updates ([Laravel release notes](https://laravel.com/docs/master/releases)). Behind the open-source framework sits a funded commercial platform: Cloud, Forge, Vapor, Nightwatch and Nova, financed by a **$57M Accel Series A** in 2024 ([Laravel blog](https://blog.laravel.com/accel-invests-57m-into-laravel)). The ecosystem's gravity is visible in downloads. Filament, an admin-panel builder, has 32.5k GitHub stars and 6.8M monthly installs, close to laravel/framework's own 35k stars ([Packagist](https://packagist.org/packages/filament/filament/stats); [GitHub](https://api.github.com/repos/filamentphp/filament)).

**Symfony** has a more predictable calendar. It ships minors every May and November and a major every two years. The current stable release is **8.1** (PHP 8.4+), 8.2 is in beta for November 2026, and **7.4 LTS gets security fixes until November 2029** ([Symfony Releases](https://symfony.com/releases)). Its components are the plumbing of the ecosystem. **symfony/console pulls 39.8M monthly downloads and http-foundation 36.0M, both more than laravel/framework's 27.5M**, because Laravel, Drupal, Shopware and countless tools depend on them ([Packagist console](https://packagist.org/packages/symfony/console/stats); [Packagist http-foundation](https://packagist.org/packages/symfony/http-foundation/stats)). That makes Symfony knowledge the most transferable framework skill in PHP. Its LTS lines run up to four years, against Laravel's two, which explains its appeal for long-lived enterprise systems.

The rest of the field is real but niche:

- **CodeIgniter 4.7, CakePHP 5.4 and Yii 3.0:** mostly maintenance work. Yii2 still out-downloads CakePHP and CodeIgniter.
- **Slim and Mezzio:** small PSR-7/15 APIs.
- **Phalcon, Hyperf and Spiral:** raw speed and coroutines.
- **Tempest 3.0:** the notable newcomer, a PHP-8.5-only framework from February 2026 ([heise](https://heise.de/-11175501)).

Download counts are on [Packagist](https://packagist.org/packages/slim/slim/stats). None is a strong first-framework bet.

The CMS world creates a separate, large pool of PHP work. **WordPress runs 38.5% of all websites and 57.4% of CMS-based sites**, though its share has slid since 2022 ([W3Techs CMS](https://w3techs.com/technologies/overview/content_management)). Drupal CMS 2.0 (January 2026, on core 11.3) ([Drupal.org](https://www.drupal.org/about/announcements/blog)) and Adobe Commerce 2.4.8 (PHP 8.3, supported to April 2028) ([Adobe](https://experienceleague.adobe.com/en/docs/commerce-operations/release/versions)) have far fewer sites but pay for specialist agency and enterprise roles. So does Shopware 6.7, which ships monthly releases ([Shopware](https://www.shopware.com/en/news/features-and-releases/)).

## A 2026 toolchain treats security and static analysis as defaults

Composer is the backbone, and it has become a security tool. **Composer 2.10** (28 May 2026) removes versions flagged as malware from dependency resolution, fails `composer install` when a lock file contains one, and blocks updates to packages with security advisories by default. A single `config.policy` block replaces the older `config.audit` ([Packagist blog](https://blog.packagist.com/composer-2-10-release/)). Advisory blocking first became the default in 2.9 ([Composer 2.9](https://blog.packagist.com/composer-2-9/)). For C extensions, **PIE replaces PECL**. An accepted RFC deprecates PECL, and the PHP manual now points users to PIE ([RFC](https://wiki.php.net/rfc/adopt_pie_deprecate_pecl); [php.net](https://www.php.net/manual/en/install.pecl.intro.php)).

Quality tooling has settled on a clear stack:

- **PHPStan 2.3** (October 2026) is the default static analyser, with levels 0–10. Level 10 treats every `mixed` type strictly ([phpstan.org](https://phpstan.org/blog)). Psalm continues on 6.x ([Psalm](https://psalm.dev/articles/psalm-6)).
- **PHPUnit 13** (February 2026, PHP 8.4+) is the current testing base ([phpunit.de](https://phpunit.de/announcements/phpunit-13.html)).
- **Pest 5** (July 2026) builds on PHPUnit 13. It adds test impact analysis (Laravel Cloud's 19,000-test suite dropped from 3 minutes to 5 seconds), an agent-verification plugin, LLM-output evals and time-balanced CI sharding ([Pest 5](https://pestphp.com/docs/pest5-now-available); [Laravel News](https://laravel-news.com/pest-5)).
- **Pest 4's Playwright-based browser testing** has displaced Dusk for new Laravel projects ([Pest 4](https://pestphp.com/docs/pest-v4-is-here-now-with-browser-testing)).
- **Rector 2.x** handles automated upgrades from PHP 5.3 code all the way to 8.5 ([newreleases.io](https://newreleases.io/project/github/rectorphp/rector/release/2.2.9)).
- **PHP-CS-Fixer** (with `@PER-CS`) and its Laravel wrapper **Pint** handle formatting ([Laravel Pint](https://laravel.com/framework/docs/pint)).
- **Xdebug 3.5** supports PHP 8.5 ([xdebug.org](https://xdebug.org/announcements/2025-12-04)).
- **`shivammathur/setup-php@v2`** is the standard GitHub Actions entry point, offering PHP 8.4–8.6 as stable and installing all of the above ([setup-php](https://github.com/shivammathur/setup-php)).

Taken together, these tools define a CI pipeline a learner should copy from the first framework project onward:

1. `composer validate` and `composer audit`
2. A style check (Pint or PHP-CS-Fixer)
3. `rector --dry-run`
4. PHPStan with a baseline
5. Tests with PCOV coverage
6. Optionally, Infection mutation testing and a separate Playwright job

For local development, Laravel Herd is native on macOS and Windows but does not run on Linux ([herd.laravel.com](https://herd.laravel.com/); [Laravel News](https://laravel-news.com/lerd)). Sail is the official Docker option for Laravel, and DDEV is the framework-agnostic Docker choice ([DDEV comparison](https://laradock.io/docs/laradock-vs-ddev)). XAMPP-style stacks are a poor fit for professional work, since they do not mirror production.

AI tools are now part of the job. **95% of PHP developers had tried an AI tool and 79% an AI coding assistant or agent** by 2025 ([@IT summary of JetBrains](https://atmarkit.itmedia.co.jp/ait/articles/2510/23/news016.html)). Some 2026 freelance postings explicitly ask for Laravel plus Claude experience ([Upwork](https://www.upwork.com/jobs/~022068042665641726663)). The ecosystem is building for this directly: Laravel ships an AI SDK, and Pest 5 includes an Evals plugin for testing LLM output.

## FPM stays the safe default as worker-mode runtimes go mainstream

PHP's classic execution model is **shared-nothing**: Nginx or Apache in front of PHP-FPM with OPcache, and every request starting from a clean slate. Slack's engineers argue this model is an advantage for both developers and operations ([Slack engineering](https://slack.engineering/taking-php-seriously/)). It is also why PHP app servers scale horizontally with little effort, provided sessions, cache and uploads live outside the server: in Redis or Valkey, a shared database, or S3.

The 2025–26 shift is toward persistent runtimes that boot the application once and keep it in memory between requests. In May 2025 the PHP Foundation made **FrankenPHP an officially supported project** and moved its code into the PHP GitHub organisation ([PHP Foundation](https://thephp.foundation/blog/2025/05/15/frankenphp/)). Laravel Octane runs on FrankenPHP, RoadRunner, Swoole or Open Swoole. Worker mode changes the rules in three ways ([Laravel Octane docs](https://laravel.com/docs/12.x/octane)):

- Service providers boot only once per worker, so singletons that hold the request or config go stale.
- Static arrays leak memory, so workers restart after 500 requests by default.
- Every deploy must run `octane:reload`.

FrankenPHP's own changelog shows how fast this layer is still moving. Between July and November 2026, its releases fixed worker-mode leaks of session IDs, environment variables, response headers and destructor output. Version 1.13.5 alone patched **17 vulnerabilities**, including non-`.php` files executing as PHP ([FrankenPHP releases](https://github.com/php/frankenphp/releases)). Performance claims deserve the same caution. A detailed 2026 analysis argues that the major runtimes land within 15–20% of each other on realistic database-bound routes. That analysis publishes no raw numbers, and headline vendor benchmarks mostly measure trivial "hello world" routes ([DEV](https://dev.to/gabrielanhaia/frankenphp-vs-roadrunner-vs-swoole-a-production-benchmark-2026-edition-3nja)). The same post flags a new failure mode: long-lived workers multiplied across hosts can exhaust Postgres `max_connections`, which makes PgBouncer or strict worker caps mandatory. JIT barely moves typical web workloads, which are I/O-bound; one WordPress test gained 3–5% ([stitcher.io](https://stitcher.io/blog/jit-in-real-life-web-applications)). Put together, the bottleneck order for most PHP systems is database queries and connections first, cache misses second, and PHP CPU a distant third.

Deployment options run along a spectrum:

- **VPS:** Nginx and FPM, often provisioned by Forge.
- **Containers on Kubernetes:** Wikimedia decommissioned its bare-metal MediaWiki hosts in 2025 and now runs PHP only on Kubernetes ([wikitech-l](https://mail-archive.com/wikitech-l@lists.wikimedia.org/msg96718.html)).
- **Managed PaaS:** **Laravel Cloud** offers scale-to-zero and per-second billing ([Laravel blog](https://laravel.com/blog/your-laravel-cloud-stack-now-scales-to-zero)).
- **Serverless:** **Bref 3.0** on AWS Lambda (February 2026, PHP 8.5, smaller layers) accepts about **250 ms of cold start** in exchange for pay-per-use scaling ([Bref 3.0](https://bref.sh/news/03-bref-3.0); [Bref cold starts](https://bref.sh/docs/environment/cold-starts)).

For observability, OpenTelemetry's PHP distro supports Laravel on PHP 8.1–8.5 ([OpenTelemetry](https://opentelemetry.io/docs/zero-code/php/distro/reference/supported-technologies/)), and Laravel's Nightwatch works with any host ([Laravel](https://laravel.com/blog/announcing-laravel-nightwatch)).

The large-scale case studies teach one lesson. Facebook's HHVM fork bought speed, then dropped PHP compatibility entirely in 2019 ([HHVM blog](https://hhvm.com/blog/2018/09/12/end-of-php-support-future-of-hack.html)). Wikimedia left HHVM once mainline PHP 7 caught up, then rolled out PHP 8.3 by routing a cohort of users by cookie at the edge ([Phabricator T176370](https://phabricator.wikimedia.org/T176370); [T405955](https://phabricator.wikimedia.org/T405955)). Mainline PHP plus caching, a CDN and containers is enough for a top-10 website, so learners should master the boring architecture before reaching for exotic runtimes.

## The market pays for portfolios that look mid-level

PHP's user base is large but no longer growing:

- **18.9% of all developers** use PHP, 8.9% use Laravel and 4% use Symfony ([Stack Overflow 2025](https://survey.stackoverflow.co/2025/technology)).
- About **58% of PHP developers have no plans to switch** languages ([@IT](https://atmarkit.itmedia.co.jp/ait/articles/2510/23/news016.html)).
- UK permanent ads citing PHP numbered 470 in the six months to November 2026, against 1,103 in the same period of 2024, while the **median salary held at £50,000** ([ITJobsWatch](https://www.itjobswatch.co.uk/jobs/uk/php.do)).
- US salary figures vary widely by source, from about $63K at PayScale ([PayScale](https://payscale.com/research/US/Job=PHP_Software_Developer/Salary)) to about $100K at Salary.com ([Salary.com](https://www.salary.com/research/salary/recruiting/php-developers-salary)).
- Freelance rates split sharply: open marketplaces sit around $15–30/hour ([Upwork](https://www.upwork.com/hire/php-developers/cost/)), while vetted senior Laravel contractors reach a $45–54/hour median ([Lemon.io](https://lemon.io/rate-calculator/laravel-developers/)).

The structural problem is the entry rung. A Perforce report found PHP's developer base aging and not being replenished, and firms struggling to hire skilled PHP developers ([IT Brief](https://itbrief.com.au/story/php-firms-face-tougher-hunt-for-skilled-developers)). Yet junior postings are scarce: one small 2026 sample found 669 mid-level PHP postings against 3 junior ones ([MisuJob](https://misujob.com/reports/php/2026-05/)). Broader payroll data shows employment of 22–25-year-olds in AI-exposed occupations running about 19% below trend ([Stanford Digital Economy Lab](https://digitaleconomy.stanford.edu/news/canariesaug26/)). The authors call this descriptive rather than causal, and their dashboard shows recent early-career gains ([dashboard](https://digitaleconomy.stanford.edu/project/canaries-dashboard/)). The net reading: mid- and senior-level PHP talent is under-supplied, and the bottleneck sits between junior and mid. UK employers most often pair PHP with **Laravel (32.8% of ads), JavaScript (32.3%), AWS (27.7%) and SQL (25.5%)** ([ITJobsWatch](https://www.itjobswatch.co.uk/jobs/uk/php.do)).

Certifications barely register in hiring. Laravel has had no official certification since January 2023 ([Laravel News](https://laravel-news.com/laravel-certification-program-is-no-longer-official)). The Zend exam has returned under Perforce at $200 ([Zend](https://www.zend.com/training/php-certification-exam)). The Symfony exam is the one credible framework credential, and it pays off mainly for Symfony-heavy consultancies ([certification.symfony.com](https://certification.symfony.com/)).

### The staged path from zero to scalable systems

No authoritative curriculum exists for PHP, and no data measures how long each stage takes. The sequence below is a synthesis of the market evidence and the structure of the strongest current courses. The durations are my estimates for 10–20 hours of study a week, not sourced figures. Each stage ends in a portfolio artefact, because in this market the artefact matters more than the course certificate.

| Stage | Focus | Prove it with |
|---|---|---|
| **1. Modern PHP foundations** (about 0–3 months) | PHP 8.5/8.6 with `strict_types`. Arrays, functions and closures. The HTTP request cycle, forms, sessions and cookies. PDO prepared statements. `password_hash`. XSS escaping and CSRF tokens. Composer, PSR-4 and Git. Skip `mysql_*`, PSR-2 and pre-2020 tutorials. | A CLI tool, plus a plain-PHP CRUD app with login and no framework |
| **2. OOP and "framework without the framework"** (about 3–6 months) | Classes, interfaces, traits, enums, readonly classes and property hooks. Exceptions. Dependency injection. A hand-built router, container and mini-MVC. PER Coding Style. First PHPUnit/Pest tests and PHPStan. | A tiny framework with tests, which makes framework "magic" legible |
| **3. Laravel in depth** (about 6–12 months) | Laravel 13: routing, Blade, Eloquent, validation, auth and policies, queues, mail, events. One front-end layer (Livewire or Inertia with Vue or React). Sanctum APIs. Pest 5, Pint, Larastan, Docker or DDEV, and a GitHub Actions pipeline. | A deployed, multi-role app and a tested REST API with OpenAPI docs: junior-employable |
| **4. Professional engineering** (about 1–2 years) | SOLID and design patterns. PHPStan at level 8–10. Redis caching. Queues with retries and idempotency. Payments and webhooks. Profiling. Security hardening. Rector-driven upgrades. Symfony 7.4 LTS / 8.x as a second framework: its DI container, Doctrine, Messenger and API Platform. | A multi-tenant SaaS with billing, or a webhook-ingestion pipeline: looks mid-level |
| **5. Systems and scale** (2+ years) | Stateless horizontal scaling. Database indexing, replicas and connection pooling. Octane or FrankenPHP worker mode, with leak monitoring and `max-requests`. Kubernetes or Bref. OpenTelemetry tracing. k6 load tests on realistic routes. A specialism chosen by market: WordPress or WooCommerce, Drupal, Shopware or Adobe Commerce, or high-performance async. | A load-tested production service with dashboards and a written performance report |

The free resources hold up through stage 3:

- **Stage 1:** the [php.net manual](https://www.php.net/manual/en/), [PHP The Right Way](https://phptherightway.com/), [Program With Gio's free series](https://classcentral.com/classroom/youtube-learn-php-the-right-way-full-php-tutorial-for-beginners-advanced-200549) (about 133 videos, ending in build-your-own-framework material), and [Exercism's PHP track](https://exercism.org/tracks/php) (122 exercises with free mentoring).
- **Stage 3:** Laracasts' **[Laravel From Scratch (2026 Edition)](https://laracasts.com/series/laravel-from-scratch-2026)** replaces the archived "30 Days" course and adds testing and deployment.
- **Stage 4:** Fabien Potencier's **[Symfony: The Fast Track](https://symfony.com/book)** is free online in a Symfony 8.1 edition and covers everything from first steps to production with Docker and async queues.

Several classic books predate PHP 8 and need current documentation alongside them. Modern PHP is from 2015, and Domain-Driven Design in PHP is from 2016–17.

## Conclusion

The research points to a counter-intuitive strategy. PHP's biggest risk for a newcomer is not that the language is dying, since it ships ambitious releases every November and runs most of the web. The risk is that the market has stopped paying for the skills beginners usually stop at. Junior work that AI tools can produce now competes with the tools themselves. Meanwhile the scarce, well-paid skills sit exactly where tutorials end: static analysis at high levels, test pipelines, safe upgrades of the 30% of sites on dead PHP versions, and operating stateful worker-mode runtimes without leaks or connection exhaustion. A learner who reaches stage 3 should therefore pull stage 4 and 5 habits forward, such as CI, PHPStan, queues and a deployed system with metrics, rather than collect more framework features.

Two ecosystem shifts are worth watching because they change what "mastery" means. First, worker mode under FrankenPHP is turning PHP from a forgiving shared-nothing language into one where memory and state discipline matter, and its 2026 changelog shows that the runtimes themselves are still learning. Second, frameworks and tools are becoming AI-native: Laravel's AI SDK, pgvector queries and Pest's eval plugins all arrived in 2026. Expect Laravel 14 (around Q1 2027) and the State of PHP 2026 results to show whether these become the new baseline. The open questions remain unresolved: the 8.7-versus-9.0 decision, and whether PHP Foundation funding keeps pace with how central PHP is to the web.
