# Lesson 7 — Loops

**Time:** 3 hours · **Skills:** `php.arrays-functions`, `core.testing` · **Before this:** Lesson 6
**Your folder:** `exercises/stage-1/lesson-07/`

## Goal
By the end you can repeat work with `foreach`, `for` and `while`, skip or stop early with
`continue` and `break`, and choose the right loop for the job.

## The idea
A loop runs the same code many times. PHP has three you will use:

| Loop | Use it when | Shape |
|---|---|---|
| `foreach` | you have a list and want each item | `foreach ($items as $item) { … }` |
| `for` | you need a counter | `for ($i = 1; $i <= 5; $i++) { … }` |
| `while` | you repeat until something becomes true, and do not know how many times | `while ($balance < $target) { … }` |

Most of the time you want `foreach`. Reach for the others only when you need them.

A list is written in square brackets: `$amounts = [5000, 12000, 300];`. Lesson 10 covers
lists properly; for now, that is all you need.

Inside a loop:
- `continue` skips the rest of this round and moves to the next item.
- `break` leaves the loop completely.

**The accumulator pattern** is the heart of most loops: start a variable before the loop
(a total, a count, a "best so far"), update it inside, use it after. It is exactly the
pseudocode you wrote in Lesson 2.

**Infinite loops.** A `while` whose condition never becomes false runs forever. If your
terminal freezes, press `Ctrl+C` to stop the program, then check that something inside
the loop moves you towards the end.

## Worked example
Daily sales for a week, with the best day.

```php
<?php
$sales = [42000, 38500, 51000, 0, 47200, 60300, 29900];  // Monday to Sunday

$total = 0;
$bestDay = 0;
$bestAmount = $sales[0];
$closedDays = 0;

foreach ($sales as $day => $amount) {
    if ($amount === 0) {
        $closedDays++;
        continue;               // a closed day is not a sales day
    }
    $total += $amount;
    if ($amount > $bestAmount) {
        $bestAmount = $amount;
        $bestDay = $day;
    }
}

assert($total === 268900);
assert($bestDay === 5);         // counting starts at 0, so 5 is Saturday
assert($closedDays === 1);
echo "Jumla: " . number_format($total) . "\n";
```

`foreach ($sales as $day => $amount)` gives you both the position (`$day`, starting at 0)
and the value.

## Predict
1. How many times does this print? `for ($i = 0; $i < 3; $i++) { echo "x"; }`
2. And this? `for ($i = 1; $i <= 3; $i++) { echo "x"; }`
3. What is printed? `foreach ([1, 2, 3, 4] as $n) { if ($n === 3) { break; } echo $n; }`
4. What is printed? `foreach ([1, 2, 3, 4] as $n) { if ($n === 3) { continue; } echo $n; }`

<details><summary>Answers</summary>

1. 3 times (`$i` is 0, 1, 2).
2. 3 times (`$i` is 1, 2, 3).
3. `12`
4. `124`
</details>

## Exercises
Each file ends with asserts. Run with `php -d zend.assertions=1`.

1. **`incoming.php`** — given a list of amounts where money out is negative
   (`[15000, -3000, 8000, -500, 22000]`), work out total in and total out separately, and
   the count of each. Assert all four numbers.
2. **`savings.php`** — a VICOBA member saves 5,000 a week and wants 120,000. Use `while`
   to count the weeks needed. Then change it: every fourth week they save double. Assert
   both answers (work them out by hand first).
3. **`messages.php`** — given a list of six text messages, some starting with
   `"Umepokea"`, count how many are payments received. Stop counting (with `break`) if you
   reach a message that is exactly `"MWISHO"`.

## Find the bug
This should print every amount. Copy it, run it, read the warning, and fix it.

```php
<?php
$amounts = [1000, 2000, 3000];
for ($i = 0; $i <= count($amounts); $i++) {
    echo $amounts[$i], "\n";
}
```

Then rewrite it with `foreach`, and write one sentence on why `foreach` makes this bug
impossible.

## Bring back
From Lesson 4: in `messages.php`, use the safe way to test that a message starts with a
word. From Lesson 5: in `incoming.php`, make sure every total is an `int`.

## Done when
- [ ] All three exercises pass their asserts.
- [ ] `savings.php` matches your hand calculation for both versions.
- [ ] The bug is fixed, and rewritten with `foreach`.
- [ ] You can explain, without notes, when you would use `while` and not `foreach`.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.arrays-functions --type implement --assistance A1 --task "Used foreach, while, break and continue with accumulators; fixed an off-by-one in a for loop"
```
