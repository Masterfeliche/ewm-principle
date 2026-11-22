# Lesson 2 — Finding answers

**Time:** 1–2 hours · **Skills:** `core.terminal` · **Before this:** Lesson 1
**Your folder:** `exercises/stage-0/lesson-02/`

## Goal
By the end you can find answers in official documentation, search an error message well,
judge whether an answer online can be trusted, and ask a question that gets a useful reply.

## The idea
No programmer remembers everything. What separates a fast programmer from a slow one is
mostly how quickly they find the right answer — and how well they can tell a good answer
from a bad one. This lesson is short, but you will use it every single day.

**1. Official documentation first.** It is the most accurate source, because the people
who made the tool wrote it.

| For | Go to |
|---|---|
| HTML, CSS, how the web works | MDN: developer.mozilla.org |
| Git | git-scm.com/doc (and the free *Pro Git* book) |
| SQL in SQLite | sqlite.org/lang.html |
| PHP (from Stage 1) | php.net/manual |
| Terminal commands | `command --help` and `man command` |

Documentation pages have a shape. Learn it once: a one-line summary, the **syntax**, the
**parameters** (what you can give it), the **return value** or result, **examples**, and
**notes and warnings**. Read the summary and an example first; read the rest when you need it.

**2. Search an error well.**
- Copy the **message itself**, not the parts that are about your machine. Remove your file
  paths, your username and your values: `cat: /home/asha/duka/x.txt: No such file` becomes
  `cat "No such file or directory"`.
- Add the tool and version: `git`, `sqlite`, `PHP 8.4`.
- Put an exact phrase in quotes.

**3. Judge an answer before you use it.**
- **How old is it?** A ten-year-old answer may describe a tool that has changed.
- **Does it explain why**, or only say "paste this"? Prefer answers that explain.
- **Do you understand every line?** If not, do not run it — especially anything with
  `sudo`, `rm` or `curl … | sh`, which can damage your computer.
- **Does the official documentation agree?**

**4. Ask a good question.** When you ask a person (or an AI), give them:
1. What you are trying to do (the goal, not just the step).
2. What you did — the exact command or code.
3. What you expected to happen.
4. What happened instead — the exact error, copied, not described.
5. What you already tried.

Writing these five things down solves the problem by itself surprisingly often.

**Never paste** passwords, keys, tokens or other people's personal data into a search box,
a forum or a chat with an AI.

**AI in this track.** The agent here is a coach. Ask it to explain a concept or an error,
not to write the answer. You will remember what you worked out; you will forget what you
were given.

## Worked example
A good question, written for a mentor about a Git problem:

> **Goal:** put my practice folder on GitHub.
> **Did:** `git push origin main`
> **Expected:** my files to appear on GitHub.
> **Got:** `error: src refspec main does not match any`
> **Tried:** searched the message; one answer said my branch might be called `master`. I
> ran `git branch` and it printed nothing at all.

The last line is the clue that solves it: `git branch` printed nothing because there are no
commits yet. A question this clear gets answered in a minute.

## Exercises
Write answers in `answers.md`.

1. **Documentation hunt.** Using only MDN, find: what the `alt` attribute on an image is for;
   what an HTTP 404 status means; and what `<label>` does in a form. For each, copy the
   page address and write the answer in one sentence *in your own words*.
2. **Search practice.** Here is an error: `bash: cd: /home/juma/projects/duka: No such file or directory`.
   Write the search you would type. Then find out what the `bash: cd:` part tells you.
3. **Judge two answers.** Search "how to delete a folder in terminal". Pick two different
   answers. For each write: how old, does it explain why, any danger, and whether you would
   use it.
4. **Ask a question.** Take one real problem you hit in Lesson 1 (or invent one) and write it
   up using the five parts above.

## Find the bug
What is wrong with this question? Rewrite it so it can be answered.

> "my git doesnt work, i tried everything, please help urgent"

## Done when
- [ ] `answers.md` has three MDN answers with page addresses, in your own words.
- [ ] You wrote a search that removes the parts specific to one machine.
- [ ] Two online answers are judged with all four checks.
- [ ] One question is written with all five parts.

## Record
```bash
python .emw/tools/emw_track.py log core.terminal --type explain --assistance A1 --task "Found answers in MDN, searched an error without local details, judged two online answers, wrote a five-part question"
```
