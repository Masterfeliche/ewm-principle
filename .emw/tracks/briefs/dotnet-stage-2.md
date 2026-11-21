# Stage 2 brief: VICOBA group ledger (records only)

**Track:** .NET (C#) · **Mode:** 1, you type everything · **Time:** 2–3 months (estimate) · Read `house-rules.md` first.

## The problem
A savings group meets, members buy shares, pay into the social fund, repay loans and pay fines, and the treasurer writes it all in a book. Members cannot easily check where the money is, and groups have lost whole share-outs when the cash was not where the officials said it was. The research report describes the cases.

## Goal
A web app on **ASP.NET Core with EF Core and PostgreSQL** where a treasurer records each meeting and every member can see their own statement and the group's totals. **The app records money; it never moves or holds it.**

## Build
**The platform pieces (learn each one by using it):**
1. Razor Pages for the screens and a few Minimal API endpoints for JSON.
2. The middleware pipeline in an order you can explain, including one small middleware of your own (for example, a log line per request with the user and the time taken).
3. Your own services registered for dependency injection with the right lifetimes; settings read through the Options pattern; logging through `ILogger`.
4. EF Core 10 with migrations you run from the command line. Money movements go through database transactions.
5. Login with ASP.NET Core Identity and cookies. Two roles: treasurer and member.

**The app:**
1. **Group and rules.** A group with its registration number (a field only), and rules set per group: share price, the most shares a member may buy at one meeting, the loan interest rate, fine types and amounts, the social-fund contribution.
2. **Members.** Name and phone number in one international format. A member logs in and sees only their own statement and the group's totals.
3. **Meetings.** For each meeting the treasurer records share purchases, social-fund contributions, loans given, loan repayments and fines.
4. **Cash count.** At the end of a meeting the treasurer enters the cash counted. The app shows the expected figure beside it and records any difference with a note.
5. **Statements.** A statement per member: shares, social fund, loans and what is still owed, fines.
6. **Share-out sheet.** At the end of the cycle, each member's share-out. Reuse your Stage 1 code.
7. **JSON API.** Read-only endpoints for a member's statement and the group summary. An endpoint called without a login answers 401, not a redirect to the login page.
8. Kiswahili and English, switchable, Kiswahili by default. Lists are paginated. Pages work on a phone and weigh little.
9. **Deployed** as a Linux container built with `dotnet publish`, behind a proxy over HTTPS, with the database backed up and the secrets kept out of the image.

## Edge cases you must handle
- Two browser tabs submit the same repayment form (it must be recorded once).
- An entry is recorded wrongly: it is corrected by a reversing entry, never by editing.
- A member tries to buy more shares than the group's rule allows.
- A repayment larger than what the member owes.
- The cash counted does not match the expected figure.
- A rule is changed mid-cycle: past meetings keep the figures they were recorded with.
- A logged-in member types another member's ID into the address bar.
- A form is submitted with a missing or wrong antiforgery token.
- A member name containing `<script>`.

## It works when
- [ ] There is no SQL built by joining strings anywhere; queries go through EF Core or parameters.
- [ ] Passwords are stored by Identity, and no secret is in the repository or the image.
- [ ] Every form has antiforgery protection, and every output is encoded.
- [ ] A member can never read another member's statement, and only the treasurer can record; you have a test or a written check proving both.
- [ ] A member's balances always equal the sum of their entries, and the expected cash always equals the sum of the meeting's movements.
- [ ] No money record is ever edited or deleted, and every amount is whole shillings in an integer type.
- [ ] The project builds with nullable reference types on and zero warnings.
- [ ] The app is live as a container, and the README explains how to run it and how a request travels through middleware, page or endpoint, service and database.

## Stretch change (transfer check)
Groups want a second pair of eyes. Add a chairperson role: a meeting is not closed until the chairperson confirms the cash count the treasurer entered, and the chairperson can read everything but record nothing. Do it with authorization policies in one place, not by copying checks into every page.

## Rebuild from memory (a week later)
Without looking: write the code that records one loan repayment (the interest part, the principal part, inside one transaction, safe to submit twice), with its tests.

## Know before real use
Real members' names, numbers and balances are personal data and bring Personal Data Protection Act duties. An app that holds or moves a group's money needs a licence or a licensed partner; this one must stay a record book. Keep to invented groups while learning, and see `resources/research/East Africa software problems for PHP projects.md`.

## Evidence to record
Items for `csharp.classes-records`, `csharp.errors-files`, `csharp.async`, `dotnet.cli-nuget`, `dotnet.host-di-config`, `dotnet.efcore`, `aspnet.endpoints-middleware`, `aspnet.razor-pages`, `aspnet.identity-auth`, `dotnet.containers`, `core.security-basics`, `core.sql`, `core.http`, `core.linux-deploy` and `core.docker`. Ask a mentor or peer to try to break in (another member's statement, a forged form, script in a name); mark that item `verified_by: human`. Better still, show the app to one real group treasurer and write down what they said.
