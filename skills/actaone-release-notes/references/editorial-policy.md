# Editorial policy

## User notes

- Describe the benefit or resolved problem in clear German by default.
- Use short headings and one or two sentences per item.
- Avoid component names, implementation details, ticket numbers, commit vocabulary, and operational instructions.
- Do not oversell. Prefer “verbessert”, “vereinfacht”, or a concrete effect over marketing superlatives.
- Group under `highlights`, `improvements`, and `fixes`.

Example:

```yaml
- title: "Übersichtlichere Suchergebnisse"
  description: "Suchtreffer lassen sich schneller erfassen und relevanter Inhalt ist deutlicher hervorgehoben."
```

## Administrator notes

- State the operational effect precisely.
- Include required actions, configuration changes, migration behavior, compatibility, rollout constraints, and known issues.
- Separate `configuration`, `operations`, `fixes`, `breaking_changes`, and `known_issues`.
- Use imperative wording only when an administrator must act.

## Internal operations notes

- Include rollout risk, verification checks, observability signals, rollback considerations, flags, and dependency changes.
- Keep source PRs, issues, and commits here rather than in public copy.
- Mark assumptions and missing evidence explicitly.

## Quality checks

- Use one concept per item.
- Merge duplicates across commits and PRs.
- Keep tense and terminology consistent.
- Avoid “diverse Verbesserungen”, “Bugfixes”, or other content-free phrases.
- Do not promise performance, availability, or security outcomes unless measured or proven.
