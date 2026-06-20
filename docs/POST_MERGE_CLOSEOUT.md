# Korean Humanize Editor Post-Merge Closeout

## Summary

Internal pilot PR #1 was merged into `main` after deterministic QA, profile-local rollout, real Hermes profile smoke, and post-merge CI verification. After one day of real use without critical drift, the rollout was accepted as stable internal operation.

## Merge

```text
PR: https://github.com/jooys/im-not-ai/pull/1
base: main
head: internal/humanize-korean-pilot
merge commit: 9b17094a1a414b50794b27c56a44deaa7def28ef
post-merge CI: https://github.com/jooys/im-not-ai/actions/runs/27837848451
conclusion: success
```

## Verification

Local post-merge verification on `main`:

```text
python3 -m py_compile $(git ls-files '*.py')              PASS
python3 -m unittest discover -s tests -q                  57 tests OK
bash -n install.sh update.sh uninstall.sh                 PASS
python3 scripts/version_check.py                          version_check_ok version=2.1.0
python3 scripts/qa_humanize_gate.py ...                   Contract PASS 13/13
git diff --check                                          PASS
```

Profile smoke artifacts from the merged branch:

```text
qa/korean-humanize-pilot/profile-smoke/report.md          PASS 5/5
qa/korean-humanize-pilot/profile-smoke/manual-review.md   PASS with profile-specific notes
```

## Runtime rollout

Enabled profile-local skill:

```text
korean-humanize-editor v0.1.8
profiles: muzel, default, muzrin, muzriel, muzria, muzback
status: accepted stable internal rollout
stable tag: internal-humanize-stable-2026-06-20
```

The rollout remains profile-local. The upstream/global installers are not used.

```text
install.sh/update.sh: NOT RUN for Hermes profiles
~/.claude / ~/.codex / Gemini global symlink: NOT USED
automatic post-processing: OFF
```

## Guard boundaries

- General: preserve facts, numbers, names, quotes, judgment strength, range, and confidence.
- `muzriel`: preserve brand copy, UI labels, layout tokens, state badges.
- `muzria`: preserve QA verdicts, expected/actual, evidence paths, reproduction semantics.
- `muzback`: preserve production/deploy/destructive/credential/admin/session/billing approval boundaries.

## Accepted operation

1. Treat `main` as the canonical internal fork branch.
2. Keep `epoko77-ai/im-not-ai` as upstream reference only.
3. Add fixture/profile smoke cases whenever a profile-specific drift is found.
4. Do not enable automatic rewriting without a separate explicit rollout decision.
5. Do not run global `install.sh`/`update.sh` for Hermes profiles.
6. The former one-week observation window is closed early by user decision after one day of acceptable operation.
