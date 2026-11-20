# Stage 2 brief: Daftari la Duka (shop ledger)

**Track:** PHP · **Mode:** 1, you type everything · **Time:** 2–3 months (estimate) · Read `php-house-rules.md` first.

## The problem
Many small shops keep sales and expenses in an exercise book, or not at all. Goods sold on credit (madeni) are written on a page that gets lost. Without records the owner cannot see profit, cannot show a lender anything, and may be taxed on an estimate.

## Goal
A web app in **plain PHP, with no framework**, where a shop owner records sales, expenses and customer credit, and sees where the money went. You build the small framework underneath it yourself, so that Laravel is not magic in Stage 3.

## Build
**The mini-framework (yours):**
1. One front controller (`public/index.php`); nothing else is reachable from the web.
2. A router that maps method and path to a handler, with route parameters (`/customers/{id}`).
3. Middleware for "must be logged in" and CSRF checking.
4. A small service container that builds your classes and their dependencies.
5. A database layer on PDO with prepared statements only, and migrations you can run from the command line.
6. A view layer that escapes output by default.

**The app:**
1. Register and log in. Each owner sees only their own shop's data.
2. Record a sale (item, quantity, amount, cash or credit) and an expense (what for, amount).
3. Customers who buy on credit: each has a balance; record payments against it; show who owes what, oldest debt first.
4. A daily summary and a monthly summary: sales, expenses, profit, outstanding credit.
5. Kiswahili and English, switchable, Kiswahili by default.
6. Lists are paginated. Pages work on a phone and weigh little.
7. Deployed on a Linux server you set up, over HTTPS, with the database backed up.

## Edge cases you must handle
- A customer pays more than they owe.
- Two browser tabs submit the same payment form (it must be recorded once).
- A sale is recorded wrongly: it is corrected by a reversing entry, never by editing.
- A logged-in owner types another owner's customer ID into the address bar.
- A form is submitted with a missing or wrong CSRF token.
- A customer name containing `<script>`.

## It works when
- [ ] There is no SQL built by joining strings anywhere; every query is prepared.
- [ ] Passwords are stored with `password_hash`, and sessions are regenerated at login.
- [ ] Every form has CSRF protection, and every output is escaped.
- [ ] One owner can never read or change another owner's records; you have a test or a written check proving it.
- [ ] A customer's balance always equals the sum of their credit sales minus their payments.
- [ ] PHPStan passes at level 5 or higher.
- [ ] The app is live, and the README explains how to install it and how the framework pieces fit together.

## Stretch change (transfer check)
Add a second user role: a shop assistant who can record sales but cannot see profit or delete anything. Do it through your middleware and container, not by copying checks into every handler.

## Rebuild from memory (a week later)
Without looking: write the router again (method, path, parameters, 404), with tests.

## Evidence to record
Items for `php.oop`, `php.http-forms-sessions`, `php.pdo`, `php.routing-di`, `php.static-analysis`, `core.security-basics`, `core.sql`, `core.http` and `core.linux-deploy`. Ask a mentor or peer to try to break in (another owner's data, a forged form, script in a name); mark that item `verified_by: human`. Better still, show the app to one real shop owner and write down what they said.
