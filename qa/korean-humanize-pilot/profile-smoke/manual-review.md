# Korean Humanize Editor Profile Smoke Manual Review

## Summary

실제 Hermes profile 호출 결과, `default`와 `muzrin` 모두 deterministic contract는 통과했다. 다만 사람 관점 리뷰에서 품질 개선 포인트가 2개 발견됐다.

## Results

| Profile | Deterministic | Manual quality note | Decision |
|---|---|---|---|
| default | PASS | 보호 span과 입력 데이터 경계는 잘 지켰다. 다만 `결론적으로`, `이를 통해`가 일부 남아 있어 문체 개선 강도는 보수적이다. | PASS with note |
| muzrin | PASS | 연구 요약 문체는 자연스럽다. 다만 원문의 “정합성이 깨져 있었다”가 “정합성이 일부 깨져 있었다”로 약화되어 확신도/범위 drift 가능성이 있다. | PASS with guard update |

## Follow-up guard

`korean-humanize-editor` skill에 다음 원칙을 추가한다.

- 강도, 범위, 확신도 표현도 의미 보존 대상이다.
- `깨져 있었다` → `일부 깨져 있었다`, `낮다` → `다소 낮다`, `확인됐다` → `가능성이 있다`처럼 원문의 판단 강도를 임의로 약화하지 않는다.
- 반대로 `가능성이 있다` → `확정됐다`처럼 강화하지도 않는다.

## Scope

이 리뷰는 자동 후처리를 켜기 위한 근거가 아니다. `default`/`muzrin`에서 명시 요청 또는 적합한 문서 편집 상황에만 skill을 사용한다.
