# Lesson 11 — Array functions and closures

**Time:** 4 hours · **Skills:** `php.arrays-functions` · **Before this:** Lesson 10
**Your folder:** `exercises/stage-1/lesson-11/`

## Goal
By the end you can filter, transform, sort, group and total arrays with PHP's built-in
array functions and short functions written inline, and you know when a plain `foreach`
is clearer.

## The idea
Many loops follow the same few shapes. PHP has a function for each:

| Shape | Function | Gives back |
|---|---|---|
| Keep some items | `array_filter($list, $test)` | the items where `$test` is true — **keys kept** |
| Change every item | `array_map($change, $list)` | a new list of changed items |
| Pick one column | `array_column($rows, "amount")` | a list of that key's values |
| Add up | `array_sum($numbers)` | the total |
| Sort by a rule | `usort($list, $compare)` | sorts *in place*, gives back `true` |
| Sort a keyed array by value | `arsort($map)` (high to low), `asort` | sorts in place, keys kept |
| Take part of a list | `array_slice($list, 0, 5, true)` | the first five, keys kept |
| Renumber from 0 | `array_values($list)` | the same values, keys 0, 1, 2… |

**Closures** are functions without a name, written where you need them:

```php
$isIncoming = function (array $t): bool {
    return $t["direction"] === "IN";
};
```

**Arrow functions** are a shorter form for one expression. They can read variables from
around them automatically:

```php
$limit = 10000;
$big = array_filter($amounts, fn (int $a): bool => $a >= $limit);
```

A full `function () { … }` closure cannot see `$limit` unless you add `use ($limit)`.

You can also pass an existing function by name with `(...)`:
`array_map(trim(...), $names)`.

**The spaceship operator `<=>`** compares two values and gives `-1`, `0` or `1`. It is
what `usort` wants: `usort($rows, fn ($a, $b) => $b["amount"] <=> $a["amount"]);` sorts
from biggest to smallest. Swap `$a` and `$b` for smallest first.

**When not to.** Three array functions chained together can be harder to read than one
`foreach`. Use whichever a colleague would understand fastest.

## Worked example
Goods that need reordering, cheapest first, as text lines.

```php
<?php
declare(strict_types=1);

$products = [
    ["name" => "Sukari", "stock" => 2, "price" => 3500],
    ["name" => "Unga", "stock" => 40, "price" => 2800],
    ["name" => "Mafuta", "stock" => 1, "price" => 7000],
    ["name" => "Chumvi", "stock" => 5, "price" => 500],
];

$low = array_filter($products, fn (array $p): bool => $p["stock"] <= 5);
usort($low, fn (array $a, array $b): int => $a["price"] <=> $b["price"]);
$lines = array_map(fn (array $p): string => "{$p['name']} ({$p['stock']})", $low);

assert($lines === ["Chumvi (5)", "Sukari (2)", "Mafuta (1)"]);
echo implode("\n", $lines), "\n";
```

`usort` renumbered `$low` from 0, which is why the final list has clean keys.

## Predict
1. `print_r(array_filter([5, 0, 8, 0, 2]));` — no test given at all.
2. `$f = array_filter([10, 3, 20], fn ($n) => $n > 5); echo $f[1] ?? "hakuna";`
3. `print_r(array_map(fn ($n) => $n * 2, [1, 2, 3]));`
4. `$m = ["a" => 3, "b" => 9, "c" => 1]; arsort($m); echo array_key_first($m);`

<details><summary>Answers</summary>

1. `[0 => 5, 2 => 8, 4 => 2]` — with no test, it drops falsy values (Lesson 3), and the
   keys are kept.
2. `hakuna` — the kept items are at keys 0 and 2. Key 1 is gone.
3. `[2, 4, 6]`
4. `b`
</details>

## Exercises
Use your six transactions from Lesson 10 (add four more). Asserts as always.

1. **`incoming.php`** — `incomingOnly(array $txs): array` with `array_filter`, giving a list
   numbered from 0. Then the total received using `array_column` and `array_sum`.
2. **`top.php`** — `topCounterparties(array $txs, int $howMany): array` giving the top
   senders by amount received, as name → total, biggest first. Reuse your Lesson 10
   grouping function. What happens with a tie, and is that acceptable? Write it down.
3. **`monthly.php`** — `totalsByMonth(array $txs): array` giving `"2026-03"` → total in, out
   and fees for each month. Dates are `"YYYY-MM-DD"` text for now; a string function from
   Lesson 4 gets you the month.

## Find the bug
"Print the first big payment." It prints a warning instead. Find out why, and fix it two
different ways.

```php
<?php
declare(strict_types=1);
$payments = [400, 900, 25000, 30000];
$big = array_filter($payments, fn (int $p): bool => $p > 10000);
echo $big[0], "\n";
```

## Project milestone: parse one message shape
In `exercises/stage-1/hesabu/` start the project. Put **one** message shape you collected
yourself (with names and numbers replaced by invented ones — house rule 5) in a list of
five lines in your code. Write `parseLine(string $line): ?array` that turns one line of
that shape into a transaction array, or gives `null` if it cannot. Use only string
functions (Lesson 4); Lesson 13 will replace them with something better. Then print the
total received with the functions from this lesson.

## Done when
- [ ] All three exercises pass their asserts.
- [ ] `top.php` has a written decision about ties.
- [ ] The bug is fixed two ways.
- [ ] `hesabu` parses five lines of one shape and prints a correct total.
- [ ] You can explain, without notes, why `array_filter` can leave gaps in the keys.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.arrays-functions --type implement --assistance A1 --task "Filtered, sorted, grouped and totalled transactions with array functions and closures; started hesabu with one message shape"
```
