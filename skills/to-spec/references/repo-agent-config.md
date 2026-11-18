# Repo agent config

<!-- JAST: replaces the upstream hand-off to the separate `setup-matt-pocock-skills`
     skill (mattpocock/skills@885e2ca). Seed templates copied unchanged from it. -->

This skill reads per-repo configuration:

- `docs/agents/issue-tracker.md`: where issues live and how to read, create, comment on, and label them. Seeds: [GitHub](agent-config/issue-tracker-github.md), [GitLab](agent-config/issue-tracker-gitlab.md), [local markdown](agent-config/issue-tracker-local.md).
- `docs/agents/triage-labels.md`: the label strings for the five triage roles. Seed: [triage-labels.md](agent-config/triage-labels.md).

Use the configuration the repo already provides: these files, or an equivalent section in `AGENTS.md` / `CLAUDE.md`. When it is missing:

1. Infer the tracker from `git remote -v`: GitHub or GitLab remote → that seed; no remote → local markdown. Labels: the seed defaults unless the tracker already uses other names.
2. Show the user the proposed file contents and the target path. Write them only after the user confirms; they change the repository. Where `setup-matt-pocock-skills` is available, the user may run it instead.
3. Without confirmation, continue only with steps that need no tracker and report what was skipped.

The seeds also describe `/wayfinder` operations. They belong to a skill outside this collection; ignore that section.
