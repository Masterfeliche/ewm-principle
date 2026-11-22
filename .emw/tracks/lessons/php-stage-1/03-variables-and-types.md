# Lesson 3 — Variables, types, and `==` versus `===`

**Time:** 2–3 hours · **Skills:** `php.syntax-types` · **Before this:** Lessons 1–2
**Your folder:** `exercises/stage-1/lesson-03/`

## Goal
By the end you can create variables of PHP's basic types, see exactly what is in a
variable with `var_dump`, and explain why you will always compare with `===`.

## The idea
A **variable** is a name for a value. In PHP every variable name starts with `$`.

```php
$name = "Asha";      // string: text
$amount = 15000;     // int: a whole number
$rate = 1.5;         // float: a number with a decimal point
$paid = true;        // bool: true or false
$note = null;        // null: "no value"
```

A value always has a **type**. `var_dump($x)` shows the type *and* the value, which makes
it the most useful debugging tool you have. `echo` only shows the value, and hides the type.

PHP is willing to convert between types for you ("type juggling"). `"5" + 3` is `8`,
because PHP turns the text `"5"` into the number 5. That is convenient, and it is also
the source of some of the hardest bugs you will ever chase. The loose comparison `==`
juggles; the strict comparison `===` does not — it is true only when the type *and*
the value are the same.

| Expression | Result | Why |
|---|---|---|
| `"15000" == 15000` | `true` | PHP converted the text to a number |
| `"15000" === 15000` | `false` | One is a string, one is an int |
| `"1" == "01"` | `true` | Both look like numbers, so PHP compared them as numbers |
| `"10" == "1e1"` | `true` | `1e1` is scientific notation for 10 |
| `null == false` | `true` | Both count as "empty" |
| `"0" == false` | `true` | The text `"0"` counts as false |

**The rule for this whole track: use `===` and `!==`.** Use `==` only if you can explain
why, out loud, to someone else.

Some values count as false in an `if` even though they are not `false` itself. They are
called **falsy**: `false`, `0`, `0.0`, `""`, `"0"`, `null`, and an empty array `[]`.
Everything else is truthy. `"0"` is the surprising one.

## Worked example
A school wants to check whether a pupil's fee is fully paid.

```php
<?php
$feeDue = 120000;
$paidSoFar = "120000";     // came from a form, so it is text

var_dump($feeDue);         // int(120000)
var_dump($paidSoFar);      // string(6) "120000"

var_dump($paidSoFar == $feeDue);   // bool(true)  — juggled
var_dump($paidSoFar === $feeDue);  // bool(false) — different types

$paidAsNumber = (int) $paidSoFar;  // convert on purpose, once, where the text arrives
var_dump($paidAsNumber === $feeDue); // bool(true)
```

The lesson in that last part: convert text to the type you need **once, at the edge**,
where it enters your program. After that, compare strictly.

## Predict
Write each answer down, then run them all in one file with `var_dump`.

1. `var_dump(10 / 5);`
2. `var_dump(10 / 4);`
3. `var_dump("5" + 3);`
4. `var_dump("5" . 3);`
5. `var_dump("abc" == 0);`
6. `var_dump((bool) "0");`

<details><summary>Answers</summary>

1. `int(2)` — dividing two ints gives an int when it divides exactly...
2. `float(2.5)` — ...and a float when it does not.
3. `int(8)` — `+` is maths, so the text became a number.
4. `string(2) "53"` — `.` joins text, so the number became text.
5. `bool(false)` in PHP 8. In PHP 7 it was `true`, which caused real security bugs.
6. `bool(false)` — `"0"` is falsy.
</details>

## Exercises
1. **`transaction.php`** — make variables for one transaction: date (text), direction
   (`"IN"` or `"OUT"`), amount, fee, counterparty and reference. `var_dump` each. Make sure
   amount and fee are `int`, not text.
2. **`compare.php`** — write ten comparisons of your own, mixing types. For each, write
   your prediction in a comment on the line above, then run it. Count how many you got
   right and write the number at the top of the file. Be honest; this is for you.
3. **`rule.md`** — in three sentences, explain to a friend who is starting PHP tomorrow
   why they should use `===`. Use one example from your own `compare.php`.

## Find the bug
A form sends the number of items as text. When a customer orders exactly `"0"` items
the program should say "No items", and it does — but it also says "No items" when it
should not. Copy this into a file, run it with different values of `$input`, and fix it
so that only a missing or empty value prints "Hakuna kitu".

```php
<?php
$input = "0";
if (!$input) {
    echo "Hakuna kitu\n";
} else {
    echo "Vitu: $input\n";
}
```

Hint ladder if you are stuck: (1) Which values are falsy? (2) What do you actually want
to test — "is it empty text", or "is it falsy"? (3) Look up `=== ""` and `is_null`.

## Bring back
From Lesson 2: before fixing the bug, write the inputs and expected outputs as a small
table (`""`, `"0"`, `"3"`, `null`). Then fix it and check every row.

## Done when
- [ ] `transaction.php` shows `int` for amount and fee.
- [ ] `compare.php` has ten predictions, each checked, with your score at the top.
- [ ] The bug is fixed and every row of your table gives the expected output.
- [ ] You can explain, without notes, what "falsy" means and name all seven falsy values.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.syntax-types --type predict --assistance A1 --task "Predicted and checked ten loose and strict comparisons; fixed a falsy '0' bug"
```
