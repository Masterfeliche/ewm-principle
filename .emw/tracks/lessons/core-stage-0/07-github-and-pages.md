# Lesson 7 — GitHub: push, branches, pull requests, and your page live

**Time:** 4 hours · **Skills:** `core.git` · **Before this:** Lesson 6
**Your folder:** `my-page/`

## Goal
By the end your repository is on GitHub, your page is live at a public address, and you have
made a change on a branch, opened a pull request, merged it, and resolved a merge conflict.

## The idea
**Git** is the tool on your computer. **GitHub** is a website that hosts Git repositories so
you can back them up, share them, and work on them with others. Your copy is **local**; the one
on GitHub is the **remote**, usually called `origin`.

| Command | Does |
|---|---|
| `git remote add origin <url>` | connect your local repo to one on GitHub |
| `git push -u origin main` | send your commits up (`-u` remembers the link; after that just `git push`) |
| `git pull` | bring down commits made elsewhere and merge them in |
| `git clone <url>` | copy a repository from GitHub to a new folder |

**Signing in from the terminal.** GitHub does not accept your password for `git push`. The
simplest route is the GitHub CLI: install it from cli.github.com, run `gh auth login`, choose
HTTPS, and follow the browser steps. (SSH keys are the other route; GitHub's documentation
"Connecting to GitHub with SSH" explains them.)

**Branches.** A branch is a separate line of work. `main` is the version you trust. To try
something, make a branch, work there, and merge it back only when it is good.

| Command | Does |
|---|---|
| `git switch -c add-photo` | create a branch and move to it |
| `git switch main` | go back to `main` |
| `git branch` | list branches; `*` marks where you are |
| `git push -u origin add-photo` | put the branch on GitHub |

**Pull requests (PRs).** On GitHub, a pull request says "please merge my branch into `main`".
It shows the changes, and others can review and comment before it is merged. Professional
teams make almost every change this way. Write a PR description that says *what* changed
and *why*, and how to check it.

After merging on GitHub, update your local copy:
```bash
git switch main
git pull
```

**Merge conflicts.** If two branches change the same lines, Git cannot choose for you. It marks
the file like this:
```
<<<<<<< HEAD
<h1>Asha Mwamba</h1>
=======
<h1>Asha M. — junior developer</h1>
>>>>>>> new-title
```
Edit the file to the version you want, delete the three marker lines, then `git add` and
`git commit`. A conflict is not an error; it is Git asking you a question.

**README formatting** uses Markdown: `# Heading`, `**bold**`, `- list item`,
`[link text](https://…)`. GitHub shows it on the repository's front page.

**GitHub Pages** serves a repository's HTML as a website, free. In the repository on GitHub:
Settings → Pages → "Deploy from a branch" → `main`, folder `/ (root)` → Save. After a minute
or two the page is at `https://<username>.github.io/<repository>/`. Your `index.html` is the
front page. Every push to `main` updates the site.

**Public means public.** Everything in a public repository, including its whole history, can be
read by anyone. Never commit passwords, keys or other people's personal details. Deleting a file
later does not remove it from the history.

## Worked example
Your practice repository from Lesson 6, onto GitHub, with a branch.

```bash
cd ~/bei-practice
gh repo create bei-practice --public --source=. --push   # creates it on GitHub and pushes
git switch -c add-rice
echo "Mchele 2500" >> bei.txt
git add bei.txt
git commit -m "Add rice price"
git push -u origin add-rice
gh pr create --fill            # or open the link Git prints, and click "Create pull request"
```

Then on GitHub: open the pull request, read the "Files changed" tab, and click "Merge".
Back in the terminal: `git switch main` then `git pull`. `bei.txt` now has the rice line.

## Predict
1. You commit on your laptop but do not push. Your laptop is stolen. Is the commit on GitHub?
2. You are on branch `add-photo` and run `git push`. Which branch goes to GitHub?
3. You merge a PR on GitHub, then run `git log` locally on `main` without pulling. Do you see the merge?

<details><summary>Answers</summary>

1. No. Commits stay local until you push. Push at the end of every session.
2. `add-photo` (if you set it up with `-u`), not `main`.
3. No. Your local `main` does not know about it until `git pull`.
</details>

## Exercises
1. **Push** `my-page` to a new public GitHub repository.
2. **Go live** with GitHub Pages. Open the address on your computer *and* on a phone.
3. **A pull request** — on a branch, make one real improvement (for example a projects section
   or a better photo), push it, open a PR with a proper description, merge it, and pull.
4. **A conflict on purpose** — make branch `title-a` and change the `<h1>`, commit. Go back to
   `main`, make branch `title-b` and change the same `<h1>` differently, commit. Merge `title-a`
   into `main` (`git switch main`, `git merge title-a`), then merge `title-b`. Resolve the
   conflict, commit, push. Write the steps in `exercises/stage-0/lesson-07/notes.md`.
5. **README** — format it with a heading, the live link and a short list of what the page has.

## Find the bug
`git push` fails with `! [rejected] main -> main (fetch first)`. Explain in one sentence what
this means and what to do. (Search it with what you learnt in Lesson 2 if you need to.)

## Done when
- [ ] The page is live at a public address and works on a phone.
- [ ] One change went through a branch and a merged pull request with a description.
- [ ] You resolved a conflict yourself and the result is pushed.
- [ ] The README shows the live link.
- [ ] `git log --oneline` shows at least 8 commits with clear messages.

## Record
```bash
python .emw/tools/emw_track.py log core.git --type implement --assistance A1 --task "Pushed my page to GitHub, published it with Pages, merged a branch through a pull request and resolved a merge conflict"
```
Then record where the project lives:
```bash
python .emw/tools/emw_track.py ship --url https://<username>.github.io/<repository>/
```
