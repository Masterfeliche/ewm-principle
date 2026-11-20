---
id: "KB-DBG-0001"
title: "Find the commit that introduced a regression with git bisect"
status: "proposed"
confidence: "high"
category: "debugging"
scope: "shared-framework"
summary: "When something used to work, write a pass/fail check first, then let git bisect binary-search the history for the first bad commit."
context: "A behaviour worked at a known commit or release and fails now, and the cause is not obvious from reading the diff."
problem: "Hours spent guessing at a regression across dozens of commits."
root_cause_or_principle: "Binary search finds the first bad commit among N commits in about log2(N) steps, and a scripted check removes judgement from each step."
recommended_approach: "Write a script that exits 0 when the behaviour is correct and non-zero when broken, mark one good and one bad commit, run git bisect run with the script, then read the single commit it names and keep the script as a regression test."
alternatives:
  - "Read the diff between good and bad when it is small"
  - "Add logging and compare runs when the bug is not tied to a code change (data or environment)"
technologies: ["Git"]
versions: []
tags: ["regression", "git", "bisect", "debugging"]
applicability: "Regressions caused by a code change, with a history where each commit builds."
evidence:
  - type: "authoritative-source"
    description: "Git documentation for git bisect, including git bisect run and exit code 125 to skip untestable commits"
    uri: "https://git-scm.com/docs/git-bisect"
limitations:
  - "Does not help when the cause is data, configuration or environment rather than code."
  - "Commits that do not build must be skipped (exit 125), which can widen the result to a range."
  - "Flaky checks give wrong answers; make the check deterministic first."
related_entries: []
related_adrs: []
source_project: ""
created_at: "2026-11-20"
last_reviewed: "2026-11-20"
review_trigger: "Changes to git bisect behaviour in a new Git release."
supersedes: []
superseded_by: ""
---

# Find the commit that introduced a regression with git bisect

## Summary
Write the failing check first, then search history automatically.

## Context and applicability
"It worked last week." Use when the cause is a code change and the diff is too large to read.

## Problem or question
Which of these commits broke it?

## Observation / root cause / principle
Binary search over history. The Git documentation describes `git bisect run <cmd>`: exit 0 = good, 1–127 except 125 = bad, 125 = skip.

## Recommended approach
```bash
git bisect start
git bisect bad HEAD
git bisect good v1.4.0
git bisect run ./check.sh   # exits 0 when correct
git bisect reset
```
Keep `check.sh` (or turn it into a test) so the regression stays caught.

## Mastery note
A good learning exercise for Mode 1: the developer writes the check and predicts the culprit before running bisect.

## Evidence and provenance
- Git documentation, git-bisect (authoritative source).

## Limitations and caveats
See frontmatter.

## Maintenance
- Status is `proposed`: a human reviewer should confirm the source and change it to `verified`.
