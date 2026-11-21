# Stage 3 brief: Seller order and delivery desk API

**Track:** Python (FastAPI) · **Mode:** 2, plan together and you write the core logic · **Time:** 3–6 months (estimate) · Read `house-rules.md` first.

## The problem
Many sellers in Dar es Salaam take orders on Instagram or WhatsApp. The buyer sends a screenshot as proof of payment, the seller checks it by eye against the phone's messages, hands the buyer's number to a boda rider who phones for directions, and tracks stock from memory. Orders get lost in the messages, the same screenshot is used twice, riders arrive to an unanswered phone, and at the end of the day cash and mobile money do not add up.

## Goal
A FastAPI service that one seller, or one small delivery operator, could run behind a simple client: orders, stock, payment proofs, riders and delivery states, with a documented API. **It is not a rider marketplace, and it records payments; it never collects, holds or pays out money.**

## Build
1. **Stack.** FastAPI pinned to an exact version, Pydantic v2 models for every request and response, SQLAlchemy 2 with typed models, Alembic migrations, PostgreSQL. mypy or pyright with no errors.
2. **Roles.** Owner, assistant and rider, with token authentication. Roles are dependencies, not checks copied into each route. A rider sees only their own deliveries.
3. **Products and stock.** Products with a price and a stock count. Stock moves only through recorded movements (received, reserved, sold, returned, adjusted); the count is the sum of the movements.
4. **Customers.** Name, phone in one international format, and a **saved landmark** per customer (free text such as a stage, a shop or a building, plus the zone) so the rider does not have to phone for directions each time.
5. **Orders.** Capture an order with its lines; reserve stock; compute the delivery fee from a **fee-by-zone** table. An order follows a state machine you draw first: for example new, awaiting payment, paid, assigned, out for delivery, delivered, failed, cancelled. Illegal moves are refused.
6. **Payment proofs.** An order creates an expected payment (amount, method). The seller enters a proof's details (amount, reference, sender, time) or uploads the screenshot and types the details from it. Pasted message text may be read with your Stage 1 parser. The service matches proofs to expected payments and puts anything unclear on a review list.
7. **Riders and delivery.** Assign a rider; the rider marks picked up, delivered or failed with a reason (not reachable, rejected at the door, wrong place). A failed delivery returns the stock.
8. **Reconciliation.** A daily report: orders delivered, mobile money expected against proofs matched, cash each rider collected against cash handed over, and every difference listed.
9. **Status notices.** The buyer gets a notice when the order is confirmed, out for delivery, delivered or failed, in their language, through an **SMS simulator** (the Africa's Talking simulator, or a fake you write). No request sends a notice directly: notices are saved first and sent by a background step with retries.
10. **API quality.** Versioned paths, pagination, consistent error responses, OpenAPI documentation generated from the code with examples.
11. **Tests.** pytest tests against a real PostgreSQL, with fakes for the SMS simulator. Add at least one property-based test (Hypothesis) for the stock or money rules.
12. **Delivery.** A multi-stage Docker build with uv; a GitHub Actions pipeline that runs a locked install, Ruff, the type check, the tests, pip-audit and the image build; migrations run as one step before the new version starts; the service is deployed.

## Edge cases you must handle
- The same proof (same reference) is offered for two different orders.
- A proof's amount is less than, or more than, the order total.
- Two orders for the same amount on the same day, and one proof with no order number on it.
- A reference typed with different spacing or letter case than the original.
- Two requests reserve the last item at the same moment.
- The same "create order" request arrives twice because the network dropped.
- A rider marks delivered an order that is not assigned to them, or one that was already marked failed.
- The buyer does not answer when the rider arrives; the order is tried again the next day.
- An order is cancelled after its payment was matched.
- An uploaded file is not an image, or is far too large.
- The SMS simulator is down: notices retry, and nobody gets the same notice twice.

## It works when
- [ ] Every role can do its own work and nothing else; tests prove each one.
- [ ] Stock on hand always equals the sum of its movements, and never goes below zero under concurrent orders, shown by a test.
- [ ] A proof can be matched to at most one order; money records are never edited or deleted, only corrected by a new record.
- [ ] Repeating any write request with the same idempotency key changes nothing the second time.
- [ ] The reconciliation report explains every mismatch you plant.
- [ ] All money is whole shillings in integers, in the database and in the API.
- [ ] The OpenAPI document is generated from the code, is complete, and a stranger can make a first order from it alone.
- [ ] The pipeline is green on the main branch, including pip-audit, and the service is live.
- [ ] Only invented sellers, customers and riders are in the system, and uploaded screenshots are invented too.

## Stretch change (transfer check)
The seller starts offering cash on delivery with a part payment up front: a deposit by mobile money, the rest in cash to the rider. Add it without editing past records, and show what the reconciliation report says when the rider hands over less than they collected.

## Rebuild from memory (a week later)
Without looking: write the function that matches one payment proof against the open expected payments (exact match, no match, more than one candidate, already used), with its tests.

## Know before real use
Customers' names, phone numbers, landmarks and payment screenshots are personal data, and the research report lists financial transaction data as sensitive. Real use means data-protection registration and a registered SMS sender name. The line between recording a seller's own payments and moving other people's money (for example paying riders out of collected funds) is one the report marks as unclear; get advice before going near it. Stay on invented data while learning.

## Alternative core project
The **fee ledger and parent reminders for a small school** elective is an equal substitute if you prefer a problem with a better-documented workflow.

## Evidence to record
Items for `fastapi.routing-di`, `fastapi.validation-openapi`, `fastapi.auth`, `fastapi.testing`, `python.sqlalchemy-alembic`, `python.async`, `python.supply-chain`, `python.type-hints`, `python.tooling`, `python.testing-pytest`, `core.docker` and `core.ci`. Ask a mentor or peer to review one pull request properly; mark that item `verified_by: human`.
