# Lesson 2 — Thinking before coding

**Time:** 2–3 hours · **Skills:** `core.testing`, `php.syntax-types` · **Before this:** Lesson 1
**Your folder:** `exercises/stage-1/lesson-02/`

## Goal
By the end you can take a problem written in plain words and turn it into inputs,
outputs, examples, edge cases and numbered steps — before writing any code — and check
your steps by hand.

## The idea
Beginners rarely get stuck on syntax. They get stuck on "where do I even start?" The
answer is: not in the editor. Experienced engineers solve the problem on paper first,
then translate. Translating is the easy part.

Use the same six questions every time:

1. **Say it back.** Rewrite the problem in one sentence, in your own words.
2. **Inputs.** What do I get? What type is each thing (text, whole number, list)?
3. **Output.** What must I give back, exactly? What does it look like?
4. **Examples.** Two or three normal inputs with the output you expect, worked out by hand.
5. **Edge cases.** Empty input. One item. Zero. A huge value. Bad input. Ties.
6. **Steps.** Numbered, plain-language steps (pseudocode). Each step does one thing.

Then **trace** the steps by hand with one of your examples, writing down the value of
everything after each step. If your trace gives the wrong answer, the bug is in your
thinking, and it is a hundred times cheaper to fix it here than in code.

## Worked example
**Problem:** "A shop wants to know how many of today's sales were above 10,000 shillings."

1. **Say it back:** count the sales whose amount is more than 10,000.
2. **Inputs:** a list of sale amounts, each a whole number of shillings.
3. **Output:** one whole number, the count.
4. **Examples:** `[5000, 12000, 10000, 30000]` → `2`. `[15000]` → `1`.
5. **Edge cases:** an empty list → `0`. Exactly 10,000 → *not* counted ("above" means more
   than). I wrote that down because it is the kind of thing that causes arguments later;
   in real work you would ask the shop owner.
6. **Steps:**
   1. Set `count` to 0.
   2. For each `amount` in the list:
      1. If `amount` is more than 10,000, add 1 to `count`.
   3. Give back `count`.

**Trace** with `[5000, 12000, 10000, 30000]`:

| Step | amount | count |
|---|---|---|
| start | — | 0 |
| 1st | 5000 | 0 |
| 2nd | 12000 | 1 |
| 3rd | 10000 | 1 |
| 4th | 30000 | 2 |

The trace gives 2, which matches the example. Only now would you write code.

## Predict
Trace these steps by hand with the list `[3000, 8000, 8000, 1000]`. What is given back?

1. Set `best` to the first amount.
2. For each `amount` in the list: if `amount` is more than `best`, set `best` to `amount`.
3. Give back `best`.

<details><summary>Answer</summary>

`8000`. A tie does not replace `best` because the test is "more than". If the problem
were "the *last* sale with the biggest amount", the steps would need "more than or equal".
Small words matter.
</details>

## Exercises
Write the answers in `plans.md` in your lesson folder. No code in this lesson.

1. **Total fees.** Given a list of transactions, each with an amount and a fee, give back
   the total of the fees. All six questions, and a trace.
2. **Biggest payment and who sent it.** Given a list of received payments, each with an
   amount and a sender's name, give back the biggest amount *and* the sender. What do you
   do if two senders tie? Decide, and write down why.
3. **Amount text to a number.** Given text such as `"Tsh15,000.00"`, `"TZS 15,000"` or
   `"15000"`, give back the whole number `15000`. List at least five edge cases. You will
   build this for real in Lesson 13, and again from memory a week after that, so make
   this plan good.

## Find the bug
Someone planned "count the sales that were *at least* 10,000". Trace their steps with
`[10000, 9000, 20000]` and find what is wrong.

1. Set `count` to 0.
2. For each `amount`: if `amount` is more than 10,000, add 1 to `count`.
3. Give back `count`.

## Done when
- [ ] `plans.md` has all six questions answered for each of the three exercises.
- [ ] Each plan has a written trace that matches one of its examples.
- [ ] Exercise 3 lists at least five edge cases.
- [ ] You found the bug above and wrote one sentence on how a trace exposed it.
- [ ] Committed.

## Record
```bash
python .emw/tools/emw_track.py log core.testing --type explain --assistance A1 --task "Planned three problems with inputs, outputs, edge cases and pseudocode, and traced each by hand"
```
