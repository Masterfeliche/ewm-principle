# Stage 0 lessons: the ground floor

Ten lessons for someone who has never programmed. Every track (PHP, .NET, Go, Python) starts
here. No programming language yet: the terminal, finding answers, HTML and CSS, Git and GitHub,
how the web works, and databases. These are the tools every later stage takes for granted.

By the end you have what the [Stage 0 brief](../../briefs/core-stage-0.md) asks for: a personal
page live on the internet, in a Git repository with real commits and a merged pull request, a
file of SQL queries you wrote yourself, and notes on what your browser actually sent and received.

## The lessons
| # | Lesson | Time | What you end up with |
|---|---|---|---|
| 1 | [The terminal, and reading an error message](01-terminal.md) | 2–3 h | Confidence moving around and reading errors |
| 2 | [Finding answers](02-finding-answers.md) | 1–2 h | How to search, judge answers and ask a good question |
| 3 | [Your editor and your first HTML page](03-first-html-page.md) | 2 h | `my-page/index.html` |
| 4 | [HTML structure: headings, lists, links, images and forms](04-html-structure-and-forms.md) | 3 h | The full page, passing the validator |
| 5 | [CSS basics and mobile-first layout](05-css-mobile-first.md) | 3–4 h | A page that works well on a phone |
| 6 | [Git: saving your work's history](06-git-basics.md) | 3 h | `my-page` as a repository with clear commits |
| 7 | [GitHub: push, branches, pull requests, and your page live](07-github-and-pages.md) | 4 h | **The page live**, a merged pull request |
| 8 | [How the web works](08-how-the-web-works.md) | 2–3 h | `http-notes.md` |
| 9 | [Designing tables](09-designing-tables.md) | 3–4 h | Your own shop database |
| 10 | [SQL queries](10-sql-queries.md) | 4–5 h | `queries.sql`, and the gate |

About 30 hours of lessons. With practice and the week's wait before the rebuild, that fits the
stage's estimate of 2–4 weeks at 10–15 hours a week. Estimates, not deadlines.

Lessons 9–10 (databases) only need Lesson 1, so if you get tired of HTML you can do them
earlier. Lesson 8 needs your page live (Lesson 7).

## How each lesson works
The same parts every time: **Goal**, **The idea**, a **Worked example** (a similar problem,
solved and explained — type it out yourself), **Predict** (answer before you check), **Exercises**
(yours, in your own files), **Find the bug**, **Done when**, and **Record**. The
[PHP Stage 1 lessons](../php-stage-1/README.md) follow the same shape, so this is also practice
for how the rest of the track works.

## Where your work goes
```
~/my-page/                 your personal page: its own repository, published on GitHub Pages
    index.html, style.css, images/, README.md, http-notes.md

your learning repository (the one with .emw/ in it)
└── exercises/
    └── stage-0/
        ├── lesson-01/ … lesson-08/   notes and practice for each lesson
        └── sql/                      design.md, schema.sql, seed.sql, queries.sql
```
The page is a separate repository because it goes live on its own address. You type everything.

## Kiswahili–English words used in the lessons
| Kiswahili | English |
|---|---|
| duka | shop |
| bei | price |
| bidhaa | goods, products |
| sukari, unga, mchele, mafuta, chumvi | sugar, flour, rice, cooking oil, salt |
| mauzo | sales |
| hesabu | accounts |
| jina | name |
| tuma | send |
| mawasiliano | contact |
| moja, mbili | one, two |
| habari | hello (literally "news?") |

## For the agent running these lessons
Follow the "For the agent" section of the [PHP Stage 1 lessons README](../php-stage-1/README.md);
it applies here unchanged. Two additions for Stage 0:
- The learner may have **never used a terminal**. In Lesson 1, check they can open one before
  anything else, and do not assume a command worked until they tell you what it printed.
- Commands that delete or overwrite (`rm`, `git restore`, `>`) are taught deliberately. Before
  the learner runs one on real work, ask them what they expect it to do.
