# Lesson 18 — Debugging 2: a step debugger, and refactoring your own code

**Time:** 4–5 hours · **Skills:** `php.testing-pest`, `core.git`, `php.files-errors` · **Before this:** Lesson 17
**Your folder:** `exercises/stage-1/hesabu/` and `exercises/stage-1/lesson-18/`

## Goal
By the end you can pause a running PHP program at any line with Xdebug and look inside
it, find a bug without adding a single `var_dump`, and improve your own code in small,
safe steps with your tests protecting you.

## The idea
### A step debugger
`var_dump` shows one value at one moment. A **step debugger** pauses the program at a
line you choose (a **breakpoint**) and lets you look at *every* variable, then move one
line at a time and watch them change.

| Action | What it does |
|---|---|
| Breakpoint | Click left of a line number; the program pauses there |
| Step over | Run this line, pause at the next one |
| Step into | Go *inside* the function this line calls |
| Step out | Finish this function, pause back in the caller |
| Continue | Run until the next breakpoint |
| Watch | Keep an expression on screen, such as `$totals['Juma'] ?? null` |

**Setting up Xdebug** (the install guide at https://xdebug.org/docs/install is the
authority; check it for your system):
1. Install: on Ubuntu, `sudo apt install php-xdebug`; elsewhere, follow the guide's wizard.
2. Check: `php -v` mentions "with Xdebug".
3. In VS Code, install the "PHP Debug" extension and create the "Listen for Xdebug"
   configuration it offers (port 9003). Other editors have the same idea.
4. Start listening in the editor, then run your program with debugging switched on:

```bash
XDEBUG_MODE=debug XDEBUG_SESSION=1 php bin/hesabu samples/mixed.txt
```

It pauses at your breakpoint. If it does not, check the port, and that `php -v` shows Xdebug.
Do not leave Xdebug switched on everywhere: it slows PHP down a lot.

### Refactoring
**Refactoring** means changing the *structure* of code without changing what it does. The
rules that make it safe:
1. Start with all tests green.
2. Make **one** small change.
3. Run the tests. Green? Commit. Red? Undo that change (`git restore`) and try a smaller one.
4. Repeat.

Never refactor and add a feature in the same step: if something breaks, you will not know
which caused it.

**Signs code needs it ("smells")**

| Smell | Typical fix |
|---|---|
| A function longer than your screen | Extract the parts into named functions |
| Deep nesting (`if` inside `if` inside `foreach`) | Return early ("guard clauses") |
| The same few lines in two places | One function, called twice |
| A bare number with no explanation (`150`, `10000`) | A named constant: `const COMMISSION_BASIS_POINTS = 150;` |
| A name you have to read the body to understand | Rename it |
| A comment explaining *what* confusing code does | Make the code clear, then delete the comment |

## Worked example
Guard clauses: the same logic, before and after.

```php
// Before: three levels deep
function discount(?array $customer, int $total): int
{
    if ($customer !== null) {
        if ($customer['member'] === true) {
            if ($total >= 50000) {
                return intdiv($total * 5, 100);
            }
        }
    }
    return 0;
}

// After: each rule exits early, and the main case reads in one line
function discount(?array $customer, int $total): int
{
    if ($customer === null || $customer['member'] !== true) {
        return 0;
    }
    if ($total < 50000) {
        return 0;
    }
    return intdiv($total * 5, 100);
}
```

Same tests, same results; now a reader sees the rules at a glance. Each version was
committed separately with the tests green.

## Exercises
1. **Step through `hesabu`** — set a breakpoint at the start of your line parser. Run one
   file through it. In `lesson-18/notes.md`, write what `$line` and your captured pieces were
   for the first three lines, and which line of a promo message makes it give up.
2. **Debugger only** — copy this into `lesson-18/bug.php` and find the bug using *only* the
   debugger. No `var_dump`, no `echo`. It should print `Juma: 7000` and `Asha: 3000`.

   ```php
   <?php
   declare(strict_types=1);
   function totals(array $payments): array
   {
       $totals = [];
       foreach ($payments as $p) {
           $name = mb_convert_case(trim($p['from']), MB_CASE_TITLE);
           $totals[$name] = ($totals[$p['from']] ?? 0) + $p['amount'];
       }
       return $totals;
   }
   $payments = [['from' => 'Juma', 'amount' => 5000], ['from' => 'Asha', 'amount' => 3000],
                ['from' => ' juma', 'amount' => 2000]];
   foreach (totals($payments) as $n => $t) {
       echo "$n: $t\n";
   }
   ```
3. **Refactor `hesabu`** — find its two worst smells (longest function, deepest nesting, or a
   bare number). Fix them one small step at a time, with a commit after each green run. At
   least four commits. Your `git log` should read like a story of small, safe changes.

## Bring back
From Lesson 9: write the debugger-only bug into your debug journal with the same seven
steps. Compare: what did the debugger show that a `var_dump` would have needed three tries
to find?

There is also a playbook for finding *when* a bug arrived, by searching your Git history:
[bisect a regression](../../../knowledge/debugging-playbooks/bisect-regressions.md).
Read it now; you will want it the first time something that used to work stops working.

## Done when
- [ ] You paused `hesabu` at a breakpoint and stepped through a line with the values written down.
- [ ] The debugger-only bug is fixed, with no `var_dump` in your history for it.
- [ ] `hesabu` has at least four refactoring commits, each with the tests green.
- [ ] You can explain, without notes, why refactoring and adding features are separate steps.
- [ ] Committed and pushed.

## Record
```bash
python .emw/tools/emw_track.py log php.testing-pest --type debug --assistance A1 --task "Found a key-mismatch bug with Xdebug alone; refactored hesabu in four green, committed steps"
```

## You have finished the Stage 1 lessons
What is left is the gate, not more lessons. Run `python .emw/tools/emw_track.py status` and
work through what it lists:
- the **stretch change** in the brief (a new message shape without touching the report code),
  done at A0 or A1, logged with `--type transfer`;
- the **rebuild from memory**, at least a week after you built it: the amount parser and its
  tests, with no notes, logged with `--type rebuild`;
- a **real person** runs `hesabu` on a sample file they make themselves and watches you
  explain your code — you record it with `--verified-by human --reviewer "<their name>"`.
