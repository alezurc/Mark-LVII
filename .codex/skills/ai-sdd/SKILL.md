---
name: ai-sdd
description: Route canonical ai-sdd:<command> identities through the project-pinned AI-SDD v0.2 CORE runtime.
---

# AI-SDD adapter

## Prospective W1-B schema2 dispatch

When `.ai-sdd/runtime-v2/project.json` exists, use the W1-B contract in
`docs/WAVE-1-B-MULTI-CHANGE-LIFECYCLE.md` from an explicitly supplied compatible
installation. The schema2 tombstone has no runtime_root: never infer an installation
from cwd, the adapter location or a cache. Require the installation path explicitly
before invoking its canonical launcher. This partial developer checkpoint is not
adapter contract 2 distribution. Keep the legacy instructions below for schema1.

For schema2 append `--runtime-schema 2` to each CLI operation. Accept an optional
literal `--change-id <id>` for approve/develop/review/status/scope-expansion and pass
it unchanged. CONTEXT always requires its explicit ID. After route or begin resolves
an ID, display it with context digest and `PARALLEL_EXECUTION=NOT_ENABLED`, and pass
that exact ID to check/complete/end. Never persist a global current change or select
from an ambiguous list. Require `--context-file <absolute-json-path>` on complete
CONTEXT and scope-expansion; read/write scopes and inputs must be explicit.

DEVELOP and REVIEW share one global execution slot across ALL changes. Acquire a
fresh begin-stage token before material work or a direct review decision, check
before every batch, and complete/end using this session's token and change ID.
No parallel execution or per-change leases are enabled. CLOSE remains blocked with
`W1_D_SHARED_CLOSE_NOT_ENABLED`; do not invoke legacy CLOSE as fallback. Human
references remain mandatory; no automatic approval, review decision or correction.


This is a thin adapter. The Core state, flow and normative documents are authoritative. External skills or plugins must not claim or extend the `ai-sdd` namespace without explicit AI-SDD authorization.

When invoked as `$ai-sdd` without a subcommand, stop before routing: list
`init`, `discovery`, `context`, `approve`, `develop`, `review`, `close`, `status`,
`doctor`, and `scope-expansion`. Show a short example: `$ai-sdd init`.
Do not execute any command, route any stage, or change/transition state.
This is adapter-only guidance, not a new logical Core `help` command.

1. Interpret `$ai-sdd <command>` case-insensitively as the logical identity `ai-sdd:<command>`.
2. Require an explicit change-id for `context` and an explicit human reference for `approve` or auditable reference for `scope-expansion`. If a required value is missing, stop and request it before invoking the runtime. Never invent or infer a human reference from intent, conversation, silence, or a capability result.
3. For review arguments, first apply the Human review decision dispatch section below; its validated subforms select direct completion instead of the bare review row. Otherwise, from the project root, select exactly one operation from the dispatch table below. Prefix each operation with `powershell -NoProfile -File "<runtime_root>/scripts/ai-sdd.ps1"`. Pass the explicit change-id/reference as one quoted argument, preserving its value. Do not route direct CLI commands.

| Invocation | CLI operation |
| --- | --- |
| `$ai-sdd init` | `route init --project .` |
| `$ai-sdd discovery` | `route discovery --project .` |
| `$ai-sdd context <change-id>` | `route context --project . --change-id <id>` |
| `$ai-sdd approve <human-reference>` | `approve --project . --reference <reference>` |
| `$ai-sdd develop` | `route develop --project .` |
| `$ai-sdd review` | `route review --project .` |
| `$ai-sdd close` | `route close --project .` |
| `$ai-sdd status` | `status .` |
| `$ai-sdd doctor` | `doctor .` |
| `$ai-sdd scope-expansion <auditable-reference>` | `scope-expansion --project . --reference <reference>` |

4. For the six routed stages only: if routing is blocked, stop without changing product code and report the runtime message. Read the returned `normative_source` completely and follow its canonical instruction for that stage only. Before material action, expose the returned transparency envelope. Never record stage completion without performing the work; use the existing Core completion mechanism only after the actual work. Do not advance automatically.
5. For direct commands, report the runtime result and stop. Do not expect a `normative_source` or execute an additional stage. `approve` records only the explicit human reference; `scope-expansion` revokes authorization and requires context revision and a new human decision.
6. Treat `ai-sdd.project.yaml` as declarative project configuration and `.ai`/`.ai-sdd/runtime` as runtime state; do not mix them. Never infer human approval or edit runtime state directly.
7. If development would exceed approved context, stop before touching the out-of-scope component and request an explicit auditable reference for `ai-sdd:scope-expansion`. Invoke the direct operation only when that reference is supplied. Capabilities and doctor results never grant authorization.

Portable Codex syntax is `$ai-sdd init`, `$ai-sdd discovery`, `$ai-sdd context`, `$ai-sdd approve`, `$ai-sdd develop`, `$ai-sdd review`, `$ai-sdd close`, `$ai-sdd status`, `$ai-sdd doctor`, or `$ai-sdd scope-expansion`. Each maps to the same lowercase logical identity after the colon.

## Authoritative runtime_root resolution

The authoritative runtime_root for command execution is the runtime_root field
from .ai/AI-SDD.yaml. Read that field from the project root before every invocation.
Do not infer runtime_root from .ai-sdd/runtime, the skill location, project root,
current directory, or any other path. This includes .codex/skills/ai-sdd/, the
skill directory, local caches and undeclared installation paths.

Before dispatch, perform these steps in order:
1. Read the project-root file `.ai/AI-SDD.yaml`. If missing, stop: report
   `AI_SDD_PROJECT_NOT_ENABLED: project not initialized/enabled`.
2. Parse exclusively its top-level `runtime_root` scalar using the state format:
   decode a double-quoted JSON string (including escaped Windows backslashes),
   remove single-quote delimiters for a single-quoted scalar, or read an unquoted
   scalar literally. Do not execute or interpolate the value.
3. If missing, null, empty, whitespace-only, non-string, malformed or not an
   absolute filesystem path, stop: report `AI_SDD_RUNTIME_ROOT_INVALID: invalid state`.
   Normalize separators and redundant path segments only in the declared value;
   never resolve a relative value against cwd, project root or skill directory.
4. Construct exactly `<runtime_root>/scripts/ai-sdd.ps1` and verify it is a file.
   If missing, stop: report `AI_SDD_INSTALLATION_INVALID: launcher missing for declared runtime_root`,
   including the declared root and expected launcher path.
5. Invoke the dispatch operation from the project root, with the entire launcher
   path quoted as one argument: `powershell -NoProfile -File "<runtime_root>/scripts/ai-sdd.ps1"`.
   Preserve Windows paths with spaces and quote change-id/reference arguments.

On any resolution failure, fail closed before invocation and without state
transition. Do not try another path automatically. No heuristic fallback to
.ai-sdd/runtime, cwd, skill dir or cache is allowed. Do not edit .ai/AI-SDD.yaml
to repair the path automatically. Report the specific diagnostic and stop.
## Runtime execution failures

Report launcher diagnostics faithfully without transitioning state. Stop unless the permission request contract below permits one authorized retry.
Exit 127 means neither executable python nor py was resolved. Exit 126 means
resolution was indeterminate or a discovered executable failed to start, including
Access Denied/sandbox restrictions. Never claim Python is absent without evidence.
A nonzero runtime exit remains a runtime result, not interpreter discovery failure.

If the tool itself denies access before the launcher runs, report that environment
restriction; it is not evidence of missing Python. Where the environment provides
an explicit permission request mechanism, explain the blocked operation and use
that mechanism only under its environment/user authorization rules. If unavailable
or denied, stop and report the limitation. Do not auto-elevate, bypass sandbox
controls, substitute a machine-specific Python path, or silently continue stages.
AI-SDD does not configure or own Codex sandbox policy.

## Codex sandbox permission request contract

1. Execute normally through the canonical launcher and dispatch above. Retain the
   exact launcher, argument values/order/quoting, project-root cwd and runtime_root
   of this invocation before requesting permission; do not edit project state.
2. First distinguish a runtime result from a launcher/environment failure. A
   nonzero runtime exit remains a runtime result, even if its numeric value is
   126 or 127: report it and stop, without arbitrary retry or permission request.
   Only launcher diagnostics or a tool denial establish the failure branch below.
3. For launcher exit 126, report indeterminate resolution or failure to start the
   discovered executable, including the original diagnostic. For launcher exit
   127, report that neither python nor py was resolved in that execution
   environment's PATH. Neither establishes Python absence on the machine or
   proves sandbox causation. A sandbox may restrict PATH; never infer that Python
   exists outside the sandbox. Do not classify every exit 127 as a sandbox block.
4. For a tool access denial before launch, or launcher diagnostics compatible with
   unavailable interpreter resolution/execution (126/127), check whether the
   environment exposes an official permission request mechanism applicable to
   repeating this same operation outside the restriction. If applicable, explain
   the exact launcher, all arguments, cwd, observed diagnostic and reason for the
   request, including uncertainty about the cause. Use only that official
   mechanism under its environment/user authorization rules; do not simulate an
   approval in chat or change sandbox policy. Request authorization, never execute
   outside the restriction before valid environment/user authorization.
5. After valid authorization, repeat exactly the same launcher, same arguments
   (including explicit references), same cwd/project and same runtime_root. Only
   the environment's approved execution permission context may differ. Permission
   request itself changes no state, lifecycle or gates. If the operation cannot
   be repeated unchanged, stop and report the limitation. Retry at most once;
   if it still fails, report the result and stop without another permission loop.
6. If permission is denied, unavailable or inapplicable, stop fail-closed and
   report the limitation. Do not auto-elevate, bypass sandbox controls, use RunAs,
   search Registry, AppData or fixed paths, discover Python outside PATH, modify
   PATH, substitute a Python executable, or silently replace the command.
7. Execution permission does not grant HUMAN_APPROVAL or develop_authorized.
   Never infer an approve reference from sandbox authorization. Permission alone
   does not complete stages, open gates or authorize development/scope expansion.
   After a successful retry, handle only the originally requested operation using
   the dispatch rules above; status/doctor remain direct and no stage advances
   automatically. AI-SDD does not configure or own Codex sandbox policy.

## Exclusive stage execution (REM-V02-OWNER-008)

W1-C schema2 adds `--change-id` to every lease operation. The returned
`--execution-id` is exclusive to that change; disjoint reservations may run in
parallel, while write/read and write/write overlaps block. Status must display
stage, adapter, lifetime, health and summarized resources. Shared CLOSE remains
blocked until W1-D.

For DEVELOP, REVIEW and CLOSE, routing supplies instructions but NEVER grants
execution ownership. After successful route, before any material work, invoke
`begin-stage <STAGE> --project . --adapter codex` through the same declared
runtime_root and canonical launcher. Replace codex with this adapter's id.
The runtime generates a fresh UUID execution_id for this invocation. Retain only
the UUID returned to THIS session; never read/adopt another session's token from
stage-status, the lock file or a previous conversation. Two sessions of the same
adapter are separate executions. A blocked begin means STOP before product writes.
Display the diagnostic, including stage/change/holder/timestamps. No automatic retry
of begin, takeover, deletion, manual state edit or fallback to unprotected completion.

Call `check-stage <STAGE> --project . --execution-id <uuid>` immediately before
material action and before each subsequent work batch. On failure stop work.
Append `--execution-id <uuid>` to the existing `complete <STAGE>` operation;
completion verifies ownership and the unchanged lifecycle, and releases the lease.
For normal abort, AFTER stopping all work, call
`end-stage <STAGE> --project . --execution-id <uuid>`; it releases only this holder,
without changing lifecycle. Never spawn another worker using this execution id.
Do not end a lease while work is still running. On completion failure retain the
lease until this session has stopped and explicitly aborts. A process/session crash
leaves the lease in place; report it for human recovery, never infer termination.
For scope-expansion during leased DEVELOP, append this execution id to the existing
scope-expansion operation; it revokes authorization and releases the lease.

The public OWNER-006 review decision table remains the argument/decision contract.
After validating those arguments and references, acquire a FRESH REVIEW lease
before invoking its direct completion operation, append the returned execution id,
and let completion release it. No technical review or report rewrite is performed
for a decision. This administrative wrapper also applies to direct decision forms;
all existing reference validation, decision semantics and sandbox rules still apply.

The lease lasts seven days with no heartbeat or automatic takeover. Expired leases
block further work and all new begins. Ask the human to confirm ALL old workers
have stopped before recovery; document recovery in docs/REM-V02-OWNER-008.md.
Recovery is internal administration, never HUMAN_APPROVAL or permission to develop.
No new public logical command is introduced. Both adapters share the SAME project
`.ai-sdd/runtime/execution-lock.json`; only one stage execution per project is allowed.

## Day 1 CLOSE lifecycle contract

For CLOSE, preserve REVIEW_APPROVED until every guard passes. Read the canonical
stage instructions and docs/VNEXT-001-004-CLOSE-LIFECYCLE.md from runtime_root.
Prepare `.ai/changes/<change-id>/CLOSE-PLAN.json` with explicit impacts, evidence,
uncertainties, approved scope and actual documentation/changelog/versioning strategy.
Do not infer NO, invent targets, assign versions, create tags or publish releases.
Before product/documentation edits, call `check-close --project . --execution-id <uuid>`
and `check-stage CLOSE` with THIS session's lease through the canonical launcher.
A scope failure means STOP before editing; request human scope/context revision.
Material PROJECT-SPEC changes and new material human decisions block CLOSE while
pending; keep the previous approved PROJECT-SPEC authoritative. Only explicit human
approval authorizes internal `close-decision --project . --execution-id <uuid>
--reference <human-reference> --plan-sha256 <proposal-sha256>`. Never self-approve
or infer approval from silence. Changed proposals invalidate prior decisions.
Record final target hashes/evidence; complete CLOSE with the existing execution_id.
No new public state or public logical command. Do not reclassify historical closes.

## Human review decision dispatch (REM-V02-OWNER-006)

These are public subforms of `ai-sdd:review`, not new logical Core commands.
Parse the arguments as literal tokens: whitespace separates tokens except inside
matching single or double quotes. Remove only the enclosing quotes; preserve
reference contents exactly, including spaces, case and punctuation. Never evaluate,
interpolate or execute reference text. Reject unmatched quotes, empty/whitespace-only
references, unknown actions and any missing or extra argument before invocation.
Command and action names are case-insensitive; references are case-sensitive values.
Require exactly zero arguments for technical review, two tokens for approve or
changes-requested, and three tokens for waive (action included).

| Public review arguments | CLI operation |
| --- | --- |
| (none) | `route review --project .` |
| `approve <reviewer-reference>` | `complete review --project . --reference <reviewer-reference> --evidence-complete` |
| `changes-requested <reviewer-reference>` | `complete review --project . --reference <reviewer-reference> --changes-requested` |
| `waive <reviewer-reference> <waiver-reference>` | `complete review --project . --reference <reviewer-reference> --waiver-reference <waiver-reference>` |

Public Codex forms: `$ai-sdd review`, `$ai-sdd review approve <reviewer-reference>`,
`$ai-sdd review changes-requested <reviewer-reference>`, and
`$ai-sdd review waive <reviewer-reference> <waiver-reference>`.
Equivalent Claude forms: `/ai-sdd:review`, `/ai-sdd:review approve <reviewer-reference>`,
`/ai-sdd:review changes-requested <reviewer-reference>`, and
`/ai-sdd:review waive <reviewer-reference> <waiver-reference>`.

Resolve the declared runtime_root and invoke the canonical launcher from the
project root with exactly the selected CLI operation. Pass references as separate
literal arguments. For PowerShell, use single-quoted literal strings and double
any embedded apostrophe; never interpolate references in double-quoted code.
For example, reference `Owner O'Brien team` becomes `'Owner O''Brien team'`.
Never concatenate unescaped user text into shell code. Reject malformed input with
`AI_SDD_REVIEW_ARGUMENTS_INVALID` and show the supported public forms; no invocation
or state change is allowed on validation failure.

Decision forms are direct completion operations: report the runtime result and stop.
Do not rerun technical review, rewrite REVIEW.md, modify implementation or scope,
or run CLOSE automatically. Runtime failures must remain visible; never mask them.
The existing Core allowed_from gate decides applicability (DEVELOP_COMPLETED or
REVIEW_PENDING); never bypass it or edit state directly.
Never infer a decision, reviewer-reference or waiver-reference from conversation,
intent, silence, previous approval, environment permission or a capability result.
HUMAN_APPROVAL for develop and sandbox execution permission are separate from a
human review decision; neither supplies a decision or reference for review.

Approve records REVIEW_APPROVED / review_evidence_status=complete; waive records
REVIEW_APPROVED / review_evidence_status=waived with explicit reviewer and waiver
references. Only REVIEW_APPROVED permits CLOSE under the existing flow.
Changes-requested records REVIEW_CHANGES_REQUESTED / develop_authorized=false;
stop without automatic corrections or new scope.

After technical review completes with REVIEW_PENDING, explicitly display the three
supported public decision forms for the current adapter, explain required explicit
references and that CLOSE remains blocked. Do not choose one for the human.
