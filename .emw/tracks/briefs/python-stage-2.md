# Stage 2 brief: Michango pledge ledger

**Track:** Python (Django) · **Mode:** 1, you type everything · **Time:** 2–3 months (estimate) · Read `house-rules.md` first.

## The problem
For a wedding, a funeral or a send-off, a committee collects contributions (michango) from relatives, friends and colleagues. People pledge an amount and pay later, often in parts. The mobile operators' products handle the collecting. The pledge list itself (who promised, who has paid, who needs a reminder) is still a notebook and a WhatsApp group, and the treasurer's figures are hard for anyone else to check.

## Goal
A Django app on PostgreSQL where a committee keeps its pledge list and anyone with access can see where things stand. **Payments are recorded, never taken.** The app holds no money and talks to no payment provider; that is what keeps it outside payment rules.

## Build
1. **Events.** An event has a type (wedding, funeral, send-off or other), a date, a target amount and a committee. A user can belong to several events.
2. **Roles per event.** Chair, treasurer and viewer. The chair manages the event and its members; the treasurer records pledges and payments; a viewer only reads. Enforce roles in one place, not by copying checks into every view.
3. **Pledgers.** Name, phone in one international format, and how they prefer to be reached. Collect nothing else.
4. **Pledges and payments.** A pledge is an amount promised by a pledger for an event. A payment is recorded against a pledge with its date, how it was paid (cash, mobile money, bank) and an optional reference. Part payments are normal.
5. **Reminder list.** Pledgers with an unpaid balance, the largest or oldest first, with a ready-to-copy reminder text in the pledger's language. The app sends nothing itself.
6. **Printable report.** Pledged, paid and outstanding per pledger and in total, laid out to print on one or two pages, with the date and who produced it.
7. **Audit log.** Every create, correction and role change is written to a log: who, when, what, before and after. Chairs can read it; nobody can edit it.
8. **Screens.** Django templates with forms. Use HTMX with template partials for at least recording a payment and filtering the pledge list, so the page does not fully reload. Lists are paginated. Pages work on a phone and weigh little.
9. **Admin.** The Django admin set up for a site administrator: search, filters, money records read-only.
10. **Language.** Kiswahili and English, switchable, Kiswahili by default, using Django's translation tools.
11. **Tests.** pytest-django tests for the balance rules and for every role.
12. **Deployed** on a Linux server you set up, behind Gunicorn and a web server, over HTTPS, with the database backed up, debug mode off and secrets read from the environment.

## Edge cases you must handle
- A pledger pays more than they pledged.
- A pledger raises or lowers their pledge after paying part of it.
- Two browser tabs submit the same payment form (it must be recorded once).
- A payment is recorded against the wrong pledger: it is corrected by a reversing entry, never by editing or deleting.
- A viewer changes the address bar or posts a form by hand to record a payment.
- A treasurer of one event types another event's ID into the address bar.
- The same person pledges to two events, or appears twice in one event under two spellings of their name.
- A pledger name containing `<script>`.

## It works when
- [ ] A pledger's balance always equals their pledge minus the sum of their payments, and the event total equals the sum of its pledgers.
- [ ] All money is whole shillings in integer columns; no payment or pledge row is ever updated or deleted.
- [ ] Every role can do its own work and nothing else; tests prove each one, including forged requests.
- [ ] No user can read or change an event they do not belong to; a test proves it.
- [ ] Every change to money or roles has an audit log entry, and a test shows the log cannot be changed through the app.
- [ ] There is no raw SQL built from user input; CSRF protection is on for every form, including the HTMX requests.
- [ ] The list pages make a fixed number of queries however many pledgers there are; you can show how you checked.
- [ ] The app is live with invented events and pledgers only, and the README explains how to install and deploy it.

## Stretch change (transfer check)
A committee asks for pledges in kind (a goat, crates of soda, a hired tent) alongside money. Add them without mixing them into the shilling totals and without editing past records, and show them on the printed report.

## Rebuild from memory (a week later)
Without looking: write the model and the function that record a payment exactly once and write its audit log entry, with tests for a repeated submission and for a viewer's attempt.

## Know before real use
Pledgers' names and phone numbers are personal data. A committee that runs this with real people takes on Personal Data Protection Act duties. The app must stay a record: the moment it collects or holds contributions it enters licensed territory. See the research report named in `house-rules.md`; it is not legal advice.

## Alternative core project
The **Daftari la Duka (shop ledger)** elective is an equal substitute if you want a harder money model (sales, expenses and customer credit).

## Evidence to record
Items for `django.models-orm`, `django.auth-permissions`, `django.forms-templates-htmx`, `django.admin`, `django.testing`, `python.classes-dataclasses`, `python.files-errors`, `core.security-basics`, `core.sql`, `core.http` and `core.linux-deploy`. Ask a mentor or peer to try to break in (another event's data, a forged payment as a viewer, script in a name); mark that item `verified_by: human`. Better still, show the app to someone who has sat on a real committee and write down what they said.
