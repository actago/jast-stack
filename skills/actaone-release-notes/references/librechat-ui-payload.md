# LibreChat UI payload

Use this contract when the user asks for JSON for the customer update modal,
first-login update view, admin release card, or `api/server/data/release-notes.json`.

## Product artifact

Create `release-notes.json` with this shape:

```json
{
  "release": {
    "id": "2026-08-27-r1",
    "version": "2026.08.27",
    "title": "Neues in actaOne",
    "publishedAt": "2026-08-27T12:00:00+02:00",
    "summary": "Die wichtigsten Neuerungen dieses Updates.",
    "entries": [
      {
        "type": "feature",
        "title": "Kurzer Titel",
        "description": "Konkreter Nutzen oder eine notwendige Admin-Handlung.",
        "audience": "user"
      }
    ]
  }
}
```

The authoritative schema is `releaseNotesFileSchema` in
`packages/api/src/release/notes.ts` of the LibreChat fork. Re-read it before
generating; the summary below was checked against fork `origin/main`
`f29a7aafa2dc` (2026-11-16):

- The file is exactly `{ "release": … }`; a top-level extra key fails validation.
- `release` is one object or `null`.
- `id`: 1–128 characters; stable and unique for the displayed release.
- `version`: 1–128 characters.
- `title`: 1–160 characters.
- `publishedAt`: ISO-8601 datetime with an explicit timezone offset.
- `summary`: optional, 1–4000 characters.
- `layout`: optional, only `"chapters"`.
- `documentUrl`: optional, a bundled PDF path matching
  `/assets/release-notes/<folder>/<name>.pdf`.
- `entries`: 1–100 items.
- `type`: `feature`, `improvement`, `fix`, or `security`.
- entry `title`: 1–160 characters.
- entry `description`: 1–4000 characters.
- `audience`: `user`, `admin`, or `all`. The schema defaults a missing value to
  `all`; emit it explicitly so an admin-only item never leaks to users by default.
- entry `images`: optional, 1–12 items of `{ src, alt, width, height }`; `src`
  is a bundled `.png` or `.webp` under `/assets/release-notes/<folder>/`, `alt`
  1–300 characters, `width`/`height` integers 1–8192. Use only images that exist
  or will be added in the same reviewed change, and show fictional or demo data.

Use `all` only when the same wording is useful to both audiences. Use separate
items when users need benefit-oriented copy and administrators need an action,
constraint, or rollout note. Internal-only changes stay out of this artifact.

The server returns every entry to instance administrators and only non-`admin`
entries to everyone else; if nothing remains, users see no release.

## Audience boundary

`admin` always means an administrator of one customer instance. Include only
behavior that this role can see or control inside that instance. Verify the
reachable customer-admin UI or API before assigning this audience. Platform,
fleet, cross-tenant, global analytics, deployment, environment, and internal
pricing capabilities are `internal`, even when their implementation lives in an
`admin-panel` directory or PR title. Describe instance-wide settings as applying
to "the administrator's own instance", never as global or multi-tenant control.

The file carries no traceability, confidence, draft status, review notes, or
other keys beyond the schema. Keep those in the audit artifact. Inside
`release` and its entries the schema silently strips unknown keys instead of
rejecting them, so a passing validator does not prove that nothing was lost.

## Audit artifact

Create `release-notes.audit.json` beside the product artifact. It may follow the
structured draft in [output-schema.md](output-schema.md), but it must map every
product entry to its PRs, issues, commits, evidence, confidence, and unresolved
questions. Record whether `publishedAt` is confirmed or a draft placeholder.

## Validation and handoff

Validate with the same schema the product uses:

```bash
node scripts/validate-release-notes.mjs <path-to-release-notes.json>
```

Run this command from a LibreChat checkout containing the validator. The
script loads `releaseNotesFileSchema` through `require('@librechat/api')`, so
the workspace package must be installed and resolvable in that checkout. A
successful parse is necessary but does not approve the wording or publication.
If the validator is unavailable or fails, label the artifact `not validated`
and return the error without substituting a second schema.

Return both artifact locations, the validated/not-validated result, the source
range, and the unresolved review count. Keep the product file as a draft until
the user explicitly authorizes the exact repository write or publication step.

## GitHub PR handoff

Use this only when the user explicitly requests a PR. A request to draft JSON
does not authorize a GitHub write.

Before final confirmation, present:

- repository and base branch: `actago/LibreChat:main`;
- the exact source range and release ID/version;
- the complete product JSON or its reviewable artifact location;
- the SHA-256 of `release-notes.json`;
- validator result and unresolved review count;
- the intended product path `api/server/data/release-notes.json`, plus every
  bundled asset path under `client/public/assets/release-notes/` if the release
  uses `images` or `documentUrl`.

Wait for confirmation of those exact parameters. After confirmation:

1. Verify the approved JSON hash (and asset hashes, if any) is unchanged.
2. Fetch the current `origin/main` and create an isolated branch named
   `agent/release-notes-<release-id>` from it.
3. Require `scripts/validate-release-notes.mjs` to exist on that base. If the
   component or validator is not yet on `main`, stop and report that prerequisite.
4. Replace only the confirmed paths, run the product validator, and verify the
   diff contains no other path.
5. Commit with the Git identity the repository or user designates for agent
   work, push the branch, and open a PR against `main`. Put source range,
   validation result, JSON hash, and unresolved review count in the PR body.
6. Return the PR URL and head SHA. Leave the PR unmerged.

If `main` moves before the push, rebuild the isolated branch from the new head
and revalidate. Any content change, conflict resolution that changes the JSON,
additional file, new target branch, or changed release parameters invalidates
the confirmation and requires a new review.
