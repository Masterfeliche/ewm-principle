# Lesson 8 — Functions, types and `strict_types`

**Time:** 3–4 hours · **Skills:** `php.arrays-functions`, `php.syntax-types` · **Before this:** Lessons 3–7
**Your folder:** `exercises/stage-1/lesson-08/`

## Goal
By the end you can write small, well-named functions with typed parameters and return
values, explain what `declare(strict_types=1)` changes, and explain why a function cannot
see variables from outside it.

## The idea
A **function** is a named piece of code you can run many times with different inputs.

```php
function formatShillings(int $amount): string
{
    return "TZS " . number_format($amount);
}

echo formatShillings(15000);   // TZS 15,000
```

- `int $amount` is a **parameter** with a **type**: this function only accepts an int.
- `: string` is the **return type**: it promises to give back a string.
- `return` gives the value back and ends the function.

**Types catch mistakes early.** Put this as the first line of every PHP file, right after
`<?php`:

```php
declare(strict_types=1);
```

Without it, PHP quietly converts: `formatShillings("15000")` works, because PHP turns the
text into an int for you. With it, PHP refuses with a `TypeError`, and you find the
mistake now instead of in production. (One allowed exception: an `int` can be passed
where a `float` is expected.) The Stage 1 project requires `strict_types` in every file.

**More parameter features**
- Default values: `function greet(string $name, string $lang = "sw"): string`
- Nullable: `?string $note` accepts a string or `null`.
- Named arguments when calling: `greet(name: "Asha", lang: "en")`.
- `void` return type for a function that gives nothing back.

**Scope.** A function only sees its own parameters and the variables it creates. A
variable made outside the function does not exist inside it. That is deliberate: a
function that depends only on its inputs is easy to test and hard to break.

**Good functions are small and do one thing.** The name says what it gives back:
`feeFor`, `directionLabel`, `isIncoming`. If you need the word "and" to describe a
function, it is probably two functions.

## Worked example
A share-out helper for a savings group, with its tests.

```php
<?php
declare(strict_types=1);

function shareOut(int $groupTotal, int $memberShares, int $allShares): int
{
    if ($allShares <= 0) {
        return 0;
    }
    return intdiv($groupTotal * $memberShares, $allShares);
}

assert(shareOut(1000000, 10, 40) === 250000);
assert(shareOut(1000000, 0, 40) === 0);
assert(shareOut(0, 10, 40) === 0);
assert(shareOut(1000000, 10, 0) === 0);
echo "Sawa\n";
```

The four asserts are its examples and edge cases, written straight from a Lesson 2 plan.

## Predict
With `declare(strict_types=1);` at the top, and `function double(int $n): int { return $n * 2; }`:

1. `echo double(4);`
2. `echo double("4");`
3. `echo double(4.0);`
4. `$n = 10; function show(): void { echo $n; } show();` — what happens?

<details><summary>Answers</summary>

1. `8`
2. `TypeError`: a string is not an int under strict types.
3. `TypeError` too: a float is not an int. (The reverse, int into float, is allowed.)
4. A warning `Undefined variable $n`, and nothing useful printed: `$n` outside is not
   visible inside.
</details>

## Exercises
Every file starts with `declare(strict_types=1);` and ends with asserts.

1. **`shares.php`** — turn your Lesson 5 bill split into a function
   `shareFor(int $total, int $people, int $position): int` that gives the share of the
   person at a given position (1 to `$people`). Assert that the shares for every position
   add up to the total for three different bills.
2. **`labels.php`** — `directionLabel(string $code, string $lang = "sw"): string` for
   `"IN"`/`"OUT"` in Kiswahili and English. Call it once with a named argument.
3. **`fees.php`** — turn your Lesson 6 fee bands into `feeFor(int $amount): int`. Keep all
   the boundary asserts. Then write `netAmount(int $amount): int` that *uses* `feeFor`.

## Find the bug
This always returns 0 and prints a warning. Copy it, read the warning, and fix it without
using `global`.

```php
<?php
declare(strict_types=1);

$basisPoints = 150;

function commission(int $sale): int
{
    return intdiv($sale * $basisPoints, 10000);
}

echo commission(20000), "\n";
```

## Project milestone: plan `hesabu` on paper
Read the [Stage 1 project brief](../../briefs/php-stage-1.md) and the
[house rules](../../briefs/house-rules.md). In `exercises/stage-1/hesabu-plan.md`, use the
six questions from Lesson 2 to plan the whole tool:

- What goes in, and what comes out (write out one full sample report by hand)?
- Which functions will you need? Give each a name, its parameters and its return type.
  Aim for small functions that do one thing.
- List every edge case from the brief, and add two of your own.

You will build it over Lessons 11–17. A good plan now saves weeks.

## Done when
- [ ] Every exercise file has `strict_types` and passes its asserts.
- [ ] `fees.php` has `netAmount` calling `feeFor`.
- [ ] The scope bug is fixed by passing the value in.
- [ ] `hesabu-plan.md` lists the functions with types, and every edge case from the brief.
- [ ] You can explain, without notes, what `strict_types` changes.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.arrays-functions --type implement --assistance A1 --task "Wrote typed functions under strict_types with asserts; fixed a scope bug; planned hesabu's functions"
```
