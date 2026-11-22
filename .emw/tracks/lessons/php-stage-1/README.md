# PHP Stage 1 lessons: language foundations

Eighteen lessons that take a complete beginner from installing PHP to a finished, tested
command-line tool: `hesabu`, the [Stage 1 project](../../briefs/php-stage-1.md). Do them in
order. Each one builds on the ones before it, and the project grows a piece at a time from
Lesson 8 on.

Before Lesson 1 you need Stage 0 (terminal, Git, a little HTML and SQL): see the
[Stage 0 lessons](../core-stage-0/README.md). If you skipped it, do at least the terminal and
Git lessons first.

## The lessons
| # | Lesson | Time | Project step |
|---|---|---|---|
| 1 | [Install PHP, run a file, read your first error](01-setup.md) | 1–2 h | |
| 2 | [Thinking before coding](02-thinking-before-coding.md) | 2–3 h | Plan the amount parser |
| 3 | [Variables, types, and `==` versus `===`](03-variables-and-types.md) | 2–3 h | |
| 4 | [Strings, UTF-8 and the `mb_` functions](04-strings-and-utf8.md) | 3–4 h | |
| 5 | [Integers, floats, and why money stays in integers](05-numbers-and-money.md) | 2–3 h | |
| 6 | [Decisions with `if` and `match`, and your first tests](06-decisions-and-first-tests.md) | 3 h | |
| 7 | [Loops](07-loops.md) | 3 h | |
| 8 | [Functions, types and `strict_types`](08-functions-and-types.md) | 3–4 h | **Plan `hesabu` on paper** |
| 9 | [Debugging 1: read the error, shrink the problem](09-debugging-1.md) | 3 h | |
| 10 | [Arrays, and how PHP copies them](10-arrays.md) | 3–4 h | |
| 11 | [Array functions and closures](11-array-functions-and-closures.md) | 4 h | **Parse one message shape** |
| 12 | [Composer, and real tests with Pest](12-composer-and-pest.md) | 3–4 h | **Composer project with tests** |
| 13 | [Regular expressions with `preg_match`](13-regular-expressions.md) | 4–5 h | **All message shapes, amount parser** |
| 14 | [Files, CSV and JSON](14-files-csv-json.md) | 3–4 h | **Read real files** |
| 15 | [Dates and time zones](15-dates-and-time-zones.md) | 3–4 h | **Real dates, monthly totals** |
| 16 | [Exceptions and handling bad input](16-exceptions-and-bad-input.md) | 3–4 h | **Every edge case handled** |
| 17 | [Command-line options and PSR-4 packaging](17-cli-and-psr4.md) | 4–5 h | **The finished tool** |
| 18 | [Debugging 2: a step debugger, and refactoring](18-debugging-2-and-refactoring.md) | 4–5 h | **Refactor with tests green** |

About 60 hours of lessons. With the exercises, the project and the time for things to sink
in, that fits the stage's estimate of 2–3 months at 10–15 hours a week. These are estimates;
nobody is behind.

## How each lesson works
Every lesson has the same parts, in the same order:

1. **Goal** — what you can do at the end.
2. **The idea** — the concept in plain words.
3. **Worked example** — a complete, explained solution to a *similar* problem. Read it, then
   type it out yourself and run it. It never solves the exercises for you.
4. **Predict** — short questions to answer *before* running anything. Write your answer
   down first, then check. Answers are hidden under "Answers".
5. **Exercises** — two to four problems you solve in your own files.
6. **Find the bug** — a short program with a planted bug. Reading broken code is half the job.
7. **Bring back** — one thing from an earlier lesson, so it does not fade.
8. **Done when** — a checklist. The lesson is finished when every box is ticked.
9. **Record** — the command that adds the evidence to your skill ledger.

## Where your code goes
```
exercises/
└── stage-1/
    ├── lesson-01/        one folder per lesson, for its exercises and notes
    ├── lesson-02/
    ├── ...
    ├── hesabu-plan.md    your plan from Lesson 8
    └── hesabu/           the project, from Lesson 11 on
```
You type every line. Commit at the end of each lesson, and more often during the project.

## Kiswahili–English words used in the lessons
| Kiswahili | English |
|---|---|
| hesabu | accounts, calculation |
| kiasi | amount |
| jumla | total |
| ada | fee |
| salio | balance |
| tarehe | date |
| imepokelewa / umepokea | received / you have received |
| imetumwa | sent |
| mauzo | sales |
| matumizi | expenses |
| madeni | debts |
| duka | shop |
| bei | price |
| hakuna kitu | nothing |
| si sahihi | not valid |
| faili halipo | the file does not exist |

## For the agent running these lessons
These lessons are part of Prompt 12 (learning track) and follow Prompt 11 (practice), with
one addition for learners at M0–M1:

- **Teach the lesson in order.** Start with the goal, explain the idea in your own words
  (shorter or slower as the learner needs), then walk through the worked example. The worked
  example may be shown and discussed in the chat: it solves a different problem from the
  exercises.
- **Run the Predict questions as questions.** Ask one at a time, wait for an answer, then
  have the learner run it. Do not reveal the answer first. Say *why* you are asking: making a
  prediction and checking it is what makes it stick.
- **Exercises follow Prompt 11 in full.** The learner writes in their own files, runs the
  code themselves, and you do not write in their files. Hint ladder one step at a time. No
  solution code before a real attempt.
- **Do not skip ahead** to a later lesson's topic because the learner's code would be
  "better" with it. If they ask about it, say which lesson covers it.
- **At the end, go through "Done when" together** and help them record the evidence with
  an honest assistance level.
- If the learner already knows a lesson's topic, let them prove it: the Predict questions,
  the bug, and one exercise without hints. If they get them right, move on and record it at A0.
