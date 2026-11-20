---
name: EMW Knowledge Intelligence
description: Use before meaningful work to retrieve relevant shared and project knowledge, or after a verified discovery to capture lessons with provenance, status, confidence, limitations, and safe sharing rules.
---

# EMW Knowledge Intelligence

Follow `.emw/core/knowledge-intelligence.md` and the matching prompt files.

## Retrieval
1. Identify task technologies, components, risk and relevant terms.
2. Inspect `.emw/knowledge/index.yaml` and `.project-knowledge/index.yaml` where present.
3. Search and read relevant candidate entries.
4. Check scope, status, confidence, evidence, versions, applicability, and limitations.
5. Compare with current project decisions and authoritative current documentation.
6. Briefly report what was useful, conflicting, stale, or missing.

## Capture
When a durable discovery is verified:
1. Follow `.emw/prompts/08-knowledge-capture.md`.
2. Create a project-local entry by default.
3. Record reproducible steps, observed results, commits, tests, authoritative sources, and caveats.
4. Update the project index.
5. Use draft/proposed status when evidence is incomplete.

## Shared contributions
Never automatically copy project knowledge to `.emw/knowledge/`. Follow `.emw/prompts/10-shared-knowledge-contribution.md`, sanitize proprietary details, and obtain explicit human approval.

## Safety
Never store credentials, secrets, customer data, unnecessary personal data, private endpoints, or proprietary source code in the shared knowledge base. Never present a draft entry as verified guidance.
