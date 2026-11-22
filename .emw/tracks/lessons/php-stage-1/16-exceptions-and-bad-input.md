# Lesson 16 — Exceptions and handling bad input

**Time:** 3–4 hours · **Skills:** `php.files-errors`, `php.testing-pest` · **Before this:** Lessons 9, 13–15
**Your folder:** `exercises/stage-1/hesabu/` and `exercises/stage-1/lesson-16/`

## Goal
By the end you can signal a problem with an exception, catch it in the right place, keep
going past bad lines while listing them, and make your program fail clearly with a proper
exit code when it cannot continue.

## The idea
So far your functions have signalled problems with special values: `null`, `-1`, `false`.
That works, but every caller must remember to check, and `-1` can look like a real number.
An **exception** is a louder signal: it stops the current function and travels up through
the callers until something **catches** it. If nothing does, the program stops and prints
the stack trace you learnt to read in Lesson 9.

```php
function parseAmount(string $text): int
{
    // ...
    throw new InvalidArgumentException("Not an amount: '$text'");
}

try {
    $amount = parseAmount($input);
} catch (InvalidArgumentException $e) {
    echo "Kiasi si sahihi: ", $e->getMessage(), "\n";
}
```

**Which exception?** PHP has many built in. The ones you will use most:

| Exception | Means |
|---|---|
| `InvalidArgumentException` | the caller passed something unacceptable |
| `RuntimeException` | something went wrong while running (a file vanished) |
| `JsonException` | bad JSON (with `JSON_THROW_ON_ERROR`, Lesson 14) |
| `TypeError`, `ValueError` | thrown by PHP itself for wrong types and values |

You can make your own, so callers can catch exactly your problem and nothing else. Classes
are a Stage 2 topic; for now, this one line is all you need:

```php
final class UnreadableLine extends RuntimeException {}
```

**Where to catch.** Catch an exception only where you can *do something useful* about it:
skip the line and record it, show the user a clear message, try again. Everywhere else, let
it travel. Catching and doing nothing is the worst choice of all.

**`finally`** runs whether or not an exception happened — the right place to close a file.

**Bad input versus broken code.** A promotional message in the file is *expected* bad input:
record it and carry on. A function being given a negative quantity by your own code is a
*bug*: let it crash, loudly, so you find it.

**Exit codes.** A command-line program reports success or failure to whoever ran it with a
number: `0` means success, anything else means failure. Scripts and CI pipelines rely on
this. End with `exit(1);` when the program cannot do its job, after writing the reason to
`STDERR`.

**Do not leak internals.** A message for a user says what went wrong in their terms
("Faili halipo: data.csv"). It does not dump a stack trace, a full server path, or data
from other records.

## Worked example
Reading quantities typed by a shopkeeper, one per line.

```php
<?php
declare(strict_types=1);

function parseQuantity(string $text): int
{
    $text = trim($text);
    if (preg_match('~^\d{1,5}$~', $text) !== 1) {
        throw new InvalidArgumentException("Not a quantity: '$text'");
    }
    return (int) $text;
}

function readQuantities(array $lines): array
{
    $good = [];
    $bad = [];
    foreach ($lines as $number => $line) {
        try {
            $good[] = parseQuantity($line);
        } catch (InvalidArgumentException $e) {
            $bad[] = ['line' => $number + 1, 'reason' => $e->getMessage()];
        }
    }
    return ['good' => $good, 'bad' => $bad];
}
```

And the test that an exception is thrown:

```php
it('rejects a quantity that is not a number', function () {
    expect(fn () => parseQuantity('tano'))->toThrow(InvalidArgumentException::class);
});
```

Note `$number + 1`: people count lines from 1, arrays from 0.

## Predict
```php
function a(): void { throw new RuntimeException("A"); }
function b(): void { try { a(); } finally { echo "finally "; } }
try { b(); } catch (RuntimeException $e) { echo "caught ", $e->getMessage(); }
```
1. What is printed?
2. If `b` used `catch (InvalidArgumentException $e)` instead of `finally`, what then?

<details><summary>Answers</summary>

1. `finally caught A` — `finally` runs, then the exception carries on up to the caller.
2. `caught A` — `b`'s catch does not match a `RuntimeException`, so it passes straight
   through to the outer catch.
</details>

## Exercises
1. **`parseAmount` throws** — change it to throw `InvalidArgumentException` instead of
   returning `-1`. Update the tests: good amounts still pass; bad ones use `->toThrow()`.
2. **Collect bad lines** — `parseAll(array $lines): array` gives back the parsed transactions
   *and* a list of unreadable lines with their line numbers and reasons. A promo, a blank line
   and a malformed amount must all end up in the list without stopping the run (the brief:
   "unreadable lines never stop the run and are listed at the end").
3. **Duplicates** — the same reference appearing twice is counted once and reported (brief,
   edge cases). Write the test first, watch it fail, then make it pass.
4. **Missing or empty file** — your entry point prints a clear Kiswahili or English message
   to `STDERR` and exits with `1` for a missing file. An empty file is not an error: print an
   empty report and exit `0`. Check the codes with `echo $?` after running.

## Find the bug
Users say "some payments are missing from the total, and nothing tells us why". Find the
line responsible and fix it so problems are reported, not hidden.

```php
foreach ($lines as $line) {
    try {
        $transactions[] = parseLine($line);
    } catch (Exception $e) {
    }
}
```

## Bring back
From Lesson 12: every new behaviour in this lesson gets a Pest test *before* the code. From
Lesson 14: `fclose` belongs in a `finally`.

## Project milestone
Every edge case in the brief is handled and tested: commas and `TZS`/`Tsh`, promos,
duplicate references, empty and missing files, two date formats. Bad lines are listed at the
end of the report.

## Done when
- [ ] Every edge case in the brief has a passing test.
- [ ] A bad line never stops the run; it appears in the list with its line number.
- [ ] Missing file → message on `STDERR`, exit code `1`. Empty file → empty report, exit `0`.
- [ ] No empty `catch` blocks anywhere in `hesabu`.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.files-errors --type implement --assistance A1 --task "Replaced sentinel values with exceptions; hesabu lists unreadable lines and duplicates and exits 1 on a missing file"
```
