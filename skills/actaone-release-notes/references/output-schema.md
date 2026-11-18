# Structured output schema

Use this shape for reusable drafts. Omit no top-level section; use empty arrays when necessary.

```yaml
schema_version: 1
release: "<version or candidate>"
status: draft
generated_at: "<ISO-8601 timestamp>"
source:
  repository: "<owner/repo>"
  from: "<tag-or-sha>"
  to: "<tag-or-sha>"
  complete: false
  limitations: []

user:
  highlights: []
  improvements: []
  fixes: []

admin:
  highlights: []
  configuration: []
  operations: []
  fixes: []
  breaking_changes: []
  known_issues: []

internal:
  deployment_notes: []
  verification_required: []
  rollback_considerations: []
  security_restricted: []

needs_review: []
```

Each public/admin item uses:

```yaml
- id: "rn-001"
  title: "<short title>"
  description: "<audience-specific copy>"
  sources:
    pull_requests: [123]
    issues: [456]
    commits: ["abcdef1"]
  confidence: high
```

`confidence` is `high`, `medium`, or `low`. Sources stay available for audit and may be stripped by the later UI publication layer. A `needs_review` item must state the question, affected draft IDs, and missing or conflicting evidence.

This structure is the audit source of truth, not the strict LibreChat product
payload. For the customer update modal or admin release card, also generate the
separate files defined in [librechat-ui-payload.md](librechat-ui-payload.md).
