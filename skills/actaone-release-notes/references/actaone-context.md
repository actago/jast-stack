# actaOne release context

Replaces the former dependency on the Hermes skill `actaone-core`. Read the
authoritative sources below in the actaOne monorepo (`actago/actaOne`) or the
LibreChat fork (`actago/LibreChat`) at the commit you are documenting. They
win over this summary.

## What a release is

- An actaOne release is one immutable image tag of the form
  `YYYYmmddHHMM-lc-<sha>-rag-<sha>-pii-<sha>`. The three short SHAs are the
  source states of `actago/LibreChat`, `actago/KB_RAG` and `actago/presidio`.
  Source: `docs/RELEASE_PROCESS.md`, section "Grundprinzip".
- For a tag-to-tag range, build one range per component: previous `lc` SHA to
  new `lc` SHA in the fork, and likewise for `rag` and `pii`. Add monorepo
  changes (deploy scripts, templates, Vault defaults) only when they change
  behavior that a user or instance administrator can see.
- "Last stable" is the release registry stamped through the Ops dashboard,
  not `deploy/RELEASE` and not the staging candidate. Source: `CLAUDE.md`,
  "Release-Fluss", and `docs/RELEASE_PROCESS.md`, "Stable-Gating" and
  "Release-Pins". A tag that is only a staging candidate is not shipped.
- New customers and existing customers can run different releases (release
  pins, "Pin halten", canary and fleet promotes). Ask which audience and which
  fleet state the notes describe before writing "now available".

## Where the shipped notes live

- Product file: `api/server/data/release-notes.json` in the LibreChat fork,
  read by `packages/api/src/release/notes.ts` and served by
  `api/server/routes/release-notes.js`. Contract: [librechat-ui-payload.md](librechat-ui-payload.md).
- Images and an optional PDF are bundled under
  `client/public/assets/release-notes/<folder>/` in the fork.

## Further context on demand

- Architecture and trust boundaries: `docs/ARCHITECTURE.md`.
- Release and promote flow, release pins, hotfix releases: `docs/RELEASE_PROCESS.md`.
- Release operations in this collection: the separate JAST skill `cut-release`.
  Writing notes never triggers a release, promote or deploy.
