# EMW Knowledge System

The EMW Knowledge Intelligence Layer (KIL) makes useful engineering experience persistent and reusable. It is designed to improve future agent work through retrieval and evidence-backed guidance, not through automatic model-weight training.

## 1. Two knowledge bases

### Shared EMW knowledge
Location: `.emw/knowledge/`

This is curated knowledge intended to help many projects:
- Reusable engineering patterns.
- Debugging playbooks and verified root causes.
- Technology and architecture guidance.
- Security and integration lessons.
- Learning and assessment methods.
- Agent workflow guidance.
- Research notes with source and limitations.

The shared knowledge base is maintained in the EMW framework repository. Contributions require review.

### Project knowledge
Location in each consuming repository: `.project-knowledge/`

This is the durable memory of that product:
- Business rules and domain vocabulary.
- Architecture and data-model context.
- Project-specific conventions and accepted decisions.
- Provider integration details and operational notes.
- Bugs, root causes, verified fixes, and regression cases.
- Security boundaries and invariants.
- Lessons learned and rejected approaches.

Project knowledge belongs to that project. It should not be copied into the shared framework without an explicit, reviewed contribution.

## 2. What is the source of truth?

Use the records for their intended purpose:
- ADRs record why a consequential design decision was made.
- Delivery ledger records what is done, blocked, or next.
- Mastery ledger records the human's evidence-backed proficiency.
- Learning log records meaningful learning events and assistance.
- Knowledge entries preserve reusable explanations, patterns, pitfalls, and diagnostic procedures.

Link between records rather than duplicating the same content in multiple places.

## 3. How an agent retrieves knowledge

Before meaningful work, the agent should:
1. Identify the task's technologies, components, failure modes, and risk areas.
2. Read `.emw/knowledge/index.yaml` and `.project-knowledge/index.yaml` when present.
3. Search for relevant terms and synonyms in the indexes and category files.
4. Read candidate entries fully.
5. Check status, confidence, applicability, technology versions, evidence, and limitations.
6. Compare with current project ADRs and authoritative documentation.
7. Report the relevant guidance and any conflict or gap.

For high-risk work, retrieval is mandatory even when the agent has prior familiarity. An index hit is not proof. The actual entry and current implementation must be inspected.

## 4. How knowledge is captured

Capture durable discoveries, not every activity. Useful examples include:
- A non-obvious production bug and its confirmed root cause.
- A reusable database, API, or framework pattern.
- A security invariant and how to test it.
- A toolchain issue and reliable resolution.
- A rejected approach and why it failed.
- A lesson that materially improved a learning or verification workflow.

Use `.emw/templates/knowledge-entry.md` and Prompt 08. Include provenance, evidence, versions, caveats, and what remains unknown. Update the correct index.

If evidence is incomplete, mark the entry `draft` or `proposed`; do not state assumptions as verified facts.

## 5. Trust and quality controls

Every entry should identify:
- A stable ID and clear title. Shared entries in `.emw/knowledge/` use `KB-` ids (for example `KB-SEC-0001`). Project entries in `.project-knowledge/` use `PKB-` ids (for example `PKB-0001`), so the two can never be confused. `emw_check.py` rejects a `PKB-` id in the shared knowledge base.
- Status and confidence.
- Scope and category.
- Technologies and affected versions.
- Applicability and preconditions.
- Problem and recommended approach.
- Evidence and provenance.
- Alternatives, limitations, and review triggers.

Statuses:
- `draft`: incomplete; not reliable guidance.
- `proposed`: ready for review but not established.
- `verified`: reviewed with supporting evidence for the stated context.
- `deprecated`: no longer recommended.
- `superseded`: replaced by a newer entry.

Confidence:
- `low`: limited evidence or significant uncertainty.
- `medium`: useful evidence but limited coverage or context.
- `high`: strong, repeatable evidence within the stated applicability.

A high-confidence entry is not universally correct. Version, context, and limitations still matter.

## 6. Project-to-shared contribution

A project lesson may be useful to other teams, but promotion must be deliberate:
1. Explain why the insight generalizes.
2. Remove secrets, private endpoints, customer data, personal data, proprietary rules, and private code.
3. Validate accuracy and evidence.
4. Check the shared base for duplicates or conflicts.
5. Create a proposal using `.emw/templates/knowledge-contribution.md`.
6. Obtain human review and approval.
7. Add the generalized entry and update the shared index through normal Git review.

Agents may draft proposals. They must not automatically publish project knowledge to the public/shared base.

## 7. Staleness and conflicts

Technology and security guidance can age. Include versions and review triggers. If two entries conflict:
- Compare scope, versions, dates, evidence, and source quality.
- Prefer current project decisions where they intentionally differ from generic advice.
- Consult authoritative documentation for current API or security behavior.
- Mark stale entries for review, supersession, or deprecation.

Do not silently remove historical lessons; link replacements so the reason for change remains understandable.

## 8. Search technology and scaling

The first implementation uses Markdown, YAML, JSON Schema, Git, and ordinary repository search. This keeps knowledge portable and auditable across agents.

Do not add embeddings, vector databases, RAG services, or a separate knowledge server until real usage shows that text search and an index are insufficient. A later retrieval adapter can expose the same knowledge files through semantic search without changing the content contract.

## 9. Privacy and licensing

Never save credentials, tokens, private keys, personal/customer information, or private project details in shared knowledge. Avoid reproducing large portions of vendor or third-party documentation. Prefer concise original explanations and links to primary sources. Check project ownership and licensing before contributing code or examples.
