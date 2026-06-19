# Human Review Samples

`korean-humanize-editor`를 실제 무즈엘 보고 문서에 적용한 사람 검토용 샘플이다. 원본 운영 문서를 덮어쓰지 않고, repo-local sample로만 보존한다.

## Samples

- `MZL-01.md` — Slack thread 최종 진행 보고 샘플
- `MZL-02.md` — Obsidian 내부 pilot 기준 문서 샘플

## Gate

두 샘플은 `qa/korean-humanize-pilot/fixtures` / `outputs`에도 포함되어 `scripts/qa_humanize_gate.py`로 deterministic safety contract를 검증한다.

사람 검토 기준:

- 의미 drift 없음
- 기술 식별자/URL/path/commit hash 보존
- 사용자-facing 보고문으로 더 읽기 쉬움
- 과한 구어체화 없음
- 탐지기 우회 목적 표현 없음
