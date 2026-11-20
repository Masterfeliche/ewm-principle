# Stage 1 brief: Mobile-money statement analyser

**Track:** Python · **Mode:** 1, you type everything · **Time:** 2–3 months including the language basics (estimate) · Read `house-rules.md` first.

## The problem
Small sellers and shops in Tanzania confirm payments by reading transaction messages on a phone and add them up by hand. At the end of the month they cannot say how much came in, from whom, or how much went on fees.

## Goal
A command-line tool, `hesabu`, that reads transaction records and prints a clear summary. It is typed and tested from the first day.

## Build
1. **Input.** Accept a file path. Support two formats:
   - a CSV statement with columns you define and document (date, type, amount, fee, counterparty, reference, balance);
   - a text file of pasted transaction messages, one per line, in at least **three message shapes you collect yourself** (for example money received, money sent, payment to a merchant). Write the shapes down in the README. Remove real names and numbers before saving any sample.
2. **Parsing.** Turn each line into one transaction: date and time (East Africa Time), direction (in or out), amount, fee, counterparty, reference. A transaction is a typed object (a dataclass), not a loose dictionary.
3. **Report.** Print:
   - totals in and out per month;
   - total fees per month;
   - totals per sender, with the top five counterparties by amount received;
   - the number of lines that could not be read, and which ones.
4. **Options.** `--from` and `--to` dates, `--lang=sw|en` for the report labels, `--json` to print the result as JSON.
5. **Packaging.** A uv project: `pyproject.toml`, a committed `uv.lock`, a package under `src/`, and a `hesabu` command declared as a script entry point. Use Typer or argparse for the command line.
6. **Quality.** Type hints on every function, checked by mypy or pyright. Ruff for linting and formatting.
7. **Tests.** pytest tests for the parser and the totals.
8. **A labelled sample set.** Keep `samples/labelled.jsonl` (or a format you document): each anonymised message with the fields a correct parse must give (amount, direction, counterparty, reference, fee, date). Your parser tests read it. **Stage 5 reuses this file**, so label carefully and keep adding to it.

## Edge cases you must handle
- Amounts written with commas or with `TZS`/`Tsh` in front (`TZS 15,000`, `Tsh15,000.00`).
- A line that is not a transaction at all (a promotional message).
- The same reference appearing twice: count it once and report it.
- An empty file, a file that does not exist, and a file that is not valid UTF-8: a clear message, never a traceback.
- Dates in two different formats within one file.
- The same kind of message in Kiswahili and in English.

## It works when
- [ ] `uv sync --locked` then `uv run hesabu samples/mixed.txt` prints the report with no warnings.
- [ ] All money is held as whole shillings in `int`; no `float` anywhere.
- [ ] Unreadable lines never stop the run and are listed at the end.
- [ ] Every function has parameter and return types, and mypy or pyright reports no errors.
- [ ] `ruff check` and `ruff format --check` pass.
- [ ] Tests cover every message shape and every edge case above, and pass.
- [ ] Every sample in the labelled set is anonymised and has its expected fields.
- [ ] The README explains the formats, the options, and shows sample output.

## Stretch change (transfer check)
Add a new message shape you have not handled before (for example a cash withdrawal at an agent, with its own fee wording) without changing the report code. If you have to touch the report to add a shape, redesign until you do not.

## Rebuild from memory (a week later)
Without looking: write the function that turns `"Tsh15,000.00"`, `"TZS 15,000"` and `"15000"` into the integer `15000`, with type hints and its pytest tests.

## Recommended alongside
Build the **Simu** elective (phone-number library) as a separate uv package and use it here to normalise counterparty numbers.

## Evidence to record
Items for `python.syntax-types`, `python.collections-functions`, `python.files-errors`, `python.classes-dataclasses`, `python.type-hints`, `python.tooling`, `python.testing-pytest`, `core.testing` and `core.git`. Have a mentor or peer run the tool on a sample file they make themselves; mark that item `verified_by: human`.
