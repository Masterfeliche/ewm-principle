# Lesson 17 — Command-line options and PSR-4 packaging

**Time:** 4–5 hours · **Skills:** `php.composer-autoload`, `php.files-errors` · **Before this:** Lessons 12–16
**Your folder:** `exercises/stage-1/hesabu/`

## Goal
By the end `hesabu` is a finished command-line tool: `bin/hesabu` with `--from`, `--to`,
`--lang` and `--json`, its code in namespaced classes loaded by Composer's PSR-4 autoloader.

## The idea
**Arguments.** Whatever is typed after the script name arrives in `$argv`, a list of strings.
`$argv[0]` is the script itself. `php bin/hesabu data.txt --json` gives
`['bin/hesabu', 'data.txt', '--json']`.

**Options with `getopt`.** Parsing `$argv` by hand gets messy fast. `getopt` does it:

```php
$options = getopt('', ['from:', 'to:', 'lang:', 'json'], $restIndex);
$files = array_slice($argv, $restIndex);
```

- `'from:'` — the colon means the option needs a value: `--from=2026-03-01`.
- `'json'` — no colon: a switch, present or absent.
- `$restIndex` receives the position where the non-option arguments start.
- A switch that is present is stored with the value **`false`** (yes, really). So test it
  with `isset($options['json'])` or `array_key_exists`, never with `if ($options['json'])`.
- `getopt` stops reading options at the first argument that is not an option. More in the
  bug below.

Validate every option exactly as you validate file input: a `--from` that is not a date and
a `--lang` other than `sw` or `en` get a clear message and exit code `1`.

**An executable entry point.** `bin/hesabu` (no `.php`) starts with a "shebang" line so the
system knows to run it with PHP:

```php
#!/usr/bin/env php
<?php
declare(strict_types=1);

require __DIR__ . '/../vendor/autoload.php';
// read options, call your code, print, exit
```

Make it executable once: `chmod +x bin/hesabu`. Now `bin/hesabu samples/mixed.txt` works.
Add `"bin": ["bin/hesabu"]` to `composer.json`, so a project that installs yours gets it too.
(On Windows outside WSL, run it as `php bin/hesabu`.)

**Namespaces** stop your names clashing with everyone else's. Your code goes in the
`Hesabu` namespace:

```php
<?php
declare(strict_types=1);

namespace Hesabu;

final class Greeter
{
    public function greet(string $name): string
    {
        return "Habari, {$name}";
    }
}
```

Another file uses it with `use Hesabu\Greeter;` and then `new Greeter()`. This is the
whole of what you need to know about classes in Stage 1: a class groups related functions
(called **methods**), and `new` creates one so you can call them with `->`. Stage 2 covers
what classes are really for.

**PSR-4** is the standard rule linking namespaces to folders: the class `Hesabu\Greeter`
lives in `src/Greeter.php`; `Hesabu\Parse\Amount` lives in `src/Parse/Amount.php`. Tell
Composer once:

```json
"autoload": {
    "psr-4": { "Hesabu\\": "src/" }
}
```

then `composer dump-autoload`. From then on any class is loaded the first time you use it.
File names must match class names **exactly, including capitals** — Windows and macOS
forgive a mismatch, Linux servers do not.

## Worked example
A tiny command-line greeter, `salamu`, in a separate practice folder (not `hesabu`).

```php
#!/usr/bin/env php
<?php
declare(strict_types=1);

$options = getopt('', ['lang:'], $restIndex);
$names = array_slice($argv, $restIndex);
$lang = $options['lang'] ?? 'sw';

if (!in_array($lang, ['sw', 'en'], true)) {
    fwrite(STDERR, "--lang must be sw or en\n");
    exit(1);
}
if ($names === []) {
    fwrite(STDERR, "Usage: salamu [--lang=sw|en] NAME...\n");
    exit(1);
}
foreach ($names as $name) {
    echo ($lang === 'sw' ? 'Habari, ' : 'Hello, '), $name, "\n";
}
exit(0);
```

`./salamu --lang=en Asha Juma` prints two lines. `./salamu --lang=fr Asha` exits with 1.
Note the third argument to `in_array`: `true` makes it compare strictly (Lesson 3).

## Predict
1. `getopt('', ['json'])` when run with `--json`: what is `$options['json']`?
2. `php tool.php --lang=en file.txt` with `getopt('', ['lang:'], $i)`: what is `$i`?
3. Composer's PSR-4 autoloader is asked for `Hesabu\Report\Printer`. Which file does it load?

<details><summary>Answers</summary>

1. `false`. Present switches are stored as `false`. Use `isset`.
2. `2` — `$argv` is `['tool.php', '--lang=en', 'file.txt']`, and the file is at position 2.
3. `src/Report/Printer.php`.
</details>

## Exercises
1. **Classes** — move your code from `src/functions.php` into a few small classes under
   `src/`, for example `Hesabu\Parser` (lines → transactions), `Hesabu\Report` (transactions
   → totals) and `Hesabu\Output` (totals → text or JSON). Switch `composer.json` to PSR-4.
   Every test must still pass — update the tests to use the classes.
2. **`bin/hesabu`** — the entry point with `--from`, `--to`, `--lang=sw|en` (Kiswahili by
   default, house rule 1) and `--json`. Invalid options give a message on `STDERR` and exit 1.
   Print a usage line when no file is given.
3. **The report** — everything the brief's "Report" section lists: totals in and out per
   month, fees per month, top five counterparties, and the unreadable lines. Labels in both
   languages. `--json` prints the same report as JSON.
4. **README** — formats, options and sample output, as the brief requires.

## Find the bug
`bin/hesabu --json samples/mixed.txt` prints JSON. `bin/hesabu samples/mixed.txt --json`
prints the text report — the `--json` is ignored. Find out why from the `getopt` page on
php.net, then decide: fix it, or document the required order in the usage line? Write
your decision and the reason in the README.

## Project milestone: the finished tool
Go through the brief's "It works when" list, one line at a time:
- `composer install` then `bin/hesabu samples/mixed.txt` prints the report with no warnings.
- All money is integers. `strict_types` and full types in every file.
- Unreadable lines never stop the run and are listed.
- Tests cover every message shape and edge case, and pass.
- The README is complete.

## Done when
- [ ] A fresh clone, `composer install`, `vendor/bin/pest` → all green.
- [ ] `bin/hesabu` handles every option, rejects bad ones with exit 1, and prints usage.
- [ ] Every line of the brief's "It works when" is ticked.
- [ ] Your decision on the option-order bug is in the README.
- [ ] Committed and pushed.

## Record
```bash
python .emw/tools/emw_track.py log php.composer-autoload --type implement --assistance A1 --task "Packaged hesabu with PSR-4 classes and an executable bin/hesabu with validated getopt options"
```
Then record the project: `python .emw/tools/emw_track.py ship --url <your repository URL>`.
