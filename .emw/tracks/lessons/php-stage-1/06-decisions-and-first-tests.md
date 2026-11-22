# Lesson 6 — Decisions with `if` and `match`, and your first tests

**Time:** 3 hours · **Skills:** `php.syntax-types`, `core.testing` · **Before this:** Lessons 3–5
**Your folder:** `exercises/stage-1/lesson-06/`

## Goal
By the end you can make a program choose between paths with `if` and `match`, handle
"no value" with `??`, and write simple checks that fail loudly when your code is wrong.

## The idea
**`if`, `elseif`, `else`** run different code depending on a condition:

```php
if ($amount > 100000) {
    echo "Kubwa\n";
} elseif ($amount > 10000) {
    echo "Wastani\n";
} else {
    echo "Ndogo\n";
}
```

Combine conditions with `&&` (and), `||` (or) and `!` (not).

**`match`** picks one value from several. It compares with `===` (strict, as in Lesson
3), it never falls through to the next arm, and if no arm matches it throws an error
(`UnhandledMatchError`) rather than carrying on quietly. That last property is a feature:
unexpected input stops the program instead of producing a wrong answer.

```php
$label = match ($code) {
    "A" => "Amelipa",
    "D" => "Anadaiwa",
    default => "Haijulikani",
};
```

`match (true)` is a common way to test ranges: each arm is a condition, and the first
true one wins.

**`??`** gives a fallback when something is `null` or missing: `$lang = $chosen ?? "sw";`

**Your first tests.** A test is code that checks other code. The simplest form in PHP is
`assert`:

```php
assert($label === "Amelipa");
```

If the condition is true, nothing happens. If it is false, the program stops with an
`AssertionError` pointing at that line. Run files with assertions switched on:

```bash
php -d zend.assertions=1 file.php
```

(Without `-d zend.assertions=1`, a production PHP setup silently skips every `assert`.)

From now on, every exercise ends with asserts that check its examples and edge cases.
In Lesson 12 you will move to a proper test tool, Pest. The habit starts now.

## Worked example
An invented bus company gives a discount by passenger type.

```php
<?php
$type = "student";
$fare = 30000;

$discountPercent = match ($type) {
    "child" => 50,
    "student" => 20,
    "adult" => 0,
};

$toPay = $fare - intdiv($fare * $discountPercent, 100);

assert($discountPercent === 20);
assert($toPay === 24000);
echo "Lipa TZS " . number_format($toPay) . "\n";
```

Try `$type = "pensioner";` and read the error. That loud failure is what you want: a
silent wrong fare would be far worse.

## Predict
1. `echo match ("1") { 1 => "namba", default => "maandishi" };`
2. `$x = null; echo $x ?? "hakuna";`
3. `$x = 0; echo $x ?? "hakuna";`
4. `$x = 0; echo $x ?: "hakuna";`

<details><summary>Answers</summary>

1. `maandishi` — `match` is strict, and `"1"` is not `1`.
2. `hakuna`
3. `0` — `??` only replaces `null`, and `0` is not null.
4. `hakuna` — `?:` replaces anything falsy, including `0`. Usually not what you want with
   amounts.
</details>

## Exercises
Each file ends with asserts. Run with `php -d zend.assertions=1`.

1. **`direction.php`** — turn a direction code into a Kiswahili label: `"IN"` →
   `"Imepokelewa"`, `"OUT"` → `"Imetumwa"`. Any other code must stop the program, not
   print a guess. Assert both labels.
2. **`band.php`** — an invented fee table: up to 999 → 0; 1,000–9,999 → 200;
   10,000–49,999 → 500; 50,000 and above → 1,000. Use `match (true)`. Assert every
   boundary: 999, 1000, 9999, 10000, 49999, 50000, and also 0. Negative amounts must
   be rejected.
3. **`lang.php`** — a variable `$chosen` holds `"sw"`, `"en"` or `null`. Use `??` to default
   to `"sw"`, then `match` to pick the greeting `"Karibu"` or `"Welcome"`. Assert all three cases.

## Find the bug
"Amounts of 10,000 or more get free delivery." The shop owner says it is wrong. Copy it,
add asserts for the boundaries, and let the asserts find the bug.

```php
<?php
$amount = 10000;
$delivery = match (true) {
    $amount > 10000 => 0,
    default => 2000,
};
echo "Delivery: $delivery\n";
```

## Bring back
From Lesson 2: before writing `band.php`, list its edge cases in a comment at the top.
Every edge case becomes one assert.

## Done when
- [ ] All three exercises pass their asserts when run with `-d zend.assertions=1`.
- [ ] `band.php` asserts every boundary and rejects a negative amount.
- [ ] The bug is fixed, and an assert proves it.
- [ ] You can explain, without notes, two differences between `match` and `if`.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log core.testing --type implement --assistance A1 --task "Wrote match-based fee bands with asserts on every boundary; an assert found an off-by-one in a delivery rule"
```
