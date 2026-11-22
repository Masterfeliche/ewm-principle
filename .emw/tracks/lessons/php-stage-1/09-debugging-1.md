# Lesson 9 — Debugging 1: read the error, shrink the problem

**Time:** 3 hours · **Skills:** `php.files-errors`, `php.syntax-types` · **Before this:** Lessons 1–8
**Your folder:** `exercises/stage-1/lesson-09/`

## Goal
By the end you can find and fix a bug with a method rather than by guessing: read the
error and its stack trace, look inside variables, form a guess, test it, and shrink the
problem until the cause is obvious.

## The idea
Debugging is the skill that suffers most when people learn with AI, and it is the one
employers test most. It is a method, not a talent.

**The method**
1. **Reproduce.** Make the bug happen on purpose, every time. Write down the exact command.
2. **Read.** Read the whole error, slowly: kind, message, file, line, and the stack trace.
3. **Look.** Put `var_dump` just before the failing line to see what the values *really* are.
4. **Guess.** Say one specific guess out loud: "I think `$amount` is a string here."
5. **Test the guess.** Change one thing, run again. Did it confirm or rule out the guess?
6. **Shrink.** If it is still unclear, delete code until you have the smallest program that
   still shows the bug. The cause is usually obvious by then.
7. **Fix, then prove it.** Add an assert that would have caught the bug.

**Silent bugs** are the hard ones: no error, just a wrong answer. For those, step 3 does
all the work. Check your assumptions one at a time, starting from where the data comes in.

**Reading a stack trace.** When a function called from another function fails, PHP shows
the chain of calls, most recent first:

```
PHP Fatal error:  Uncaught TypeError: feeFor(): Argument #1 ($amount) must be of type int,
string given, called in /home/asha/report.php on line 14 and defined in
/home/asha/report.php:5
Stack trace:
#0 /home/asha/report.php(14): feeFor('15000')
#1 /home/asha/report.php(20): buildReport(Array)
#2 {main}
```

Read it as a story: the program started at `{main}`, line 20 called `buildReport`, and
inside it line 14 called `feeFor` with the *text* `'15000'`. `feeFor` is fine; the bug is
whoever passed it a string. Fix it where the wrong value is *created*, not where it
finally explodes.

**Useful tools**
- `var_dump($x);` — type and value.
- `var_dump($x); exit;` — look, then stop, so the output does not scroll away.
- `print_r($list);` — a quicker, more readable view of a list.
- `php -d display_errors=1 -d error_reporting=-1 file.php` — show every warning.

**Keep a debug journal.** For each bug: what you saw, your guesses, what proved it, the
fix. After a month you will see your own patterns, and that is where real speed comes from.

## Worked example
"The weekly total is wrong. It should be 26,500 but it says 25,000."

```php
<?php
declare(strict_types=1);
$days = ["12000", "8000", "5000", "1,500"];
$total = 0;
foreach ($days as $d) {
    $total += (int) $d;
}
echo $total, "\n";   // 25001
```

1. **Reproduce:** `php week.php` prints `25001` every time. (Not even 25,000: noticing that
   is a clue.)
2. **Read:** no error at all. It is a silent bug.
3. **Look:** add `var_dump((int) $d);` inside the loop. It prints 12000, 8000, 5000, **1**.
4. **Guess:** "`(int)` stops at the comma in `"1,500"`." This is Lesson 5's trap.
5. **Test:** `var_dump((int) "1,500");` → `int(1)`. Confirmed.
6. **Fix:** remove commas before converting. **Prove:** `assert($total === 26500);`

## Exercises
Copy each broken program into its own file *by typing it*. Fix it with the method and write
every step, including wrong guesses, in `journal.md`. A wrong guess you ruled out is good
evidence of method; do not hide it.

**Bug A** — crashes.
```php
<?php
declare(strict_types=1);
function percent(int $part, int $whole): int
{
    return intdiv($part * 100, $whole);
}
function report(array $counts): void
{
    foreach ($counts as $name => $count) {
        echo $name, ": ", percent($count, array_sum($counts) - $count - $count), "%\n";
    }
}
report(["Juma" => 5, "Asha" => 5]);
```

**Bug B** — wrong answer, no error. It should print `3` (three payments of 10,000 or more).
```php
<?php
declare(strict_types=1);
$payments = [10000, 25000, 9999, 10000, 400];
$big = 0;
foreach ($payments as $p) {
    if ($p > 10000) {
        $big++;
    }
}
echo $big, "\n";
```

**Bug C** — crashes, and the message points at a line that looks fine.
```php
<?php
declare(strict_types=1);
function label(string $code): string
{
    return match ($code) { "IN" => "Imepokelewa", "OUT" => "Imetumwa" };
}
$codes = ["IN", "OUT", "in"];
foreach ($codes as $c) {
    echo label($c), "\n";
}
```
For Bug C, decide whether the fix belongs in `label` or in the data, and write why.

## Bring back
For each bug, write the assert that would have caught it (Lesson 6), and add it.

## Done when
- [ ] All three bugs are fixed, each with an assert that proves it.
- [ ] `journal.md` has all seven steps for each bug, including at least one wrong guess.
- [ ] You can read the worked example's stack trace aloud and say which line caused it.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.files-errors --type debug --assistance A1 --task "Fixed a crash, a silent off-by-one and a match error by reading traces, var_dump and shrinking; kept a debug journal"
```
Debugging is evidence the gate values highly. Use A0 if you used no hints at all.
