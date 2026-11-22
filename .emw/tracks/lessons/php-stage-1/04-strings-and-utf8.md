# Lesson 4 — Strings, UTF-8 and the `mb_` functions

**Time:** 3–4 hours · **Skills:** `php.syntax-types` · **Before this:** Lesson 3
**Your folder:** `exercises/stage-1/lesson-04/`

## Goal
By the end you can build, search, split, clean and format text in PHP, and you know which
functions break on letters outside plain English and what to use instead.

## The idea
A **string** is text. You will spend more time working with strings than anything else,
because almost everything a program receives — a file, a form, a text message — arrives
as text.

**Building strings**
- Single quotes `'...'` take the text exactly as written.
- Double quotes `"..."` understand `\n` and put variables inside: `"Habari, $name"`.
  Use braces when the variable is followed by letters or is an array item: `"{$name}ni"`.
- `.` joins strings: `"Bei: " . $price`. Always put spaces around it: `"5".3` is a syntax
  error, because PHP reads `.3` as the number 0.3.
- `sprintf` builds a string from a pattern: `sprintf("%s alilipa %d", $name, $amount)`.
- `number_format(15000)` gives `"15,000"`.

**Inspecting and changing strings** — look each one up on php.net when you use it:
`strlen`, `trim`, `strtolower`, `strtoupper`, `str_replace`, `str_contains`,
`str_starts_with`, `str_ends_with`, `strpos`, `substr`, `explode`, `implode`.

**UTF-8: the trap.** Computers store text as bytes. English letters take one byte each,
but letters such as `é`, `ë`, `ñ`, and every emoji, take two to four bytes. Most of the
functions above count **bytes**, not letters. For names and messages that may contain
such letters, use the multibyte versions, which count **characters**:

| Byte version (unsafe for names) | Character version |
|---|---|
| `strlen` | `mb_strlen` |
| `substr` | `mb_substr` |
| `strtoupper`, `strtolower` | `mb_strtoupper`, `mb_strtolower` |
| `ucwords` | `mb_convert_case($s, MB_CASE_TITLE)` |

Your users' names will not all be plain English letters. Assume they are not.

## Worked example
Printing a neat line on a receipt.

```php
<?php
$item = "  sukari   ";
$quantity = 2;
$price = 3500;

$item = trim($item);                         // "sukari"
$item = mb_convert_case($item, MB_CASE_TITLE); // "Sukari"
$total = $quantity * $price;

echo sprintf("%-10s x%d  TZS %s\n", $item, $quantity, number_format($total));
// Sukari     x2  TZS 7,000
```

`%-10s` means "a string, padded to 10 characters, lined up on the left". `%d` means "a
whole number". Look up `sprintf` on php.net for the rest — you will use it a lot.

## Predict
1. `echo strlen("José");`
2. `echo mb_strlen("José");`
3. `echo strtoupper("josé");`
4. `echo substr("Zoë Mushi", 0, 3);`
5. `var_dump(explode(",", "2026-03-14,IN,15000"));`
6. `var_dump(strpos("Umepokea Tsh5,000", "Umepokea"));`

<details><summary>Answers</summary>

1. `5` — `é` is two bytes.
2. `4`
3. `JOSé` — `strtoupper` only changes plain English letters.
4. `Zo` followed by a broken character: it cut `ë` in half.
5. An array of three strings: `"2026-03-14"`, `"IN"`, `"15000"`. Note the amount is
   still *text*.
6. `int(0)` — found at position 0, the very start. Remember this one for the bug below.
</details>

## Exercises
1. **`names.php`** — turn `"  asha MWAMBA "`, `"zoë   njeri"` and `"JOSÉ massawe"` into
   `"Asha Mwamba"`, `"Zoë Njeri"` and `"José Massawe"`. Notice the extra spaces in the
   middle of the second one; find a way to handle them.
2. **`line.php`** — take the text `"2026-03-14,IN,15000,300,Juma Ally,REF123"`, split it,
   and print each part with a label (`Tarehe:`, `Aina:`, `Kiasi:` and so on). Print the
   amount with `number_format`.
3. **`short.php`** — shorten a counterparty name to at most 10 characters, adding `…` when
   it was cut. Test it with a short name, a name of exactly 10 characters, a long name and
   a long name containing `ë`.

## Find the bug
This should print "Pesa imeingia" for any message that contains "Umepokea". It works for
some messages and not for others. Copy it, find which messages fail, then fix it.

```php
<?php
$message = "Umepokea Tsh5,000 kutoka JUMA";
if (strpos($message, "Umepokea")) {
    echo "Pesa imeingia\n";
} else {
    echo "Si malipo\n";
}
```

## Bring back
From Lesson 3: `strpos` returns either a number or `false`. Which of those numbers is
falsy? Write one line in `notes.md` linking this bug to the falsy values you learnt.

## Done when
- [ ] All three exercises give the right output for every input listed, including `ë`.
- [ ] The bug is fixed two ways: once with `str_contains`, once with `!== false`.
- [ ] You can explain, without notes, why `strlen("José")` is 5.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.syntax-types --type implement --assistance A1 --task "Cleaned, split and formatted strings with UTF-8-safe functions; fixed a strpos-at-position-0 bug"
```
