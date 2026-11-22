# Lesson 15 — Dates and time zones

**Time:** 3–4 hours · **Skills:** `php.files-errors` · **Before this:** Lessons 13–14
**Your folder:** `exercises/stage-1/hesabu/` and `exercises/stage-1/lesson-15/`

## Goal
By the end you can turn date text in more than one format into a date object in East
Africa Time, reject dates that do not exist, group by month, and filter by a date range.

## The idea
Never handle dates as text once they are inside your program. `"14/3/26"` and
`"2026-03-14"` are the same day; as text they are not even comparable. Convert them to a
**`DateTimeImmutable`** where they enter the program, the same "convert at the edge" rule
as Lesson 3.

**Time zones.** A moment in time is the same everywhere, but the clock reading differs.
Tanzania is on East Africa Time (UTC+3, no daylight saving), named `Africa/Dar_es_Salaam`.
PHP's default zone is usually UTC, so always say which zone you mean:

```php
$eat = new DateTimeZone('Africa/Dar_es_Salaam');
$d = new DateTimeImmutable('2026-03-14 14:15', $eat);
```

**Reading a known format** — the safe way for input you did not write:

```php
$d = DateTimeImmutable::createFromFormat('!j/n/y g:i A', '14/3/26 2:15 PM', $eat);
```

Format letters you will need (all on php.net under `DateTimeImmutable::createFromFormat`):
`d` day with zero (`04`), `j` day without (`4`), `m`/`n` month with/without zero, `Y`
four-digit year, `y` two-digit year, `H` 24-hour, `g` 12-hour, `i` minutes, `A` AM/PM.

Two traps:
- It gives back **`false`** if the text does not fit the format. Always check.
- Without `!` at the start of the format, any part you did not give (such as the time) is
  filled in from *now*. `!` sets the missing parts to zero instead.

**Impossible dates.** `31/02/2026` *fits* the format `d/m/Y`, so PHP quietly rolls it over
to 3 March and only records a warning. Check for it:

```php
$errors = DateTimeImmutable::getLastErrors();   // false when there were none
if ($errors !== false && $errors['warning_count'] > 0) { /* reject */ }
```

**Immutable means "never changes".** `$d->modify('+1 day')` gives back a *new* date and
leaves `$d` alone. (The older `DateTime` class changes itself, which causes bugs when two
parts of a program share one date. Use `DateTimeImmutable`.)

**Using dates**
- `$d->format('Y-m')` → `"2026-03"`, a perfect key for grouping by month.
- `$a < $b` compares two dates correctly.
- `$a->diff($b)->days` → the number of whole days between them.

## Worked example
Rent "paid until" dates for an invented landlord. A tenant pays for N months.

```php
<?php
declare(strict_types=1);

function paidUntil(DateTimeImmutable $start, int $months): DateTimeImmutable
{
    return $start->modify("+{$months} months");
}

$eat = new DateTimeZone('Africa/Dar_es_Salaam');
$start = new DateTimeImmutable('2026-01-31', $eat);

echo paidUntil($start, 1)->format('Y-m-d'), "\n";   // 2026-03-03 !
echo $start->format('Y-m-d'), "\n";                  // 2026-01-31 — unchanged
```

31 January plus one month is "31 February", which does not exist, so PHP rolls over to
3 March. A real rent system must decide what it wants instead (usually the last day of the
month: look up `modify('last day of next month')`). This is a decision for the landlord,
not for PHP's defaults, and the test you write should make that decision visible.

## Predict
1. `var_dump(DateTimeImmutable::createFromFormat('d/m/Y', '2026-03-14'));`
2. `$d = new DateTimeImmutable('2026-03-14'); $d->modify('+1 day'); echo $d->format('d');`
3. `echo (new DateTimeImmutable('2026-03-14 23:30', new DateTimeZone('UTC')))
   ->setTimezone(new DateTimeZone('Africa/Dar_es_Salaam'))->format('Y-m-d H:i');`

<details><summary>Answers</summary>

1. `bool(false)` — the text is not in the `d/m/Y` shape.
2. `14` — `modify` returned a new date, which was thrown away.
3. `2026-03-15 02:30` — the next day in Dar es Salaam. A transaction late at night UTC
   belongs to the *next* day's report in EAT. Getting this wrong puts money in the wrong month.
</details>

## Exercises
1. **`parseDate`** (in `hesabu/src/`) — `parseDate(string $text): ?DateTimeImmutable` that
   accepts at least the two date formats your samples use (the brief requires two in one
   file), in EAT, and gives `null` for text that fits no format *or* names an impossible date.
   Pest dataset: both formats, a date-only value, `31/02/2026`, `29/02/2028` (a leap year,
   so valid), and rubbish.
2. **Monthly totals** — change `totalsByMonth` from Lesson 11 to use real dates and
   `format('Y-m')`. Test a transaction at 23:30 on the last day of a month.
3. **Range filter** — `inRange(DateTimeImmutable $d, ?DateTimeImmutable $from,
   ?DateTimeImmutable $to): bool`, where `null` means "no limit", and both ends are
   included. Test the boundaries: a transaction at 00:00 on `from` and at 23:59 on `to`.
   (Careful: if `to` is `2026-03-31 00:00`, a payment at noon that day is "after" it. Decide
   how to handle that and test it.)

## Find the bug
This crashes on one of the inputs. Find which, read the error, and fix it so a bad date is
reported instead of crashing the program.

```php
<?php
declare(strict_types=1);
$eat = new DateTimeZone('Africa/Dar_es_Salaam');
foreach (['14/03/2026', '2026-03-14', '15/03/2026'] as $text) {
    $d = DateTimeImmutable::createFromFormat('!d/m/Y', $text, $eat);
    echo $d->format('Y-m-d'), "\n";
}
```

## Bring back
From Lesson 9: when you hit the crash, write the stack trace in your journal and say which
line *created* the bad value.

## Project milestone
`hesabu` now has real dates on every transaction, totals per month are correct across
time zones, and the `--from`/`--to` logic is tested (the options themselves come in Lesson 17).

## Done when
- [ ] `parseDate` rejects `31/02/2026` and accepts `29/02/2028`.
- [ ] Monthly totals put a late-night transaction in the right month.
- [ ] Range filter boundary tests pass, with your end-of-day decision written down.
- [ ] You can explain, without notes, why `DateTimeImmutable` is safer than `DateTime`.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.files-errors --type implement --assistance A1 --task "Parsed two date formats in EAT with impossible-date checks; month grouping and inclusive range filter with boundary tests"
```
