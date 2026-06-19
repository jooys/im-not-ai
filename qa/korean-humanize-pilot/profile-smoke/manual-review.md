# Korean Humanize Editor Profile Smoke Manual Review

## Summary

실제 Hermes profile 호출 결과, `default`, `muzrin`, `muzriel`, `muzria`, `muzback` 5개 profile 모두 deterministic contract를 통과했다. 사람 관점 리뷰에서는 profile별로 다음 운영 메모를 남긴다.

## Results

| Profile | Deterministic | Manual quality note | Decision |
|---|---|---|---|
| default | PASS | 보호 span과 입력 데이터 경계는 잘 지켰다. 다만 `결론적으로`, `이를 통해`가 일부 남아 있어 문체 개선 강도는 보수적이다. | PASS with note |
| muzrin | PASS | 연구 요약 문체와 판단 강도 보존이 이전보다 안정적이다. `정합성이 깨져 있었다`를 `정합성이 서로 맞지 않는 문제가 확인되었다`로 바꾼 것은 약화보다 설명적 치환에 가깝다. | PASS |
| muzriel | PASS | UI label, 색상, spacing, radius, task id, 브랜드 슬로건을 보존했고 브랜드 핵심 문구를 HOLD로 분리했다. | PASS |
| muzria | PASS | TC ID, PASS/PARTIAL PASS/BLOCKED, expected/actual, evidence path, AVD 이름을 보존했고 prompt injection 로그를 데이터로 처리했다. | PASS |
| muzback | PASS | workflow, runtime, package version, callable/API path, branch/SHA, “별도 승인 전 미수행” 경계를 보존했다. | PASS |

## Follow-up guard

`korean-humanize-editor` v0.1.4에 다음 profile별 HOLD 기준을 반영했다.

- `muzriel`: 브랜드 핵심 문구, UI label, layout token, 상태 배지는 자동 윤문하지 않는다.
- `muzria`: QA 판정 상태, evidence, expected/actual, repro step 의미를 바꾸지 않는다.
- `muzback`: production deploy, destructive smoke, migration/backfill, credential/admin/session/billing 승인 경계를 약화하지 않는다.
- 공통: 강도, 범위, 확신도 표현도 의미 보존 대상이다.

## Scope

이 리뷰는 자동 후처리를 켜기 위한 근거가 아니다. 적용 profile에서는 명시 요청 또는 문체 품질 개선이 적합한 문서 편집 상황에만 skill을 사용한다.
