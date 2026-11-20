# Contributing to EMW

Thank you for improving Engineering Mastery Workflow.

## Contribution principles
- Keep the core framework agent- and technology-neutral.
- Prefer small, focused changes with clear rationale.
- Keep reusable prompts as separate files in `.emw/prompts/`.
- Update prompt routing when adding or changing a prompt.
- Preserve the separation between shared framework knowledge and project-local records.
- Never include secrets, customer data, personal information, or proprietary project details.
- Do not claim empirical effectiveness without evidence.

## Adding a knowledge entry
1. Read `.emw/core/knowledge-intelligence.md` and [the knowledge-system guide](docs/KNOWLEDGE-SYSTEM.md).
2. Confirm that the lesson is reusable beyond one project.
3. Generalize and sanitize the material.
4. Use `.emw/templates/knowledge-entry.md`.
5. Include evidence, source provenance, technologies/versions, applicability, limitations, status, and confidence.
6. Add the entry to the appropriate category under `.emw/knowledge/`.
7. Update `.emw/knowledge/index.yaml`.
8. Validate the metadata against `.emw/knowledge/knowledge-entry.schema.json` where tooling is available.
9. Request human review. Do not self-label a new assertion as verified without adequate evidence.

## Adding or changing a prompt
1. Create a standalone file under `.emw/prompts/`.
2. Give it one clear purpose and a specific trigger.
3. Include required inputs, operating steps, constraints, and expected output.
4. Add it to `.emw/prompts/README.md` routing table.
5. Update `AGENTS.md` and applicable adapter files so compatible agents can select it automatically.
6. Ensure the prompt does not contradict the core policies.

## Updating the core
When changing lifecycle, mastery levels, collaboration modes, or safety rules:
- Update all directly affected documentation and templates.
- Preserve compatibility where practical.
- Explain migration implications for existing project records.
- Do not overwrite project-owned files or ledgers.

## Review checklist
- [ ] Purpose and scope are clear.
- [ ] No invented research or unsupported claims.
- [ ] Prompts are separately reusable and routed.
- [ ] Shared and project knowledge remain separated.
- [ ] Evidence, provenance, privacy, and licensing are addressed.
- [ ] README and guides reflect the actual repository structure.
- [ ] Agent instructions remain concise and point to canonical core files.
