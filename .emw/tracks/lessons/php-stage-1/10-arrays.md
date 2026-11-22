# Lesson 10 — Arrays, and how PHP copies them

**Time:** 3–4 hours · **Skills:** `php.arrays-functions` · **Before this:** Lessons 7–9
**Your folder:** `exercises/stage-1/lesson-10/`

## Goal
By the end you can store data in lists and keyed arrays, nest them, add, read, check and
remove items safely, and predict what happens when an array is passed to a function.

## The idea
A PHP **array** is one structure used two ways:

**A list** — items in order, numbered from 0:
```php
$amounts = [15000, 3000, 22000];
echo $amounts[0];          // 15000
$amounts[] = 500;          // add to the end
echo count($amounts);      // 4
```

**A keyed array** (a "map" or "dictionary") — each value has a name:
```php
$transaction = [
    "date" => "2026-03-14",
    "direction" => "IN",
    "amount" => 15000,
    "counterparty" => "Juma Ally",
];
echo $transaction["amount"];   // 15000
$transaction["fee"] = 0;       // add or change a key
unset($transaction["fee"]);    // remove a key
```

**Nesting** — a list of keyed arrays is how you will hold all of `hesabu`'s transactions:
```php
$transactions = [
    ["amount" => 15000, "counterparty" => "Juma"],
    ["amount" => 8000,  "counterparty" => "Asha"],
];
echo $transactions[1]["counterparty"];   // Asha
```

**Reading a key that is not there** gives a warning (`Undefined array key`) and `null`.
Check first:
- `isset($a["fee"])` — the key exists *and* its value is not `null`.
- `array_key_exists("fee", $a)` — the key exists, even if the value is `null`.
- `$a["fee"] ?? 0` — the value, or `0` if missing. The one you will use most.

**Copies.** When you assign an array to another variable or pass it to a function, PHP
gives the function its **own copy**. Changing the copy does not change the original:

```php
function addFee(array $t): void
{
    $t["fee"] = 300;     // changes the function's copy only
}
$tx = ["amount" => 15000];
addFee($tx);
var_dump(isset($tx["fee"]));   // bool(false)
```

So a function that changes an array must **return** the new array, and the caller must use it:
`$tx = withFee($tx);`. This is a good thing: no function can quietly change your data.
Objects (Stage 2) do *not* behave this way, which is one reason Stage 2 spends time on them.

## Worked example
Stock in a shop, and what is running low.

```php
<?php
declare(strict_types=1);

$stock = ["sukari" => 12, "mchele" => 3, "mafuta" => 0, "unga" => 25];

function lowStock(array $stock, int $limit): array
{
    $low = [];
    foreach ($stock as $item => $quantity) {
        if ($quantity <= $limit) {
            $low[] = $item;
        }
    }
    return $low;
}

assert(lowStock($stock, 3) === ["mchele", "mafuta"]);
assert(lowStock([], 3) === []);
print_r(lowStock($stock, 3));
```

## Predict
1. `$a = [1, 2]; $b = $a; $b[] = 3; echo count($a);`
2. `$a = ["x" => null]; var_dump(isset($a["x"]), array_key_exists("x", $a));`
3. `$a = [5 => "tano"]; $a[] = "sita"; print_r($a);`
4. `$t = []; echo $t["total"] ?? 0;`

<details><summary>Answers</summary>

1. `2` — `$b` is a copy.
2. `bool(false)` then `bool(true)`.
3. `[5 => "tano", 6 => "sita"]` — `[]` adds after the highest number key.
4. `0`, with no warning.
</details>

## Exercises
`strict_types`, functions with types, asserts — as always now.

1. **`ledger.php`** — make a list of six invented transactions, each a keyed array with
   date, direction, amount, fee and counterparty. Write `totalIn(array $transactions): int`
   and `totalFees(array $transactions): int`. Assert both.
2. **`by-person.php`** — write `totalsByCounterparty(array $transactions): array` that gives
   back a keyed array of name → total received, for incoming transactions only. Assert the
   result for your six, and for an empty list.
3. **`copies.php`** — write a function that tries to change an array passed to it, and show
   with asserts that the original did not change. Then write the version that returns the
   new array, and assert that it works.

## Find the bug
This works, but prints warnings. Copy it, read the warnings, and fix it so there are none.

```php
<?php
declare(strict_types=1);
$payments = [["from" => "Juma", "amount" => 5000], ["from" => "Asha", "amount" => 3000],
             ["from" => "Juma", "amount" => 2000]];
$totals = [];
foreach ($payments as $p) {
    $totals[$p["from"]] += $p["amount"];
}
print_r($totals);
```

## Bring back
From Lesson 9: before fixing the bug above, write the warning's file, line and message in
`notes.md` and say what PHP was trying to read.

## Done when
- [ ] All three exercises pass their asserts, including the empty-list cases.
- [ ] `copies.php` proves the copy behaviour both ways.
- [ ] The bug runs with no warnings (`-d error_reporting=-1` to be sure).
- [ ] You can explain, without notes, the difference between `isset` and `array_key_exists`.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.arrays-functions --type implement --assistance A1 --task "Modelled transactions as nested arrays, totalled by counterparty, and showed arrays are copied into functions"
```
