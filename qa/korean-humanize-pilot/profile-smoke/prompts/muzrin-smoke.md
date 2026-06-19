다음 리서치 요약문을 `korean-humanize-editor` 기준으로 다듬어줘.

요구사항:
- 연구 요약 장르를 유지할 것
- 수치, 고유명사, branch, PR URL은 그대로 보존할 것
- “AI 탐지기 우회” 목적이 아니라 “문체 품질 개선” 관점으로만 정리할 것
- 결과는 `## 수정본`, `## 주요 변경`, `## 검증` 형식으로 작성할 것

원문:

무즈린 분석에 따르면 `epoko77-ai/im-not-ai`는 한국어 AI 문체 taxonomy, quick-rules, metric layer, Fast/Strict 구조에 있어서 참고 가치가 있다. 그러나 main branch의 버전·문서·테스트·marketplace 정합성이 깨져 있었고, 이를 통해 그대로 도입하기보다는 `jooys/im-not-ai`의 `internal/humanize-korean-pilot` branch와 PR https://github.com/jooys/im-not-ai/pull/1 기준으로 검증하는 것이 안정적이다. QA gate 결과는 Contract PASS 13/13, Critical fail 0이다.
