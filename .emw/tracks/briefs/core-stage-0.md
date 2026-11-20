# Stage 0 brief: Personal page and first queries

**Track:** core (all languages) · **Mode:** 1, you type everything · **Time:** 2–4 weeks (estimate)

## Goal
Put something of yours on the internet, under version control, and write your first database queries. Nothing here needs a programming language yet.

## Build
1. **A personal page.** One HTML page with a little CSS: who you are, what you are learning, and a list of the projects you will build on your track. It includes a heading structure, a list, a link, an image and a simple contact form (the form does not need to send anything).
2. **A Git repository** on GitHub holding the page, with a README that says what it is and how to view it.
3. **The page live** on a free static host (for example GitHub Pages).
4. **A file `queries.sql`** with 10 queries you wrote against a sample database (for example the SQLBolt lessons or a small shop database you create): at least two with `JOIN`, one with `GROUP BY`, one `INSERT`, one `UPDATE`.
5. **A file `http-notes.md`:** open your live page with the browser's network tab, and write down in your own words what was requested, the status codes you saw, and one request header and one response header and what each is for.

## It works when
- [ ] The page opens from a public link on a phone and on a computer.
- [ ] The repository has at least 8 commits with messages that say what changed.
- [ ] One change was made on a branch and merged with a pull request.
- [ ] Every query in `queries.sql` runs and has a one-line comment saying what it answers.
- [ ] You can explain, without notes, what happens between typing the address and seeing the page.

## Stretch change (transfer check)
Break the page on purpose on a branch (a wrong link, a missing closing tag), open a pull request, and write in the description how you would find the problem using the browser's developer tools. Then fix it.

## Rebuild from memory (a week later)
Without looking at your old work: create a new repository, add a page, commit, push, and publish it.

## Evidence to record
In `.emw-project/skill-ledger.yaml`, one item each for `core.terminal`, `core.git`, `core.html-css`, `core.http` and `core.sql`, with the date, what you did and the assistance level. Ask a mentor or peer to look at the repository and the live page, and mark that item `verified_by: human`.
