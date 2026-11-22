# Lesson 14 — Files, CSV and JSON

**Time:** 3–4 hours · **Skills:** `php.files-errors` · **Before this:** Lessons 10–13
**Your folder:** `exercises/stage-1/hesabu/` and `exercises/stage-1/lesson-14/`

## Goal
By the end you can read a text file line by line, read and write CSV, turn PHP arrays into
JSON and back, and handle a file that is missing or empty.

## The idea
**Paths.** A relative path such as `samples/a.txt` is relative to the folder you *ran the
command from*, not to the PHP file. To point at a file next to your code, build the path
from `__DIR__`, the folder of the current file: `__DIR__ . '/../samples/a.txt'`. A path the
user types on the command line is relative to where *they* are, which is what you want.

**Check first.**
- `is_file($path)` — exists and is a file (not a folder).
- `is_readable($path)` — you are allowed to read it.

**Reading text, line by line**
```php
$lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
```
gives a list of lines, without the line endings, skipping blank ones. It gives `false` if
the file cannot be read. Fine for files of a few megabytes. (For huge files you would read
one line at a time with `fopen` and `fgets`.)

**Reading CSV**
```php
$handle = fopen($path, 'r');
$header = fgetcsv($handle, null, ',', '"', '');
while (($row = fgetcsv($handle, null, ',', '"', '')) !== false) {
    $record = array_combine($header, $row);
    // ...
}
fclose($handle);
```
- Pass all five arguments to `fgetcsv`. PHP 8.4 warns when the last one (`escape`) is left
  out, because its default is going to change. `''` switches the old escape behaviour off.
- `array_combine($header, $row)` pairs column names with values, giving a keyed array.
  It fails if a row has a different number of columns — a real edge case.
- **Every value from a CSV is a string.** Convert amounts with your `parseAmount`.
- Files saved from Excel often begin with three invisible bytes (a "BOM",
  `"\xEF\xBB\xBF"`), which end up glued to the first column name. Strip them from the header.

**Writing CSV:** `fputcsv($handle, $row, ',', '"', '')`, with a handle opened with `'w'`.

**JSON** is how programs swap data:
```php
$json = json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
$back = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
```
- `JSON_UNESCAPED_UNICODE` keeps `ë` as `ë` instead of `ë`.
- `JSON_THROW_ON_ERROR` makes bad JSON throw an error instead of quietly giving `null`.
- `true` in `json_decode` gives arrays instead of objects.

## Worked example
Stock value from an invented shop's CSV.

`stock.csv`:
```
item,quantity,unit_cost
Sukari,12,3000
Mchele,30,2500
Mafuta,8,6500
```

```php
<?php
declare(strict_types=1);

function stockValue(string $path): int
{
    if (!is_file($path) || !is_readable($path)) {
        fwrite(STDERR, "Cannot read $path\n");
        return 0;
    }
    $handle = fopen($path, 'r');
    $header = fgetcsv($handle, null, ',', '"', '');
    $total = 0;
    while (($row = fgetcsv($handle, null, ',', '"', '')) !== false) {
        $item = array_combine($header, $row);
        $total += (int) $item['quantity'] * (int) $item['unit_cost'];
    }
    fclose($handle);
    return $total;
}

echo stockValue(__DIR__ . '/stock.csv'), "\n";   // 163000
```

`STDERR` is where error messages go, separate from the normal output, so that a report
piped into a file does not fill up with errors. Lesson 16 improves how this handles errors.

## Predict
You run `php src/read.php` from the project folder, and `read.php` contains
`file('samples/a.txt')`.
1. Where does PHP look for the file?
2. What if you run `cd src && php read.php`?
3. `var_dump(json_encode(['jina' => 'Zoë']));`
4. `var_dump(json_decode('{"kiasi": 500'));` — the closing brace is missing.

<details><summary>Answers</summary>

1. `./samples/a.txt` in the project folder — it works.
2. `src/samples/a.txt` — it fails. Same code, different folder. This is the bug below.
3. `string(19) "{"jina":"Zoë"}"` — the `ë` is escaped without `JSON_UNESCAPED_UNICODE`.
4. `NULL` — silently. With `JSON_THROW_ON_ERROR` it would throw a `JsonException`.
</details>

## Exercises
1. **Samples** — in `hesabu/samples/`, make `statement.csv` with the columns the brief lists
   (date, type, amount, fee, counterparty, reference, balance) and ten invented rows, and
   `messages.txt` with ten invented message lines in your shapes, two promos and one blank
   line. Document the CSV columns in the README.
2. **Readers** — in `hesabu/src/`, write `readMessages(string $path): array` and
   `readCsvStatement(string $path): array`, each giving back a list of lines or rows. A
   missing file and an empty file must not crash. Test them with Pest, using small sample
   files in `tests/fixtures/`.
3. **JSON** — `toJson(array $report): string` (lesson folder first, then move it into
   `hesabu`). Test that a name with `ë` comes out readable, and that decoding your output
   gives back exactly the array you started with.

## Find the bug
This works from the project folder and fails from anywhere else. Fix it so it works
wherever it is run from.

```php
<?php
declare(strict_types=1);
$lines = file('samples/messages.txt', FILE_IGNORE_NEW_LINES);
echo count($lines), "\n";
```

## Security and data
- Your samples are invented. Never commit a real statement or real messages — even
  "anonymised" ones often still identify people (house rules 5 and 6).
- `hesabu` only reads the file it is given. It must never write to it or delete it.

## Project milestone
`hesabu` reads a real file now: it reads `messages.txt` or a CSV, parses every line, and
prints the total received. A missing or empty file gives a clear message, not a crash.

## Done when
- [ ] Both readers have Pest tests, including a missing file, an empty file and a CSV row
  with the wrong number of columns.
- [ ] A CSV saved with a BOM still reads its first column correctly.
- [ ] The bug works from any folder.
- [ ] `hesabu samples/messages.txt` prints the correct total.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log php.files-errors --type implement --assistance A1 --task "Read text and CSV statements with tested readers handling missing, empty and malformed files; wrote JSON output"
```
