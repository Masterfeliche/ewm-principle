# Lesson 13 — Regular expressions with `preg_match`

**Time:** 4–5 hours · **Skills:** `php.syntax-types`, `php.testing-pest` · **Before this:** Lessons 4, 12
**Your folder:** `exercises/stage-1/hesabu/` and `exercises/stage-1/lesson-13/`

## Goal
By the end you can describe the shape of a piece of text as a regular expression, pull out
the parts you need with `preg_match`, and test your patterns against good and bad input.

## The idea
In Lesson 11 you parsed a message with `explode` and `strpos`. That works for one shape
and breaks the moment the wording shifts. A **regular expression** ("regex") describes the
*shape* of text, and PHP checks whether a string fits it and pulls out the pieces.

```php
$found = preg_match('~^Kiti (\d+)$~', "Kiti 12", $m);
// $found is 1, and $m[1] is "12"
```

- The pattern sits between two **delimiters**. `~` is a good choice because it rarely
  appears in text; `/` is common too, but then every `/` inside must be escaped as `\/`.
- `preg_match` gives back `1` (matched), `0` (did not match) or `false` (the pattern itself
  is broken). Test with `=== 1`.
- The third argument receives the captured pieces.

**The building blocks**

| Piece | Means | Example match |
|---|---|---|
| `abc` | exactly these letters | `abc` |
| `.` | any one character | `a`, `7`, ` ` |
| `\d` | a digit | `7` |
| `\s` | a space or tab | ` ` |
| `[A-Z]` | one character from a set | `K` |
| `[\d,]` | a digit or a comma | `,` |
| `+` | one or more of the previous | `\d+` → `15000` |
| `*` | zero or more | `\s*` → nothing, or spaces |
| `?` | optional | `Tsh\s?` → `Tsh` or `Tsh ` |
| `{2}`, `{1,3}` | exactly 2, or 1 to 3 | `\d{2}` → `14` |
| `^` and `$` | start and end of the text | stops extra text sneaking in |
| `(…)` | capture this piece | |
| `(?<name>…)` | capture with a name: `$m['name']` | |
| `(?:…)` | group without capturing | |
| `\.` | a real full stop (escaped) | `.` |
| `a\|b` | either | `TZS\|Tsh` |

Flags after the closing delimiter: `i` ignores upper/lower case; `u` treats the text as
UTF-8 (always add it for text people wrote — Lesson 4).

**Write patterns slowly.** Build them one piece at a time, testing each step. Use
https://regex101.com with the "PCRE2" flavour to see what each piece matches. Do not
paste real messages there — use your invented samples (house rule 5).

**Anchor them.** Without `^` and `$`, a pattern matches if the shape appears *anywhere*,
which lets malformed input through.

## Worked example
An invented bus ticket message: `Tiketi TK4821 Dar-Arusha 14/03/2026 Kiti 12`

```php
<?php
declare(strict_types=1);

function parseTicket(string $text): ?array
{
    $pattern = '~^Tiketi (?<code>TK\d+) (?<from>[A-Za-z]+)-(?<to>[A-Za-z]+) '
             . '(?<date>\d{2}/\d{2}/\d{4}) Kiti (?<seat>\d{1,2})$~u';

    if (preg_match($pattern, trim($text), $m) !== 1) {
        return null;
    }
    return [
        'code' => $m['code'],
        'route' => "{$m['from']}-{$m['to']}",
        'date' => $m['date'],
        'seat' => (int) $m['seat'],
    ];
}
```

And its tests, including the shapes that must *not* match:

```php
it('reads a ticket', function () {
    expect(parseTicket('Tiketi TK4821 Dar-Arusha 14/03/2026 Kiti 12'))
        ->toBe(['code' => 'TK4821', 'route' => 'Dar-Arusha', 'date' => '14/03/2026', 'seat' => 12]);
});

it('rejects text that is not a ticket', function (string $text) {
    expect(parseTicket($text))->toBeNull();
})->with([
    'promo' => ['Pata tiketi kwa bei nafuu leo!'],
    'seat too long' => ['Tiketi TK4821 Dar-Arusha 14/03/2026 Kiti 123'],
    'extra text' => ['Tiketi TK4821 Dar-Arusha 14/03/2026 Kiti 12 ASANTE'],
]);
```

Because `~` is the delimiter, the `/` in the date needs no escaping.

## Predict
1. `preg_match('~\d+~', 'Kiasi 500', $m); echo $m[0];`
2. `echo preg_match('~^\d+$~', '500 TZS');`
3. `echo preg_match('~^tsh~', 'Tsh500');`
4. `echo preg_match('~^tsh~i', 'Tsh500');`
5. `preg_match('~(\d+),(\d+)~', '15,000', $m); echo $m[1] . '|' . $m[2];`

<details><summary>Answers</summary>

1. `500`
2. `0` — `$` demands the text end after the digits.
3. `0` — case matters...
4. `1` — ...unless you add `i`.
5. `15|000`
</details>

## Exercises
1. **The amount parser** (in `hesabu/src/`). Build `parseAmount(string $text): int` from
   your Lesson 2 plan, turning `"Tsh15,000.00"`, `"TZS 15,000"`, `"15000"` (and every edge
   case you listed) into `15000`. Decide what to do with `"15,000.50"` — the house rules say
   whole shillings — and with text that is not an amount. For now, return `-1` for bad input;
   Lesson 16 replaces that with an exception. Pest tests with a dataset for every case.
   **This is the piece you will rebuild from memory a week from now. Understand every
   character of your pattern.**
2. **All your message shapes** (in `hesabu/src/`). Rewrite `parseLine` with one pattern per
   message shape you collected — at least three, as the brief requires. Use named groups.
   Use `parseAmount` for the amounts. Test each shape, plus a promotional message that must
   give `null`.
3. **`phone.php`** (lesson folder) — recognise Tanzanian mobile numbers written as
   `0712345678`, `0712 345 678`, `+255712345678` and `255712345678`, and give back the
   `+255…` form (house rule 4). Reject numbers that are too short or too long.

## Find the bug
This should accept only amounts with exactly two decimal places, like `15000.00`. Write a
test that proves it accepts something it should not, then fix it.

```php
function hasCents(string $text): bool
{
    return preg_match('~^\d+.\d{2}$~', $text) === 1;
}
```

## Security note
Never build a pattern by gluing in text from a user. Characters such as `.` or `(` would
change its meaning. If you must, wrap the text in `preg_quote($text, '~')` first. And keep
patterns simple: some badly written patterns (nested `+` and `*`, such as `(a+)+`) can take
minutes on a crafted input, which is a way to freeze a server.

## Project milestone
`hesabu` now parses every message shape you collected, and the amount parser is tested
against every edge case in the brief. Unreadable lines give `null` and are not counted.

## Done when
- [ ] `parseAmount` passes a dataset covering every format and edge case in your plan.
- [ ] At least three message shapes parse, each with its own test, and a promo gives `null`.
- [ ] The cents bug has a test that failed before your fix and passes after.
- [ ] You can explain, without notes, every character of your amount pattern.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.syntax-types --type implement --assistance A1 --task "Wrote anchored, tested regexes for amounts, three message shapes and phone numbers; fixed an unescaped dot"
```
