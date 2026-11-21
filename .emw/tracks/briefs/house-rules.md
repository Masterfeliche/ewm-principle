# House rules for every track project

These apply to every project from Stage 1 on. A project that breaks one is not finished.

1. **Bilingual.** Kiswahili and English, with Kiswahili as the default. Use the words owners use (mauzo, matumizi, madeni), and check them with a real user before you settle on them.
2. **Light.** Usable on a cheap Android phone and a slow connection. No heavy front end before Stage 3. For services with no screens, "light" means small responses and sensible timeouts.
3. **Money is exact.** Store whole shillings as integers. Record every movement. Never edit or delete a money record; add a correcting one.
4. **Phones are identity.** Store numbers in one international format (`+2557…`). A prefix only suggests the operator, because numbers can be moved between networks; let the user pick their wallet.
5. **Sandbox only.** Invented people, invented shops, simulators and mocks. No real money, no real customer data, no real submissions to TRA. Never practise on a payment provider that has no sandbox.
6. **Data protection by habit.** Collect the least data you can. Log who viewed or changed what. Support export and delete. Keep children's and patients' data out unless the project needs it.
7. **Never hold other people's money.** Record it, and let a licensed provider move it.
8. **Assume the power or network drops mid-request.** Make writes safe to repeat, and queue outbound calls.

## How to work
- Stage 0: you type everything. These house rules do not apply yet; the stage 0 brief is the whole specification.
- Stages 1 and 2: you type the code. Use `/emw-practice`; the agent gives hints one step at a time and no complete solutions before you attempt.
- Stage 3 on: plan with the agent, write the core logic yourself, and let it scaffold only what you have already written by hand once.
- Log each meaningful task in `.emw-project/task-log.yaml` and each demonstration in `skill-ledger.yaml` with its honest assistance level.

## Before going beyond a sandbox
Real payments, a real SMS sender name and real fiscal receipts need a registered business with a TIN, and some activities need a licence or a regulator's approval. Handling real people's data brings Personal Data Protection Act duties, including registration. The framework repository keeps a background report on these constraints under its own `resources/research/`; it is not copied into a consuming project, and it is not legal advice.
