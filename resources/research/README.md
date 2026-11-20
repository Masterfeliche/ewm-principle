# Backend language research

Research reports on four backend ecosystems as of 20 November 2026. Each covers the language and its versions, frameworks, tooling and testing, deployment and scaling, the job market, and a five-stage path from beginner to deploying scalable systems, with a source link after each key claim.

| Report | File |
|---|---|
| PHP | [PHP ecosystem mastery path.md](PHP%20ecosystem%20mastery%20path.md) |
| .NET (C#) | [Dotnet ecosystem mastery path.md](Dotnet%20ecosystem%20mastery%20path.md) |
| Go | [Go ecosystem mastery path.md](Go%20ecosystem%20mastery%20path.md) |
| Python | [Python ecosystem mastery path.md](Python%20ecosystem%20mastery%20path.md) |

## Tanzania and East Africa project research
- [East Africa software problems for PHP projects.md](East%20Africa%20software%20problems%20for%20PHP%20projects.md) (21 Nov 2026): which project ideas hold up against local evidence, the payment, SMS and tax-receipt systems that shape them, what needs a company or licence, and a five-stage project menu for the PHP track. Not legal advice.

## Visual version
- `backend-language-field-guide.html`: all five reports on one page (four languages plus East Africa projects), with an overview, job-market charts and a side-by-side table. Open it in a browser (needs internet for fonts and the Markdown renderer).
- Hosted copy: https://claude.ai/artifact/DKbwTBWqa1CpqCamEnjXR1 (private until shared from its Share menu).

To rebuild the page after editing a report:

```bash
python resources/research/_build/build_guide.py resources/research resources/research/backend-language-field-guide.html
```

The rebuilt file has no doctype line; add `<!doctype html>` at the top for local viewing, or publish it as an artifact as is.

## Caveats
- Job figures are UK data (ITJobsWatch, six months to 20 Nov 2026). Check job boards where you plan to work.
- Stage durations are estimates; no source measures them.
- Some survey figures come from secondary summaries; each report says where.
- These are point-in-time snapshots. Versions and figures will date; re-run the research before relying on them.
