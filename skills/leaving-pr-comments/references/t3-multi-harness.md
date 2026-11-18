# tstack runtime adaptation

<!-- JAST: from ~/.agents/tstack/T3-MULTI-HARNESS.md (2026-10-26); personal install
     scope and account names generalized, see references/sources.md. -->

Applies to the nine tstack skills of the JAST stack (Windows and POSIX).
Use these integration rules with each skill's workflow. Current user instructions,
repository rules, and harness approval requirements remain authoritative.
Installing a skill does not invoke it or authorize a PR, merge, or message.

## Discover the runtime

In T3 Code, prefer its app-owned tools, including harness-normalized names such
as `mcp__t3_code__delegate_task`. Read `orchestrator_capabilities` for live,
enabled provider instances, exact model IDs, model options, and inherited options.
Do not cache model availability or infer it from the native subagent catalog.
If the tools are initially absent, make one direct capability call. If unavailable
and `T3_ACP_MCP_NODE` exists, use the supported `acp-mcp-call` transport. On Windows
invoke the executable with PowerShell's `&` operator and pass the optional
`T3_ACP_MCP_ENTRYPOINT` as a separate argument; set `ELECTRON_RUN_AS_NODE=1` for
that process and restore its previous value afterward. Keep JSON as a single
argument. If no T3 route exists, use only native tools that support the required
model and settings. Report a missing capability instead of inventing an ID.

## Delegation and model selection

For cross-provider work, T3-owned child work, separate-checkout child work, or
requested/inherited model options, use `delegate_task`. Native same-provider
subagents are suitable only when they support the selected model and no model
options are requested or inherited. Merely installing or adapting these skills
does not request a review or delegation.

Resolve Sol dynamically from the enabled OpenAI catalog. For council, distinct
account profiles are not distinct model providers: two Claude account profiles
both count as Anthropic. OpenCode is a harness and can expose several model
providers; establish the model's actual provider before counting it as a seat.
Use the skill's requested model families and effort. If a requested council
member or a third distinct model provider is unavailable, report the limitation
rather than silently substituting or counting two Claude accounts twice.

Pass model settings in `target.options` using that model's advertised option IDs
and values. Preserve inherited settings only for the same instance and model.
Verify returned provider, model, and options; report unsupported settings.
Do not enable fast mode, premium service tiers, or higher effort unless requested
by the user, inherited, or required by the invoked workflow.

Each delegated review round is a fresh `delegate_task` with the original brief,
scope, base SHA, checks, prior findings, responses, and unresolved objections.
Retain its `taskId` and use a distinct `clientRequestId` per round, stable on
retries. Use `mode: "async"`; completion wakes the parent. Do not duplicate
active work or poll in a loop. `childThreadId` is storage, not a follow-up target.
Child reviewers do not watch PRs or launch reviewers of their own.

For a child needing its own checkout use `isolation: "worktree"`; it starts from
the parent's local commit, without uncommitted edits. Review uncommitted work in
the shared checkout, read-only. Ordinary `t3_thread_launch` / `create_threads`
require an explicit request for a separate top-level conversation; they are not
subagent APIs. For explicitly requested new threads choose `workspaceStrategy`
in the launch call so the app binding matches the checkout.

## Pull requests and monitoring

Immediately register each PR created or worked on with `link_pull_request` using
its full URL, including every worked-on stack layer. Before final handoff use
`list_thread_pull_requests` and link missing PRs from this task. Report failures.

The owning parent uses `watch_pull_request`, then ends its turn so T3 can wake it.
Unwatch before handoff or asking the user. A wake is not merge approval. Preserve
the invoked skill's merge gate: only an explicit full-send/merge request grants
merging; full-stop leaves the PR open and unmerged. Follow the real base branch
for stacked PRs. Comments on others' behalf still require task authorization;
`leaving-pr-comments` supplies formatting, not permission to post.

Outside T3, run the bundled watcher with an available Python 3 interpreter and
an authenticated `gh` CLI. PowerShell:
`python "<absolute-skill-path>/scripts/pr-wait" <PR> --repo owner/name`; POSIX
shells can run the script directly. Only `babysit-pr` bundles `pr-wait`.
The local script supports Windows locks as well as POSIX locks. Prefer T3's
watcher whenever available, and never run both watchers for one PR.

## Browser and questions

In T3 prefer `preview_status`, then `preview_open` if needed, followed by its
snapshot and interaction tools. Read a human-owned tab without taking control.
Use another browser only when the T3 tools are unavailable, an explicitly chosen
workflow requires it, or the runtime's documented failure threshold is met.

Use the question tool actually available in the current harness and mode;
`request_user_input` may be restricted to Plan mode. Prefer an available async
question tool for missing information while independent work continues. Pending
questions and timeouts are not approval. If a required answer cannot be obtained,
leave the PR open and unmerged and state the concrete blocker.
