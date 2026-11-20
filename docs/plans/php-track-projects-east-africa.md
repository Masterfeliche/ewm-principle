# PHP Track Projects: Dar es Salaam, Tanzania and East Africa

Project menu for the PHP (Laravel) track, built around problems people in Tanzania and East Africa actually have. Each stage has one core project and alternatives. All run against sandboxes and test data only.

Research date: 20 Nov 2026. Figures marked (press) come from news coverage of the source, not the source document itself. Items marked (general knowledge) were not checked in this research.

## 1. Local facts that shape what to build

| Fact | What it means for a project |
|---|---|
| About 87 million active mobile-money accounts in June 2026; M-Pesa, Mixx by Yas and Airtel Money hold about 89%, M-Pesa 40.6% (press, TCRA) | Mobile money is the payment method. Cards are an extra. |
| Developers usually reach the operators through an aggregator (Selcom, AzamPay, ClickPesa) with one API; direct M-Pesa access needs business registration and can take weeks (third-party guides) | Build against an aggregator sandbox. Check its current terms first. |
| Smartphone penetration about 45%, feature phones about 83% (press, TCRA June 2026) | SMS and USSD matter. Pages must be light and work on slow connections. |
| 68% of SMEs keep records by hand and 27% use formal digital payments; many run on margins under 10% (press, FSDT 2024) | Record keeping is a real gap. Tools must be cheap and simple. |
| Commentary calls for tools in both Kiswahili and English | Every project is bilingual from the start. |
| About 50,000 VICOBA savings groups with 4.4 million clients and TZS 1.5 trillion; only 5–10% of SACCOs are digitised (press) | Group savings and loans are a large, under-served problem. |
| TRA accepts a Virtual Fiscal Device (VFD): software that posts signed XML receipts to TRA; a test host exists; credentials belong to a registered taxpayer (open-source libraries, third-party notes) | A learner cannot get real credentials, so builds a mock TRA service and integrates with that. |
| Personal Data Protection Act: controllers and processors must register; enforcement from April 2026; fines up to TZS 5 billion; breaches must be reported to the commission (press, law-firm notes) | Projects practise data protection: least data, access logs, export and delete. |
| Tanzanian shilling amounts are whole numbers; phone numbers come as `+255…`, `255…` or `07…/06…`; time zone is EAT (general knowledge) | Money as integers, one phone format in storage, dates in EAT. |

Sources: [The Citizen on mobile money](https://thecitizen.co.tz/tanzania/news/national/mobile-money-surge-fuels-cashless-growth-5578364), [TanzaniaInvest Q2 2026](https://tanzaniainvest.com/telecoms/telecom-subscriptions-q2-2026), [Daily News on the TCRA report](https://dailynews.co.tz/tanzanias-digital-rise-what-the-latest-tcra-report-tells-us), [TCRA statistics](https://www.tcra.go.tz/publications/statistics), [aggregator comparison](https://mctaba.com/learn/tanzania/selcom-vs-clickpesa-vs-pesapal-vs-direct-api-tanzania), [ClickPesa integration guide](https://medium.com/clickpesa-engineering-blog/a-practical-guide-to-integration-with-tanzanias-mobile-money-providers-567b6bef1a61), [The Citizen on SMEs going cashless](https://thecitizen.co.tz/tanzania/business/how-tanzania-can-speed-up-smes-cashless-switch-5204060), [Daily News on small traders](https://dailynews.co.tz/how-technology-is-changing-small-traders-lives/), [Daily News on savings groups](https://dailynews.co.tz/savings-groups-become-digital-lending-pipeline/), [The Citizen on SACCOS](https://thecitizen.co.tz/tanzania/business/analysts-upbeat-on-saccos-digitisation-4270988), [TRA EFD/VFD suppliers](https://tra.go.tz/page/efd-vfd-suppliers), [Go TRA VFD library](https://beta.pkg.go.dev/github.com/Golang-Tanzania/tra-vfd), [Beem Laravel package](https://github.com/gowelle/laravel-beem-africa), [PDPC final reminder](https://dailynews.co.tz/pdpc-issues-final-reminder-for-data-registration/), [DLA Piper on Tanzania data protection](https://www.dlapiperdataprotection.com/index.html?t=law&c=TZ).

## 2. Rules every project follows
1. **Bilingual:** Kiswahili and English, switchable.
2. **Light:** usable on a cheap Android phone on a slow connection; no heavy front end before Stage 3.
3. **Money is exact:** integer shillings, every movement recorded, nothing edited in place.
4. **Phones are identity:** one stored format (`+2557…`), operator detected from the prefix.
5. **Sandbox only:** no real money, no real customer data, no real TRA submissions.
6. **Data protection:** collect the least data, log who viewed what, support export and delete.

## 3. Projects by stage

### Stage 1: PHP foundations (command-line tools)

| Project | Problem it solves | You build | You learn |
|---|---|---|---|
| **Core: Mobile-money statement analyser** | People and small shops reconcile income by scrolling through transaction SMS messages | A tool that reads an exported statement (CSV) or a file of pasted M-Pesa, Mixx and Airtel SMS texts and prints totals per month, per sender, and total fees paid | Text parsing and regular expressions, arrays, dates, integer money, tests with messy real-world input |
| Shilingi kwa maneno | Receipts and cheques need the amount in words, in Kiswahili and English | A Composer library: `1250000` → "shilingi milioni moja laki mbili na elfu hamsini" | Algorithms, recursion, packaging, thorough tests |
| Simu | Phone numbers arrive in several formats and break SMS sending | A library that validates Tanzanian numbers, converts to one format and names the operator | String handling, data tables, edge cases |
| Duka day-end report | Shop owners do not know their daily profit | Reads a day's sales CSV and prints sales, cost, profit per item and low-stock items | File handling, grouping, sorting, formatted output |

### Stage 2: Web and database in plain PHP (on a mini-framework you write)

| Project | Problem it solves | You build | You learn |
|---|---|---|---|
| **Core: Daftari la Duka (shop ledger)** | 68% of SMEs keep records by hand; credit given to customers (deni) is tracked in an exercise book and often lost | Login; record sales and expenses; customers who buy on credit, their balances and payments; daily and monthly summary; Kiswahili/English | Routing, sessions, PDO, hashed passwords, CSRF and XSS protection, pagination, translation, deploying to a VPS |
| VICOBA group ledger | Savings groups keep contributions and loans on paper; disputes follow | Members, weekly shares (hisa), loans with interest and fines; treasurer and member roles; each member sees their own statement | Roles, database transactions, money correctness, reports |
| Rent book (general knowledge) | Small landlords track rent and deposits in notebooks | Rooms, tenants, monthly rent due, payments, arrears list | Recurring records, date logic, simple reporting |

### Stage 3: Laravel (roles, queues, API, tests, CI)

| Project | Problem it solves | You build | You learn |
|---|---|---|---|
| **Core: School fees and parent messaging** (general knowledge) | Schools chase fee instalments by phone and paper; parents do not know their balance | Roles for admin, bursar, teacher and parent; fee structures and instalment plans; balances and statements; SMS reminders through a queue (Beem or Africa's Talking sandbox); PDF receipts; a REST API; tests and CI | Eloquent relationships, policies, queues and retries, notifications, PDF generation, API design, Pest tests |
| Bus seat booking (general knowledge) | Upcountry bus tickets are sold from paper seat charts; double-selling happens | Routes, trips, seat maps, booking with a hold timer, agent and admin roles, ticket by SMS | Database locking and transactions (two people booking the same seat), state machines, scheduled jobs |
| Boda delivery dispatch (general knowledge) | Small sellers send goods by motorcycle with no tracking; addresses are landmarks, not street numbers | Orders, rider assignment, status updates by SMS to the customer, landmark-based addresses, rider earnings | Status workflows, events and listeners, notifications, simple maps |
| Dawa stock and expiry (general knowledge) | Small pharmacies lose money on expired stock and stock-outs | Batches with expiry dates, sales that take the oldest batch first, expiry and reorder alerts, roles | Inventory logic, scheduled tasks, reporting queries |

### Stage 4: Production engineering (one Laravel SaaS)

| Project | Problem it solves | You build | You learn |
|---|---|---|---|
| **Core: Duka POS for many shops** | Shops need sales, mobile-money collection and fiscal receipts in one cheap tool | Many shops on one system with data kept apart; payment requests through an aggregator sandbox; webhooks handled safely when they arrive twice or out of order; nightly matching of payments against sales; fiscal receipts sent as signed XML to **a mock TRA service you write yourself**; sales that queue when the connection drops; subscription billing; monitoring with Pulse; data export and delete; an audit log; one package extracted (for example the phone or mobile-money code) | Multi-tenancy, payment integration, idempotency, reconciliation, XML signing, queues at depth, caching, monitoring, package development, data-protection practice |
| Digital VICOBA and SACCO platform | 50,000 groups, mostly on paper | Many groups on one system; contributions by mobile money; full loan lifecycle; a double-entry ledger; statements by SMS; a USSD menu for members on feature phones (simulator) | Double-entry accounting, USSD session handling, financial reporting, tenant isolation |
| Ticketing SaaS for bus operators | Operators each want online sales with their own branding | Stage 3 booking turned multi-operator, with payments, QR tickets and agent commissions | Tenancy, payments, QR generation, commission calculations |

### Stage 5: Scale (stress the Stage 4 system)

| Project | You build | You learn |
|---|---|---|
| **Core: End-of-month rush** | Load-test your Stage 4 system with k6 to a target such as 500 requests a second; replay a storm of duplicate and out-of-order payment webhooks; run it on Octane; fix what breaks (indexes, caching, queue workers, connection limits); add tracing; write a performance report | Finding bottlenecks, worker-mode pitfalls, queue tuning, database performance, observability |
| Slow-network mode | Simulate a poor mobile connection and make every key screen usable under it; measure before and after | Front-end weight, caching, offline queues |
| Going regional | Add Kenya and Uganda: KES and UGX, different operators and phone formats, per-country tax rules | Designing for change; the "transfer" check for the stage gate |

## 4. A recommended path through the menu

One product that grows with you, so each stage builds on the last:

1. **Stage 1:** Mobile-money statement analyser, plus the Simu phone library.
2. **Stage 2:** Daftari la Duka.
3. **Stage 3:** School fees and parent messaging (or bus seat booking if you want the harder database problem).
4. **Stage 4:** Duka POS for many shops, reusing your Stage 1 libraries and Stage 2 ledger ideas.
5. **Stage 5:** End-of-month rush, then going regional.

## 5. Limits to know before building
- **Real payments need a registered business** and the aggregator's approval. Stay in the sandbox until then.
- **Real TRA integration needs a registered taxpayer's credentials** and the official specification from TRA. The signing details here come from open-source code, not TRA documents.
- **Handling real people's data** brings Personal Data Protection Act duties, including registration. Use invented data while learning.
- **Aggregator sandbox terms, SMS prices and sender-ID rules change.** Check each provider's own pages before starting.
- Problems marked (general knowledge) should be confirmed by talking to two or three people who have them. That conversation is itself good practice for building real software.
