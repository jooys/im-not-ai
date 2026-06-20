# Stable Rollout Acceptance — Korean Humanize Editor

## Summary

`korean-humanize-editor` has moved from pilot/observation to accepted internal operation after one day of real profile use without critical drift.

## Decision

```text
decision: accepted as internal stable rollout
decision date: 2026-06-20
accepted by: 주윤식
repo: jooys/im-not-ai
canonical branch: main
stable tag: internal-humanize-stable-2026-06-20
profile skill: korean-humanize-editor v0.1.7
```

The original one-week observation window is no longer required for this rollout because the user reviewed the first day of operation and approved promotion to stable internal use.

## Scope accepted

Enabled profile-local skill:

```text
muzel
default
muzrin
muzriel
muzria
muzback
```

The rollout remains profile-local. The following remain intentionally off:

```text
global install.sh/update.sh: OFF / not used
~/.claude / ~/.codex / Gemini global symlink rollout: OFF / not used
automatic post-processing: OFF
```

## Verification baseline

Last accepted verification before stable promotion:

```text
main CI: success
version_check_ok version=2.1.0
Korean humanize pilot gate: Contract PASS 13/13
profile smoke: PASS 5/5
critical fail: 0
```

## Operating rule after acceptance

1. Use `jooys/im-not-ai` `main` as the internal source of taxonomy/tests/docs.
2. Keep `epoko77-ai/im-not-ai` as upstream reference only.
3. Use the Hermes `korean-humanize-editor` skill only for explicit or contextually appropriate Korean writing polish.
4. Preserve facts, identifiers, judgment strength, scope, and confidence.
5. Keep profile-specific HOLD boundaries:
   - `muzriel`: brand/UI labels/layout/state badges.
   - `muzria`: QA verdict/evidence/expected-actual/repro semantics.
   - `muzback`: production/deploy/destructive/credential/admin/session/billing approval boundaries.
6. If drift appears later, add a fixture/profile smoke case and update the profile-local skill guard before broader use.

## Non-goals

- This is not an AI-detector bypass workflow.
- This does not authorize automatic rewriting of every message.
- This does not authorize upstream/global installer execution.
- This does not delete the old pilot branch; branch cleanup remains a separate repository maintenance action.
