# Stage 1 brief: Share-out and loan-schedule calculator

**Track:** .NET (C#) · **Mode:** 1, you type everything · **Time:** 2–3 months including the language basics (estimate) · Read `house-rules.md` first.

## The problem
Savings groups (VICOBA) work out the end-of-cycle share-out and the interest on members' loans by hand. The sums are long, small mistakes turn into arguments, and members have no easy way to check the treasurer's figures.

## Goal
A command-line tool, `hisa`, that keeps one group's cycle in a JSON file and prints two things anyone can check: the share-out per member, and a reducing-balance schedule for a loan.

## Build
1. **Group file.** One JSON file per group cycle, in a format you define and document: the group's rules, its members, and a list of entries (share purchases, fines, interest received). Entries are only ever added.
2. **Rules are inputs.** Share price, the interest rate, the fine amounts and whether fines join the share-out pot are all set by the group. No typical values were found in the research, so put none in the code.
3. **Commands.** Create a group file; add a member; record a share purchase; record a fine; record interest received; correct a wrong entry by adding a reversing one.
4. **Share-out.** Print each member's shares, their part of the pot and the total. Write the rounding rule in the README: what happens to the shillings left over when the pot does not divide evenly.
5. **Loan schedule.** Given a principal, a rate per period and a number of periods, print each instalment (interest part, principal part, balance after) and the total cost of the loan, on a reducing balance.
6. **Options.** `--lang=sw|en` for the labels (Kiswahili by default), `--json` to print the result as JSON.
7. **Project.** An SDK-style project with `Nullable` enabled, run with the `dotnet` CLI. File reads and writes are async and take a cancellation token.
8. **Tests.** An xUnit test project for the share-out, the schedule and the file handling.

## Edge cases you must handle
- A pot that does not divide evenly among the shares.
- A member with no shares, and a group with no members.
- A loan of one period, and a loan at a rate of zero.
- A negative amount, a share count of zero, or an amount typed with commas or `TZS` in front.
- The same member added twice.
- A group file that is missing, empty, or cut off half-way (the power went during a save).
- A rate that gives a fraction of a shilling in every instalment.

## It works when
- [ ] `dotnet run` on a sample group file prints the share-out and a schedule with no warnings.
- [ ] All money is held as whole shillings in integer types; no `float` or `double` anywhere, and the form you hold a rate in is stated.
- [ ] The members' share-outs add up to the pot exactly, to the shilling, for every test case.
- [ ] A schedule's principal parts add up to the principal, and the last balance is zero.
- [ ] A save can never leave a half-written group file, and no entry is ever edited or removed.
- [ ] The project builds with nullable reference types on and zero warnings.
- [ ] Tests cover every edge case above, and pass with `dotnet test`.
- [ ] The README explains the file format, the commands, the rounding rule, and shows sample output in both languages.

## Stretch change (transfer check)
A group charges interest a different way: a flat rate on the original amount for every period. Add it as a second method without changing the code that prints the schedule. If you have to touch the printing to add a method, redesign until you do not.

## Rebuild from memory (a week later)
Without looking: write the function that splits a pot among members by their shares so that the parts always add up to the pot, with its tests.

## Recommended alongside
Build the **Simu** elective (phone-number library) as a separate NuGet package and use it here to store each member's number in one format.

## Know before real use
The tool's figures are an aid, not a ruling: a group's own constitution decides its share-out. Keep to invented members. Lending to the public is a licensed activity; see `resources/research/East Africa software problems for PHP projects.md`.

## Evidence to record
Items for `csharp.syntax-types`, `csharp.collections-linq`, `csharp.classes-records`, `csharp.errors-files`, `csharp.async`, `dotnet.cli-nuget`, `csharp.testing-xunit`, `core.testing` and `core.git`. Have a mentor or peer work out one share-out by hand from a group file they make themselves and compare it with the tool; mark that item `verified_by: human`.
