# Lesson 1 — The terminal, and reading an error message

**Time:** 2–3 hours · **Skills:** `core.terminal` · **Before this:** nothing
**Your folder:** `exercises/stage-0/lesson-01/`

## Goal
By the end you can move around your computer's folders from the terminal, create, copy,
move and delete files, run a program, and read the error when something goes wrong.

## The idea
The **terminal** (also called the command line or shell) is a text window where you type
commands instead of clicking. Programmers use it all day: to run code, install tools, use
Git and look at servers that have no screen at all.

It looks unfriendly at first. It is actually very simple: you type a **command**, press
Enter, and it prints a result. Most commands follow the same shape:

```
command  --option  argument
ls       -l        exercises
```

**Which terminal?**
- **Linux:** open "Terminal".
- **macOS:** open "Terminal" (in Applications → Utilities).
- **Windows:** install WSL with Ubuntu (search "install WSL" on learn.microsoft.com and
  follow Microsoft's steps), then open "Ubuntu". Everything in this track assumes a Linux-style
  terminal, and almost every server you will ever deploy to runs Linux.

**Where am I?** The terminal is always "in" one folder, the **working directory**.

| Command | Does | Example |
|---|---|---|
| `pwd` | print the folder you are in | `/home/asha` |
| `ls` | list what is in it (`ls -la` shows hidden files and details) | |
| `cd folder` | go into a folder | `cd exercises` |
| `cd ..` | go up one folder | |
| `cd ~` | go to your home folder | |
| `mkdir name` | make a folder (`mkdir -p a/b/c` makes several levels) | |
| `touch file` | make an empty file | |
| `cat file` | print a file | |
| `cp from to` | copy | `cp notes.md notes-old.md` |
| `mv from to` | move or rename | `mv old.md new.md` |
| `rm file` | delete a file — **there is no bin; it is gone** | |
| `command --help` | short help for most commands | `ls --help` |

**Paths.** `/home/asha/exercises/notes.md` is an **absolute** path: it starts at the top
(`/`). `exercises/notes.md` is **relative**: it starts from where you are now. `.` means
"this folder" and `..` means "the folder above".

**Saving effort:** press **Tab** to complete a file or folder name; press **↑** to bring
back the last command; **Ctrl+C** stops a command that is running or stuck.

**Errors.** When a command fails, the terminal tells you why. Read it — it is almost always
exactly right. The three you will see most:

| Error | Usually means |
|---|---|
| `command not found` | a typo, or the program is not installed |
| `No such file or directory` | wrong name or wrong folder — run `pwd` and `ls` |
| `Permission denied` | you are not allowed to read, write or run that file |

## Worked example
Setting up a folder for a small shop's notes, then tidying it.

```bash
pwd                          # /home/asha
mkdir -p duka/notes
cd duka/notes
touch bei.txt stock.txt
ls                           # bei.txt  stock.txt
echo "Sukari 3500" > bei.txt # > writes text into a file (replacing what was there)
echo "Unga 2800" >> bei.txt  # >> adds to the end
cat bei.txt                  # Sukari 3500
                             # Unga 2800
mv stock.txt hesabu.txt
cd ..
ls notes                     # bei.txt  hesabu.txt
cat notes/mauzo.txt          # cat: notes/mauzo.txt: No such file or directory
```

The last line fails on purpose. The error names the exact file it could not find.

## Predict
Each one starts again from `/home/asha/duka`, which holds the `notes` folder from the
worked example. Write down what each prints or where you end up.
1. `cd notes` then `pwd`
2. `cd ../..` then `pwd`
3. `ls notes/bei.txt`
4. `cat bei.txt` (from `/home/asha/duka`)

<details><summary>Answers</summary>

1. `/home/asha/duka/notes`
2. `/home` — `../..` goes up two levels: from `duka` to `asha`, then to `home`.
3. `notes/bei.txt` — `ls` of a single file just prints its name.
4. `No such file or directory` — `bei.txt` is in `notes`, not here.
</details>

## Exercises
Type every command yourself. Keep a list of what you typed in `commands.md`.

1. **Build a tree.** Inside `exercises/stage-0/lesson-01/`, create this, using only the terminal:
   ```
   practice/
   ├── a/
   │   └── one.txt   (containing "moja")
   └── b/
       └── two.txt   (containing "mbili")
   ```
   Then copy `one.txt` into `b`, rename `two.txt` to `pili.txt`, and delete the folder `a`
   (look up how `rm` deletes a folder — and read the warning about it first).
2. **Errors on purpose.** Cause each of the three errors in the table above. Copy each into
   `errors.md` with one sentence in your own words on what caused it.
3. **Help.** Use `ls --help` (or `man ls`) to find how to list files sorted by time, newest
   first. Write the command in `commands.md`.

## Find the bug
Someone typed these and got `No such file or directory` at the last line. Why? Fix it
without changing the last line.

```bash
cd ~
mkdir shop
touch shop/list.txt
cd shop
cat shop/list.txt
```

## Done when
- [ ] The `practice/` tree is built and changed exactly as described, using only the terminal.
- [ ] `errors.md` has all three errors with their causes.
- [ ] You can explain, without notes, the difference between an absolute and a relative path.
- [ ] You can move around, create and delete without looking at the table.

## Record
```bash
python .emw/tools/emw_track.py log core.terminal --type implement --assistance A1 --task "Built and changed a folder tree from the terminal; caused and explained three common errors"
```
Use A0 if you used only documentation, A1 if the agent asked questions or explained a concept.
