# Lesson 12 — Composer, and real tests with Pest

**Time:** 3–4 hours · **Skills:** `php.composer-autoload`, `php.testing-pest`, `core.testing` · **Before this:** Lessons 8–11
**Your folder:** `exercises/stage-1/hesabu/` (you continue the project here)

## Goal
By the end your `hesabu` project is a Composer project, its functions live in `src/`, and
its asserts have become Pest tests that you run with one command.

## The idea
**Composer** is PHP's package manager. It does three jobs:
1. **Installs libraries** other people wrote (such as Pest) into a `vendor/` folder.
2. **Records exactly which versions** you used, in `composer.lock`, so the project
   installs the same way on every machine.
3. **Autoloads** your own code, so you never write a pile of `require` lines.

The file `composer.json` describes your project. The important parts for now:

```json
{
    "name": "yourname/hesabu",
    "require": {
        "php": "^8.3"
    },
    "autoload": {
        "files": ["src/functions.php"]
    }
}
```

`"files"` tells Composer: "load this file whenever the project starts". It suits plain
functions. In Lesson 17 you will switch to PSR-4, the standard way to load classes.

After changing the `autoload` section, always run `composer dump-autoload`.

**Pest** is a test tool. A Pest test is a sentence and a check:

```php
test('formats shillings with commas', function () {
    expect(formatShillings(15000))->toBe('TZS 15,000');
});
```

`toBe` checks with `===`. Run all tests with `vendor/bin/pest`. Green means pass; red shows
exactly what was expected and what came instead.

**Datasets** run the same test with many inputs — perfect for boundaries:

```php
it('charges the right fee', function (int $amount, int $fee) {
    expect(feeFor($amount))->toBe($fee);
})->with([
    [999, 0],
    [1000, 200],
    [9999, 200],
]);
```

Tests are better than asserts because they live apart from the code, all run with one
command, give clear reports, and cannot be switched off by a setting.

## Set up
In your `hesabu` folder:

1. Install Composer by following https://getcomposer.org/download (check: `composer --version`).
2. `composer init` and answer the questions, or write `composer.json` by hand as above.
3. `composer require pestphp/pest --dev --with-all-dependencies`
4. `vendor/bin/pest --init` — creates `tests/` and `phpunit.xml`.
5. Add `/vendor/` to `.gitignore`. **Do** commit `composer.json` and `composer.lock`.
6. `composer audit` — checks your installed packages for known security problems. Run it
   whenever you add a package.

## Worked example
The share-out function from Lesson 8 as a tested Composer project, in a separate practice
folder (not in `hesabu`):

```php
<?php
// src/functions.php
declare(strict_types=1);

function shareOut(int $groupTotal, int $memberShares, int $allShares): int
{
    if ($allShares <= 0) {
        return 0;
    }
    return intdiv($groupTotal * $memberShares, $allShares);
}
```

```php
<?php
// tests/ShareOutTest.php
declare(strict_types=1);

it('gives each member their share', function (int $total, int $mine, int $all, int $expected) {
    expect(shareOut($total, $mine, $all))->toBe($expected);
})->with([
    'a quarter' => [1000000, 10, 40, 250000],
    'no shares' => [1000000, 0, 40, 0],
    'empty group' => [1000000, 10, 0, 0],
]);
```

Naming each dataset row (`'a quarter'`) makes a failing test say *which* case failed.

## Exercises
1. **Move the code.** Move `parseLine` and every helper from Lesson 11 into
   `src/functions.php`. Your main file now only loads `vendor/autoload.php` and calls them.
2. **Convert the asserts.** Turn every assert you wrote for these functions into Pest tests
   in `tests/`. Use a dataset wherever you test several inputs.
3. **Test the edge.** Add tests for a line that is not a transaction, an empty line, and an
   amount with commas. Watch them go red if the code does not handle them yet — that is fine,
   and it is the point. Make them pass.

## Find the bug
After adding `"files": ["src/functions.php"]` to `composer.json`, running the tests gives
`Call to undefined function parseLine()`. The function is definitely in `src/functions.php`.
What was forgotten? (The answer is in "The idea" above. Find it without asking.)

## Bring back
From Lesson 9: make one test fail on purpose and read Pest's report the way you read a
stack trace. Which line, what was expected, what came instead?

## Done when
- [ ] `composer install` from a fresh clone, then `vendor/bin/pest`, runs every test green.
- [ ] Every earlier assert for these functions is now a Pest test.
- [ ] `vendor/` is ignored; `composer.json` and `composer.lock` are committed.
- [ ] `composer audit` reports no problems.
- [ ] You can explain, without notes, what `composer.lock` is for.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.testing-pest --type implement --assistance A1 --task "Made hesabu a Composer project, moved functions to src/, and converted asserts to Pest tests with datasets"
```
Also log `php.composer-autoload` with what you did for it.
