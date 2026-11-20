# Stage 3 brief: Fee ledger and parent reminders for a small school

**Track:** PHP (Laravel) · **Mode:** 2, plan together and you write the core logic · **Time:** 3–6 months (estimate) · Read `php-house-rules.md` first.

## The problem
Small private schools bill fees in instalments. Parents pay through a bank or mobile money against a reference number, and the bursar ticks them off in a book or spreadsheet. Parents often do not know their balance, reminders are phone calls, and disputes are settled by searching for old receipts. Larger schools buy a full school system; small low-fee schools do not.

## Goal
A Laravel application a small school could run: fee plans, a ledger per student, reminders by SMS, receipts, and an API. **The app records payments; it never collects money.**

## Build
1. **Roles:** owner, bursar, teacher, parent. Policies decide what each can see and do.
2. **Structure:** academic years, terms, classes, students, guardians (a guardian can have several children; a child can have several guardians).
3. **Fees:** a fee structure per class and year; an instalment plan with due dates; a unique reference number per student.
4. **Payments:** the bursar records a payment or imports a CSV of payments; each is matched to a student by reference; unmatched payments go to a review list.
5. **Statements:** a balance and history per student; an arrears report per class.
6. **Reminders:** queued SMS to guardians before a due date and when in arrears, through the Africa's Talking simulator, in the guardian's language. Each guardian can opt out.
7. **Receipts:** a PDF receipt per payment, generated in a queued job.
8. **API:** a documented REST API (token auth) for students, balances and payments, with pagination.
9. **Quality:** Pest feature tests, Pint, Larastan, a GitHub Actions pipeline that runs them, and a Docker or DDEV setup for local work.
10. **Deployed**, with queue workers and the scheduler running.

## Edge cases you must handle
- The same payment is imported twice.
- A payment arrives with a reference that matches no student, or two students.
- A parent overpays; the credit carries to the next instalment.
- A student changes class mid-year.
- The SMS provider is down: reminders retry, then land in failed jobs, and nobody gets the same reminder twice.
- A parent tries to open another family's statement.
- A fee structure is changed after some parents have paid.

## It works when
- [ ] Every role can do its own work and nothing else; feature tests prove each policy.
- [ ] A student's balance always equals fees due minus payments; no payment is ever edited or deleted.
- [ ] Importing the same file twice changes nothing the second time.
- [ ] No request sends an SMS or builds a PDF directly; both go through the queue.
- [ ] The API has documentation generated from the code, and tests.
- [ ] The pipeline is green on the main branch, and the app is live.
- [ ] Only invented students and guardians are in the system.

## Stretch change (transfer check)
A school asks for sibling discounts: the second child pays 10% less, the third 20% less. Add it without editing past records, and show what happens to a family part-way through the year.

## Rebuild from memory (a week later)
Without looking: write the job that sends one reminder, with retry and a guard against sending twice, and its test using fakes.

## Know before real use
Real pupils' data is children's personal data. A real deployment needs the school's consent arrangements, registration with the data-protection commission, and a registered SMS sender name. Stay on invented data while learning.

## Alternative core project
The **seller order and delivery desk** elective is an equal substitute if you want a problem no existing product dominates.

## Evidence to record
Items for `laravel.routing-controllers`, `laravel.eloquent`, `laravel.validation-auth`, `laravel.api`, `laravel.testing`, `laravel.queues-notifications`, `laravel.frontend`, `core.docker` and `core.ci`. Ask a mentor or peer to review one pull request properly; mark that item `verified_by: human`.
