# Lesson 6 — Git: saving your work's history

**Time:** 3 hours · **Skills:** `core.git`, `core.terminal` · **Before this:** Lessons 1, 3–5
**Your folder:** `my-page/`

## Goal
By the end your page is a Git repository, you commit changes with clear messages, you can
see what changed and when, and you can undo a change you regret.

## The idea
**Git** records snapshots of a folder over time. Each snapshot is a **commit**: the state of
every file, who made it, when, and a message saying why. With Git you can see exactly what
changed, go back to any earlier version, and (Lesson 7) work with other people without
overwriting each other.

A folder tracked by Git is a **repository** ("repo"). Git keeps its records in a hidden
`.git` folder inside it. Never edit that folder by hand.

**The three places a change can be:**

```
working folder  --git add-->  staging area  --git commit-->  history
(your edits)                  (ready to commit)              (saved for good)
```

Staging lets you choose exactly what goes into a commit — for example, one finished change
while another is still half done.

**Set up once per computer:**
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```
Use the email you will use on GitHub. It becomes public in your commits.

**The everyday commands**

| Command | Does |
|---|---|
| `git init` | make the current folder a repository |
| `git status` | what changed and what is staged — run it constantly |
| `git add file` | stage a file (`git add .` stages everything here) |
| `git commit -m "message"` | save the staged changes as a commit |
| `git log --oneline` | the history, one line per commit |
| `git diff` | what changed and is *not* staged yet |
| `git diff --staged` | what is staged and about to be committed |
| `git restore file` | throw away unstaged changes to a file — **they are gone** |
| `git restore --staged file` | unstage, keeping your edits |

**Good commit messages.** Your history is a story for your future self and your colleagues.
- Start with a verb, say what the commit *does*: "Add contact form", "Fix image overflowing on phones".
- Keep the first line short (under about 60 characters).
- One idea per commit. "Lots of changes" tells nobody anything.
- Bad: `update`, `fix`, `asdf`, `final final 2`.

**`.gitignore`** lists files Git should never track: editor settings, system files, and later,
secrets and downloaded packages. A file named `.gitignore` with these lines is a good start:
```
.DS_Store
Thumbs.db
.vscode/
```

## Worked example
A practice repository for an invented shop's price list (not your page).

```bash
mkdir ~/bei-practice && cd ~/bei-practice
git init
echo "Sukari 3500" > bei.txt
git status                    # bei.txt is "untracked"
git add bei.txt
git commit -m "Add price list with sugar"
echo "Unga 2800" >> bei.txt
git diff                      # shows +Unga 2800
git add bei.txt
git commit -m "Add flour price"
echo "Mafuta 99999" >> bei.txt  # a mistake
git restore bei.txt           # gone; the file is back to the last commit
git log --oneline
# 3f2a1c9 Add flour price
# 8b7e0d4 Add price list with sugar
```

(Your commit ids will be different: each one is a fingerprint of its contents.)

## Predict
1. You edit `index.html` and run `git commit -m "Change heading"` without `git add`. What happens?
2. You run `git add index.html`, then edit `index.html` again, then commit. Which version is committed?
3. You run `git restore index.html` after editing it. Can you get your edits back?

<details><summary>Answers</summary>

1. Nothing is committed: Git says there is nothing staged ("no changes added to commit").
2. The version at the moment you ran `git add`. The later edit is still unstaged — `git status`
   shows the file in both lists.
3. No. Unstaged edits that you restore were never saved by Git. Commit often.
</details>

## Exercises
1. **Make `my-page` a repository.** Set up your name and email, `git init`, add a `.gitignore`,
   and make your first commit of the page as it is now.
2. **Small commits.** Make at least four separate improvements to your page (a section, a
   style change, a fix found by the validator, the README in the next exercise) — each its own
   commit with a clear message. The brief asks for at least 8 commits by the end of the stage.
3. **README.md** — say what the page is and how to view it. Plain text is fine; Lesson 7 shows
   the formatting.
4. **Undo practice.** Make a deliberate mess in `style.css` without committing, look at it with
   `git diff`, then restore it. Stage a file and unstage it. Write in
   `exercises/stage-0/lesson-06/notes.md` which command did what.

## Find the bug
Someone says "Git lost my work!". Read what they typed and explain what actually happened,
and what they should have done.

```bash
git add index.html
git commit -m "Add about section"
# ...two hours of work on index.html and style.css...
git restore .
```

## Done when
- [ ] `my-page` is a repository with a `.gitignore` and a README.
- [ ] `git log --oneline` shows at least five commits with clear, verb-first messages.
- [ ] You have used `git diff`, `git restore` and `git restore --staged` and know which does what.
- [ ] You can explain, without notes, the three places a change can be.

## Record
```bash
python .emw/tools/emw_track.py log core.git --type implement --assistance A1 --task "Put my page under Git, made small commits with clear messages, and practised diff, restore and unstaging"
```
