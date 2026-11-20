---
description: Independently review a code change using EMW's verification policy
---

Read and follow `.emw/prompts/05-code-review.md` and `.emw/prompts/07-knowledge-retrieval.md` to review: $ARGUMENTS

Inspect the complete change and relevant call sites. Report concrete findings first, ordered by severity. Review correctness, maintainability, tests, security, authorization, tenant isolation, data integrity, and regressions. Distinguish confirmed defects from questions and unverified areas. Do not treat AI-generated tests as proof.
