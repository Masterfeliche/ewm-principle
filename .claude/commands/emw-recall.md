---
description: "Do a scheduled recall check: rebuild something from memory, no notes, no AI"
---

Read and follow `.emw/prompts/13-recall.md` for this skill or piece of work: $ARGUMENTS

If no skill was named, run `python .emw/tools/emw_recall.py due` first and offer the checks it lists.

State the task from the outside only: what it must do, its inputs and outputs, one edge case, and how the developer will know it works. Give no code, no skeleton and no sight of their earlier implementation until they say their attempt is finished. One conceptual hint makes the check A1; anything more ends it, and it becomes a practice session (Prompt 11) instead. Afterwards compare their rebuild with the original, let them name the differences, record the result with `emw_recall.py done`, and lower the level in the ledger if the rebuild needed the old code.
