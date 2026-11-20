# Installing EMW in a Project

EMW is designed to live inside the repository it governs. Install the core and the entry-point instructions your agent understands.

## Option A — Copy the framework
1. Copy the `.emw/` directory into the target repository.
2. Copy root `AGENTS.md` to the target repository root.
3. Copy the relevant adapter file(s), such as `CLAUDE.md`, `GEMINI.md`, `.cursor/rules/emw.mdc`, or `.github/copilot-instructions.md`.
4. If the target already has an instruction file, do not overwrite it. Merge the EMW reference into the existing file and preserve project-specific instructions.
5. Commit the files with a message such as `chore: add EMW engineering workflow`.

## Option B — Git subtree (keeps upstream history)
From the target project repository:
```bash
git remote add emw https://github.com/Masterfeliche/ewm-principle.git
git fetch emw
git subtree add --prefix=.emw emw main --squash
```
Then copy or adapt the root agent instruction files from the EMW repository. If `.emw` already exists, inspect and merge; do not overwrite local records.

To update later:
```bash
git fetch emw
git subtree pull --prefix=.emw emw main --squash
```
Note: subtree is optional. For a small team, copying a pinned version may be simpler.

## Option C — Git submodule
```bash
git submodule add https://github.com/Masterfeliche/ewm-principle.git .emw-upstream
git submodule update --init --recursive
```
This keeps the framework as a separate repository but adds submodule management overhead. Do not put project-specific ledgers inside a shared upstream submodule; keep them in the host project's own `.emw/` directory or another project-owned path.

## First-time setup
1. Ask the agent to inspect the repository and read `AGENTS.md` and `.emw/core/`.
2. Complete `.emw/templates/project-onboarding.md`.
3. Create a project-specific skill map and copy `skill-ledger.yaml` as the initial ledger.
4. Create `delivery-ledger.md`.
5. Establish baseline proficiency with small assessments; mark unassessed skills M0 or unverified, not guessed.
6. Agree which decisions require explicit human approval.
7. Start with one real feature and evaluate whether the workflow is useful.

## Important
EMW is instructions and records, not an executable agent plugin. It works by providing the agent with repository-local operating rules. Different agents load instruction files differently; see [Using EMW with Any Agent](USING-WITH-ANY-AGENT.md).
