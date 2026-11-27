# Lesson 1 — Install PHP, run a file, read your first error

**Time:** 2–3 hours · **Skills:** `core.terminal`, `php.syntax-types` · **Before this:** nothing
**Your folder:** `exercises/stage-1/lesson-01/`

## Goal
By the end you can open a terminal, move around folders, install PHP, run a PHP file,
try a line in the interactive shell, and read a PHP error message well enough to find
the line it is about.

## The terminal — where everything starts
The **terminal** (also called the command line or shell) is a text window where you type
commands instead of clicking. You will use it every day: to run PHP, install tools, use
Git, and later to talk to servers. It looks unfriendly at first. It is actually simple:
you type a command, press Enter, and it prints a result.

**Open it:**
- **Linux:** open "Terminal".
- **macOS:** open "Terminal" (Applications → Utilities).
- **Windows:** install WSL with Ubuntu (search "install WSL" on learn.microsoft.com),
  then open "Ubuntu". Everything in this track assumes a Linux-style terminal.

**Where am I?** The terminal is always "in" one folder, the **working directory**.

| Command | Does |
|---|---|
| `pwd` | print the folder you are in |
| `ls` | list what is in it (`ls -la` shows hidden files and details) |
| `cd folder` | go into a folder |
| `cd ..` | go up one folder |
| `cd ~` | go to your home folder |
| `mkdir name` | make a folder (`mkdir -p a/b/c` makes several levels) |
| `cat file` | print a file's contents |
| `cp from to` | copy a file |
| `mv from to` | move or rename |
| `rm file` | delete — **there is no bin; it is gone** |

**Paths.** `/home/asha/exercises/notes.md` is an **absolute** path (starts at the root `/`).
`exercises/notes.md` is **relative** (starts from where you are now). `.` means "this
folder", `..` means "the folder above".

**Saving effort:** press **Tab** to complete a name, **↑** for the last command,
**Ctrl+C** to stop something stuck.

**Errors.** When a command fails, read the message — it is almost always exactly right.
`command not found` = a typo or the tool is not installed.
`No such file or directory` = wrong name or wrong folder. Run `pwd` and `ls` to check.

## Finding answers
No programmer remembers everything. When you're stuck:
1. **Search the error message itself** — remove your file paths and add the tool name
   (e.g. `PHP 8.4 "unexpected token"`).
2. **Official docs first:** php.net/manual for PHP, git-scm.com/doc for Git.
3. **Judge an answer:** how old is it? Does it explain *why*? Do you understand every line?
4. **Ask a good question:** what you tried, what you expected, what happened instead, the
   exact error.

## The idea
PHP is a program that reads your `.php` file and runs it. On your machine you run it
from the terminal: `php file.php`. Later, a web server will run the same files when a
browser asks for a page; the language is the same.

Every PHP file starts with `<?php`. Each statement ends with a semicolon `;`. `echo`
prints text. `"\n"` inside double quotes is a new line.

When PHP cannot understand or run your code it prints an error. An error is not a
failure; it is PHP telling you exactly where to look. Every error has four parts:

| Part | Example | What it tells you |
|---|---|---|
| Kind | `Parse error` | When it broke: before running (parse) or while running (warning, fatal) |
| Message | `syntax error, unexpected token "echo"` | What PHP expected and what it found |
| File | `/home/asha/exercises/.../hello.php` | Which file |
| Line | `on line 3` | Where PHP *noticed* the problem. The mistake is often on the line before |

## Install
Pick your system. You need PHP 8.3 or newer.

- **Ubuntu or Debian:** `sudo apt update && sudo apt install php-cli php-mbstring php-xml php-curl php-zip unzip`
- **macOS:** install [Homebrew](https://brew.sh), then `brew install php`
- **Windows:** the easiest route is WSL (Windows Subsystem for Linux) with Ubuntu, then the
  Ubuntu line above. The alternative is the zip from https://windows.php.net/download
  added to your `PATH`.

Check it worked:

```bash
php -v
```

```bash
php -m
```

`php -v` prints the version. `php -m` lists the extensions; look for `mbstring` and
`json`. If `php` is "command not found", the install did not finish or PHP is not on
your `PATH`. Search that exact message with your system's name before asking anyone.

## Worked example
A file that prints a shop's opening hours. Read it, then type it yourself (do not copy
and paste: your fingers are part of the learning).

```php
<?php
echo "Duka la Mama Neema\n";
echo "Hufunguliwa saa 1 asubuhi\n";
echo "Hufungwa saa 3 usiku\n";
```

```bash
php hours.php
```

Three more tools you will use every day:
- `php -a` opens an interactive shell. Type `echo 2 + 3;` and press Enter. Type `exit` to leave.
- `php -l hours.php` checks a file for syntax errors without running it ("lint").
- `php -r 'echo 7 * 6;'` runs one line without a file.

## Predict
Write your answer down *before* you run anything. Then run it and compare.

1. `echo "Bei: " . 1500;` — what does it print? (`.` joins two pieces of text.)
2. `echo 'Karibu\n';` — what does it print? (Notice the single quotes.)
3. A file has `echo "a"` on line 2 (no semicolon) and `echo "b";` on line 3. Which line
   does the error mention?

<details><summary>Answers</summary>

1. `Bei: 1500`
2. `Karibu\n` — the two characters `\` and `n`, not a new line. Single quotes do not
   understand `\n`; double quotes do.
3. Line 3. PHP only notices the missing `;` when it reaches the next statement. This is
   why you always check the line *before* the one in the error too.
</details>

## Exercises
Write each in its own file in your lesson folder. You type everything.

0. **Terminal warm-up** — before writing any PHP, do this in the terminal:
   - Run `pwd` to see where you are.
   - Create your exercise folder: `mkdir -p exercises/stage-1/lesson-01`
   - `cd` into it. Run `pwd` again to confirm you are there.
   - Create an empty file: `touch hello.txt`, then `ls` to see it.
   If any command is new to you, try it twice. No notes needed — just get comfortable.
1. **`me.php`** — prints your name, the track you are on, and today's date, each on its own line.
2. **`breakit.php`** — start from a working copy of `me.php`. Make *one* mistake at a time,
   run it, and copy the error into `notes.md` with one line on what caused it. Do at least:
   a missing semicolon, `echo` spelled `ecko`, a missing closing `"`, and a missing `<?php`.
   The last one does not give an error at all — write down what happens instead, and why.
3. **Lint** each broken version with `php -l` before running it. Note in `notes.md` which
   mistakes `-l` caught.

## Find the bug
This should print two lines. It prints one line with odd characters in it. Find and fix it.

```php
<?php
echo 'Habari za asubuhi\n';
echo 'Karibu dukani\n';
```

## Done when
- [ ] `php -v` shows 8.3 or newer, and `php -m` lists `mbstring`.
- [ ] `me.php` runs and prints three lines.
- [ ] `notes.md` has at least four errors, each with its cause in your own words.
- [ ] You can explain, without notes, why an error can point at the line after the mistake.
- [ ] Everything is committed: `git add` and `git commit -m "Lesson 1: setup and first errors"`.

## Record
```bash
python .emw/tools/emw_track.py log core.terminal --type implement --assistance A1 --task "Installed PHP, ran files from the terminal, read and explained four kinds of PHP error"
```
Use the assistance level that is true for you: A0 if you used only documentation, A1 if
the agent asked questions or explained a concept.
