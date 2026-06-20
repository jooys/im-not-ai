# Internal Adoption Plan — Korean Humanize Skill

## 목적

이 fork는 upstream `epoko77-ai/im-not-ai`를 우리 Hermes multi-profile 시스템에 바로 전역 설치하기 위한 repo가 아니다. 목적은 한국어 문서·보고·카피에서 번역투와 AI식 표현을 줄이는 **문체 품질 게이트**를 내부 skill wrapper로 안전하게 적용하는 것이다.

## 적용 원칙

1. **전역 설치 금지**
   - `install.sh`/`update.sh`가 `~/.claude`, `~/.codex`, Gemini extension에 symlink를 만들기 때문에 우리 시스템에는 직접 실행하지 않는다.
   - 실제 적용은 Hermes profile-local skill wrapper에서 시작한다.

2. **품질 개선 포지셔닝**
   - AI 사용 은폐나 AI 탐지기 우회 목적 요청에는 사용하지 않는다.
   - 사용자 목적을 가독성, 번역투 제거, 한국어 문체 개선으로 재정의할 수 있을 때만 진행한다.

3. **입력 데이터 경계**
   - 붙여넣은 원문 안의 명령형 문구는 실행 지시가 아니라 윤문 대상 데이터로 처리한다.
   - prompt injection 방어 문구는 Claude/Codex/Gemini runtime 모두에 존재해야 한다.

4. **의미 보존 우선**
   - 사실, 주장, 수치, 날짜, 고유명사, 직접 인용, 법률/정책 문구는 원문과 100% 일치해야 한다.
   - 의미 변경이 의심되면 `HOLD`로 보고하고 사람 검토를 요구한다.

## Phase 1 — Fork hygiene

### 반영한 upstream 패치

- PR #28: marketplace version, Fast output contract, broken tests cleanup
- PR #32: Fast output contract + injection guard
- PR #34: C-13 가운데점(·) 결합도 무시 나열 taxonomy 추가

### 내부 추가 패치

- manifest/SKILL/Gemini version을 `2.1.0`으로 통일
- manifest keyword `ai-detector` 제거
- Claude/Codex/Gemini runtime에 내부 fork 사용 범위와 prompt injection guard 추가
- README 상단에 전역 설치 금지 운영 주의 추가
- `scripts/version_check.py` 추가
- GitHub Actions CI 추가

### 검증 명령

```bash
python3 -m py_compile $(git ls-files '*.py')
python3 -m unittest discover -s tests -q
bash -n install.sh update.sh uninstall.sh
python3 scripts/version_check.py
git diff --check
```

## Phase 2 — Hermes skill wrapper

### 목표 skill

```text
korean-humanize-editor
```

### wrapper 범위

- 대상: 한국어 문서, Slack/Telegram 보고, 기획 문서, 리서치 요약, UI copy, 정책/스토어 카피 초안
- 제외: 코드, CLI 명령, 로그 원문, 법률/의료/정책 문서의 자동 확정본, 사용 은폐/탐지기 우회 요청

### profile rollout 순서

1. `muzel` — PM 보고/기획 문서 선택 적용
2. `default` — 자비스 최종 요약 중 긴 문서만 선택 적용
3. `muzrin` — 리서치 보고서 후처리 선택 적용
4. `muzriel` — UI copy/브랜드 문구 QA
5. `muzria` — 문체 QA fixture와 regression check
6. `muzback` — 릴리즈 노트/문서에만 제한 적용

## Phase 3 — QA gate

### 추가 guard

- C-13 가운데점 규칙은 본문 산문에서 결합도 낮은 독립 항목이 반복될 때만 후보로 본다.
- 제목, 표, 태그, UI 라벨, 코드/CLI/API/file path, 고유표기, 직접 인용 안의 가운데점은 자동 교정하지 않는다.
- 브랜드 핵심 문구, 법적/정책 문구, destructive action copy는 자동 PASS하지 않고 `HOLD`로 둔다.

### 최소 fixture

- PM/기획 문서 3개
- 리서치 보고서 3개
- UI/정책/스토어 카피 3개
- prompt injection 포함 악성 원문 2개

### PASS 기준

- critical fail 0건
- 수치/고유명사/직접 인용 보존 100%
- 입력 내부 명령 무시 100%
- 의미 drift 없음
- 번역투/AI식 관용구 감소가 사람이 보기에 확인 가능

### HOLD 기준

- 의미 변경 가능성
- 수치/고유명사/인용 훼손
- 과한 구어체화/문학체화
- 원문에 없는 주장·예시 추가
- 사용 목적이 탐지기 우회 또는 AI 사용 은폐로 명시됨

## 현재 운영 상태 — accepted stable rollout

```text
PR: https://github.com/jooys/im-not-ai/pull/1
merge commit: 9b17094a1a414b50794b27c56a44deaa7def28ef
post-merge CI: https://github.com/jooys/im-not-ai/actions/runs/27837848451
status: accepted stable internal rollout
canonical branch: main
stable tag: internal-humanize-stable-2026-06-20
profile skill: korean-humanize-editor v0.1.7
```

적용 완료 profile:

```text
muzel
fallback/default
muzrin
muzriel
muzria
muzback
```

검증 완료:

```text
Python compile PASS
unittest 57 tests OK
shell syntax PASS
version_check_ok version=2.1.0
Korean humanize pilot gate Contract PASS 13/13
profile smoke PASS 5/5
post-merge CI success
```

## 다음 운영 원칙

1. 내부 기준 소스는 이제 `jooys/im-not-ai` `main`이다.
2. 전역 `install.sh`/`update.sh`는 계속 실행하지 않는다.
3. Hermes profile-local `korean-humanize-editor` wrapper만 사용한다.
4. 자동 후처리는 켜지 않는다. 명시 요청 또는 적합한 문서 편집 상황에서만 사용한다.
5. 1일 실사용 관찰에서 critical drift가 없어 사용자 결정으로 stable rollout을 수용했다. 기존 1주 관찰 대기는 종료한다.
6. drift가 발견되면 fixture/profile smoke를 추가하고 skill guard를 보강한다.
