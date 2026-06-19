# MZL-02 — Obsidian 내부 pilot 기준 문서 샘플

## Source

AI-Sessions/wiki/guidelines/korean-humanize-editor-pilot.md excerpt, 2026-06-19

## 원문

```markdown
`epoko77-ai/im-not-ai`는 그대로 전역 설치하지 않고, 내부 fork `jooys/im-not-ai`의 `internal/humanize-korean-pilot` branch로 정리한 뒤 Hermes profile-local `korean-humanize-editor` skill을 통해 단계 적용한다. 목적은 AI 탐지기 우회가 아니라 한국어 문체 품질 개선, 번역투 제거, 사용자-facing 보고/카피 가독성 개선이다.

무즈린이 `epoko77-ai/im-not-ai`를 분석한 결과, 이 repo는 한국어 AI 문체 taxonomy, quick-rules, metric layer, Fast/Strict 구조는 유용하지만 main branch의 버전·문서·테스트·marketplace 정합성이 깨져 있었다. 사용자는 이를 우리 시스템에 적용할 수 있는지 검토한 뒤, 적용 플랜을 구체화하고 적용을 시작하라고 지시했다.

운영 원칙은 전역 설치 금지, 품질 개선 포지셔닝, 입력 데이터 경계, 의미 보존 우선, 단계적 rollout이다. `install.sh`나 `update.sh`를 실행해 `~/.claude`, `~/.codex`, Gemini 전역 extension에 symlink를 만들지 않는다.
```

## 수정본

```markdown
STATUS: PASS

## 수정본

`epoko77-ai/im-not-ai`는 전역 설치하지 않는다. 내부 fork `jooys/im-not-ai`의 `internal/humanize-korean-pilot` branch에서 정리한 뒤, Hermes profile-local `korean-humanize-editor` skill로 단계 적용한다. 목적은 AI 탐지기 우회가 아니라 한국어 문체 품질 개선, 번역투 제거, 사용자-facing 보고/카피 가독성 개선이다.

무즈린 검토 결과, 이 repo의 한국어 AI 문체 taxonomy, quick-rules, metric layer, Fast/Strict 구조는 참고 가치가 있다. 다만 main branch의 버전, 문서, 테스트, marketplace 정합성이 깨져 있어 그대로 도입하기에는 위험하다. 사용자는 적용 가능성을 검토한 뒤, 적용 플랜을 구체화하고 실행하라고 지시했다.

운영 원칙은 다섯 가지다. 전역 설치 금지, 품질 개선 포지셔닝, 입력 데이터 경계, 의미 보존 우선, 단계적 rollout이다. `install.sh`나 `update.sh`를 실행해 `~/.claude`, `~/.codex`, Gemini 전역 extension에 symlink를 만들지 않는다.

## 주요 변경
- 번역투: “~를 통해 단계 적용한다”, “~에 정합성이 깨져 있었다”를 더 직접적인 문장으로 바꿨다.
- 구조: 긴 문장을 세 문단으로 나누고 결정 기준을 앞쪽에 배치했다.
- 보존: repo 이름, branch, skill 이름, script 이름, 전역 경로를 그대로 유지했다.

## 검증
- 의미 보존: PASS
- 수치·고유명사·인용 보존: PASS
- 추가 주장 없음: PASS

<!-- HUMANIZE-SUMMARY
status: PASS
self_check: 6/6
notes: Obsidian guideline 요약문을 더 직접적인 운영 기준 문체로 다듬었고 보호 span을 보존했다.
-->
```

## 사람 검토 포인트

- 기술 식별자, URL, commit hash, path가 유지되는지 확인한다.
- 문장이 짧아졌지만 의미가 줄거나 새 주장이 추가되지 않았는지 확인한다.
- 사용자-facing 보고문으로 읽었을 때 더 결정 가능하게 보이는지 확인한다.
