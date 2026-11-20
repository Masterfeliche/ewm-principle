---
id: "KB-AGT-0001"
title: "Report checks not run as plainly as checks that passed"
status: "proposed"
confidence: "medium"
category: "agent-guidance"
scope: "shared-framework"
summary: "An agent's completion report lists the exact commands it ran with their observed results, and separately lists the checks it did not run and why."
context: "Any AI-assisted change where a human will decide to merge or deploy based on the agent's report."
problem: "Reports say 'tests pass' or 'should work' when no test was run, and the human merges on that basis."
root_cause_or_principle: "Readers cannot tell a verified claim from an expected one unless the report separates them; agents tend to summarise intent as outcome."
recommended_approach: "Use a fixed report shape: Ran (command, result), Not run (check, reason), Risks. Quote the command exactly. Never write passed for a check whose output was not observed in this session."
alternatives:
  - "Attach the raw command output instead of a summary"
technologies: ["AI coding agents"]
versions: []
tags: ["verification", "reporting", "agents", "honesty"]
applicability: "Every EMW completion report; see verification-policy.md."
evidence:
  - type: "reasoned-guidance"
    description: "Derived from EMW verification-policy.md 'Never fabricate' and completion report rules"
limitations:
  - "Reasoned guidance only; it stays proposed until a project records observed cases where this format caught an unrun check."
  - "A listed command can still have been run against the wrong branch or environment; name it."
related_entries: []
related_adrs: []
source_project: ""
created_at: "2026-11-20"
last_reviewed: "2026-11-20"
review_trigger: "First project evidence of this format catching, or failing to catch, a false claim."
supersedes: []
superseded_by: ""
---

# Report checks not run as plainly as checks that passed

## Summary
Ran / Not run / Risks, every time.

## Recommended approach
```text
Ran
- pytest tests/invoices -q        -> 42 passed
- ruff check .                    -> 0 issues
Not run
- integration tests (needs staging database)
- manual check of the PDF layout
Risks
- tenant filter on the export job is untested
```

## Evidence and provenance
Reasoned guidance from `.emw/core/verification-policy.md`. This entry deliberately stays `proposed`: `emw_check` refuses `verified` when the only evidence is reasoned guidance.

## Limitations and caveats
See frontmatter.
