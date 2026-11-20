---
id: "KB-<ID>"
title: "<Descriptive knowledge title>"
status: "draft"
confidence: "low"
category: "debugging"
scope: "project-local"
summary: "<One-sentence searchable lesson>"
context: "<Where and under what conditions this applies>"
problem: "<Problem or question addressed>"
root_cause_or_principle: "<Verified cause or underlying principle>"
recommended_approach: "<Actionable recommendation>"
alternatives: []
technologies: []
versions: []
tags: []
applicability: "<Preconditions and context>"
evidence: []
limitations: []
related_entries: []
related_adrs: []
source_project: ""
created_at: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
review_trigger: ""
supersedes: []
superseded_by: ""
---

# <Knowledge title>

## Summary
A short, searchable statement of the lesson.

## Context and applicability
Where does this apply? Include relevant architecture, versions, constraints, and preconditions.

## Problem or question
What problem, decision, or recurring task does this knowledge address?

## Observation / root cause / principle
Separate direct observations from interpretation. For a bug, explain the verified root cause. For a pattern, explain why it works.

## Recommended approach
Give a safe, actionable sequence or pattern. Link to project examples rather than duplicating large code blocks.

## Alternatives and trade-offs
What else could be done? When would this recommendation not fit?

## Evidence and provenance
For every item in frontmatter `evidence`, explain how it was obtained:
- Reproduction / test / command:
- Observed result:
- Source files / commit / ADR / issue:
- Authoritative references:
- Evidence type: direct observation / reproducible test / authoritative source / reasoned guidance

## Limitations and caveats
List version constraints, failure cases, assumptions, and unverified areas.

## Related knowledge
- 

## Maintenance
- Review trigger:
- Supersedes / superseded by:

> Validate the YAML metadata against `.emw/knowledge/knowledge-entry.schema.json` when validation tooling is available. Do not label an entry verified unless its evidence supports the stated applicability.
