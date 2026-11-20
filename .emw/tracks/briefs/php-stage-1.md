# Stage 1 brief: Mobile-money statement analyser

**Track:** PHP · **Mode:** 1, you type everything · **Time:** 2–3 months including the language basics (estimate) · Read `php-house-rules.md` first.

## The problem
Small sellers and shops in Tanzania confirm payments by reading transaction messages on a phone and add them up by hand. At the end of the month they cannot say how much came in, from whom, or how much went on fees.

## Goal
A command-line tool, `hesabu`, that reads transaction records and prints a clear summary.

## Build
1. **Input.** Accept a file path. Support two formats:
   - a CSV statement with columns you define and document (date, type, amount, fee, counterparty, reference, balance);
   - a text file of pasted transaction messages, one per line, in at least **three message shapes you collect yourself** (for example money received, money sent, payment to a merchant). Write the shapes down in the README. Remove real names and numbers before saving any sample.
2. **Parsing.** Turn each line into one transaction: date and time (East Africa Time), direction (in or out), amount, fee, counterparty, reference.
3. **Report.** Print:
   - totals in and out per month;
   - total fees per month;
   - the top five counterparties by amount received;
   - the number of lines that could not be read, and which ones.
4. **Options.** `--from` and `--to` dates, `--lang=sw|en` for the report labels, `--json` to print the result as JSON.
5. **Packaging.** A Composer project with PSR-4 autoloading and a `bin/hesabu` entry point.
6. **Tests.** Pest tests for the parser and the totals.

## Edge cases you must handle
- Amounts written with commas or with `TZS`/`Tsh` in front (`TZS 15,000`, `Tsh15,000.00`).
- A line that is not a transaction at all (a promotional message).
- The same reference appearing twice: count it once and report it.
- An empty file, and a file that does not exist.
- Dates in two different formats within one file.

## It works when
- [ ] `composer install` then `bin/hesabu samples/mixed.txt` prints the report with no warnings.
- [ ] All money is held as whole shillings in integers; no floats anywhere.
- [ ] Unreadable lines never stop the run and are listed at the end.
- [ ] `declare(strict_types=1)` is in every file, and every function has parameter and return types.
- [ ] Tests cover every message shape and every edge case above, and pass.
- [ ] The README explains the formats, the options, and shows sample output.

## Stretch change (transfer check)
Add a new message shape you have not handled before (for example a cash withdrawal at an agent, with its own fee wording) without changing the report code. If you have to touch the report to add a shape, redesign until you do not.

## Rebuild from memory (a week later)
Without looking: write the function that turns `"Tsh15,000.00"`, `"TZS 15,000"` and `"15000"` into the integer `15000`, with its tests.

## Recommended alongside
Build the **Simu** elective (phone-number library) as a separate Composer package and use it here to normalise counterparty numbers.

## Evidence to record
Items for `php.syntax-types`, `php.arrays-functions`, `php.files-errors`, `php.composer-autoload`, `php.testing-pest`, `core.testing` and `core.git`. Have a mentor or peer run the tool on a sample file they make themselves; mark that item `verified_by: human`.
