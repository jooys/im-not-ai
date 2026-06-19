다음 backend/release note를 `korean-humanize-editor` 기준으로 다듬어줘.

요구사항:
- workflow name, runtime, package version, function/API name, run id, commit SHA, branch는 그대로 보존할 것
- production deploy, destructive smoke, migration/backfill 범위를 임의로 확정하지 말 것
- “별도 승인 전 미수행” 표현은 유지할 것
- 결과는 `## 수정본`, `## 주요 변경`, `## 검증` 형식으로 작성할 것

원문:

무즈백 closeout에 따르면 `Deploy All` workflow run 27830975208은 backend/admin path에 있어서 success로 확인됐다. Functions runtime은 nodejs22이고 firebase-admin은 14.x이며 callable `deleteUserAccount`와 API path `/api/sources/system`을 통해 운영 상태를 확인할 수 있다. 그러나 production destructive smoke와 migration/backfill은 별도 승인 전 미수행 상태다. branch는 `internal/humanize-korean-pilot`, commit은 `3cc3a4e036a171012980e5dda17652034f6c20f4`이다.
