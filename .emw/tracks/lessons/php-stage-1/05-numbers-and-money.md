# Lesson 5 — Integers, floats, and why money stays in integers

**Time:** 2–3 hours · **Skills:** `php.syntax-types` · **Before this:** Lessons 3–4
**Your folder:** `exercises/stage-1/lesson-05/`

## Goal
By the end you can do arithmetic in PHP, explain why floats are wrong for money, and
calculate shares, fees and percentages exactly using whole numbers.

## The idea
PHP has two kinds of number:
- **int** — whole numbers: `15000`, `-300`, `0`. Exact, always.
- **float** — numbers with a fractional part: `1.5`, `0.1`. *Approximate.*

Floats are stored in binary, and most decimal fractions cannot be stored exactly in
binary, in the same way that 1/3 cannot be written exactly in decimal (0.3333…). So:

```php
var_dump(0.1 + 0.2 == 0.3);   // bool(false)
var_dump(0.1 + 0.2);          // float(0.30000000000000004)
```

For a measurement that is fine. For money it is not: tiny errors add up across thousands
of transactions, and a total that is one shilling out is a total nobody trusts.

**House rule 3: money is stored as whole shillings in an `int`. No floats, anywhere.**

The tools for exact money maths:

| Need | Use | Example |
|---|---|---|
| Add, subtract, multiply | `+`, `-`, `*` | `$total = $price * $qty;` |
| Divide, whole part | `intdiv` | `intdiv(10000, 3)` → `3333` |
| Remainder | `%` | `10000 % 3` → `1` |
| A percentage | basis points (1% = 100) | 1.5% of `$a` is `intdiv($a * 150, 10000)` |

A percentage almost never divides exactly, so you must **choose a rounding rule** (round
down, round up, or to the nearest) and write it down. Fee rules in real systems say which
one they use; yours must too.

**Converting text to numbers.** `(int) "15000"` gives `15000`. But `(int)` is forgiving
in a dangerous way: it reads digits from the start and silently stops at the first
character it does not understand. Remember that for the bug below.

## Worked example
A shop pays a 1.5% commission on each sale to the agent who brought the customer,
rounded down to the shilling.

```php
<?php
$sale = 15999;
$basisPoints = 150;                              // 1.5%

$commission = intdiv($sale * $basisPoints, 10000);
var_dump($commission);                           // int(239)

// Check by hand: 15999 × 0.015 = 239.985, rounded down is 239. ✓
```

Notice the check by hand. On money, always do one by hand.

## Predict
1. `var_dump(7 / 2);`
2. `var_dump(intdiv(7, 2));`
3. `var_dump(7 % 3);`
4. `var_dump((int) ((0.1 + 0.7) * 10));`
5. `var_dump((int) "Tsh15000");`
6. `var_dump(round(2.5));`

<details><summary>Answers</summary>

1. `float(3.5)`
2. `int(3)`
3. `int(1)`
4. `int(7)`, not 8. `0.1 + 0.7` is really `0.7999999…`, times 10 is `7.999999…`, and
   `(int)` chops the fraction off. This exact bug has shipped in real billing systems.
5. `int(0)` — it stops at `T`, before reading any digit.
6. `float(3)` — `round` gives back a float, even when the answer is whole.
</details>

## Exercises
1. **`floats.php`** — show the `0.1 + 0.2` problem yourself, then show that adding
   `10` and `20` and comparing to `30` with ints is exact. Write in `notes.md`, in your own
   words, why house rule 3 exists.
2. **`split.php`** — split a bill of 10,000 shillings between 3 friends so that the shares
   add up to *exactly* 10,000. One person pays the extra shilling. Then make it work for any
   total and any number of people (still just variables at the top of the file; functions
   come in Lesson 8). Check that the shares always add up to the total.
3. **`fee.php`** — an invented wallet charges 1.25% on withdrawals, **rounded up** to the
   next shilling, with a minimum fee of 100. Work out the fee for 1,000, 8,000, 8,001 and
   100,000 shillings. Do each one by hand in a comment first.

## Find the bug
A file has amounts written the way people write them. The total should be 45,000. It is 45.

```php
<?php
$a = (int) "15,000";
$b = (int) "20,000";
$c = (int) "10,000";
echo $a + $b + $c, "\n";
```

Fix it so it prints `45000`. Do not use floats.

## Bring back
From Lesson 4: the fix needs a string function. Which one, and why is it safe to use the
byte version here?

## Done when
- [ ] `split.php` gives shares that add up to the total for 10,000 ÷ 3, 10 ÷ 4 and 7 ÷ 7.
- [ ] `fee.php` matches your hand calculations for all four amounts, including the minimum.
- [ ] No float appears in any money variable (`var_dump` them to check).
- [ ] You can explain, without notes, why `(int) "15,000"` is 15.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.syntax-types --type implement --assistance A1 --task "Split bills and calculated rounded-up fees exactly with integer maths; fixed (int) on comma-formatted amounts"
```
