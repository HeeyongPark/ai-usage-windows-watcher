# 주제
AI Usage Watcher for Windows (윈도우 AI 사용량 워처)

## Collaboration Mode
- selected_mode: confirm_each_cycle
- re-confirm triggers:
  - 범위/목표 변경
  - 핵심 스택(언어/프레임워크) 변경
  - 개인정보 정책 변경

## Pipeline Order
- Big Picture -> Cycle Manager -> Planning -> Coding -> Review -> Integration Test (Pre) -> Git Release -> Deploy -> Integration Test (Post)

## Project Scope Override (2026-02-18)
- terminal_stage: git_release
- excluded_stages_this_project:
  - deploy
  - integration_test_post
- completion_rule:
  - Review 통과 + Integration Test (Pre) 통과 + Git Release 완료 시 `done` 처리

## Active Queue
1. [git_release] phase1-win-agent-usage-collector :: Windows 사용량 수집기 에이전트 MVP
2. [git_release] phase1-desktop-dashboard :: 로컬 대시보드 MVP
3. [git_release] phase1-budget-alert-rule :: 예산 임계치 알림 규칙

## Stage Board (Latest)
- queued:
- planning:
- coding:
- review:
- integration_test_pre:
- git_release:
  - phase1-win-agent-usage-collector
  - phase1-desktop-dashboard
  - phase1-budget-alert-rule
- deploy:
- integration_test_post:
- done:
- blocked:

## Cycle 1 (2026-02-18 16:03)

### 입력
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
- Notion 소스:
  - https://www.notion.so/mirador/30be497bcfdf807a877bdccfbdcbd8c4?source=copy_link
- 이전 사이클 carry-over:
  - 없음(초기 생성)

### 사용자 확인 게이트
- 핵심 내용:
  - AI 도구 사용량을 확인하는 완전 신규 프로젝트를 PodoNote 파이프라인으로 시작한다.
- 방향:
  - Windows MVP를 먼저 만들고, 첫 태스크는 사용량 수집기 에이전트로 고정한다.
- 고민거리:
  - 노션 원문 본문 부재 상태에서 초기 범위를 어디까지 추정할지

### 상태 전이
- before:
  - queued: 0
- after:
  - planning: 1
  - queued: 2
- 전이 이유:
  - 신규 subject 초기화와 동시에 첫 태스크를 planning 상태로 진입시켰다.

### Handoff To Planning (단일 태스크)
- task-id:
  - phase1-win-agent-usage-collector
- 입력:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 출력:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-win-agent-usage-collector.md

### 리스크 및 블로커
- 리스크:
  - 노션 요구사항 상세 부재로 Planning 정확도가 낮을 수 있음
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Planning (single task)
- 담당 스킬:
  - podonote-planning

## Cycle 2 (2026-02-18 16:20)

### 입력
- 선택 태스크:
  - phase1-win-agent-usage-collector
- 코드 저장소:
  - git@github.com:HeeyongPark/ai-usage-windows-watcher.git
- 로컬 경로:
  - /Users/mirador/Documents/ai-usage-windows-watcher

### 사용자 확인 게이트
- 핵심 내용:
  - 실제 코드 저장소를 지정 경로에 클론하고 첫 Coding 부트스트랩을 시작한다.
- 방향:
  - 빈 저장소에 agent MVP의 최소 실행 골격(collector/storage/cli/schema/test)을 먼저 구축한다.
- 고민거리:
  - 토큰 지표를 추정치로 시작할지, 도구별 API 연동으로 정밀화할지

### 상태 전이
- before:
  - phase1-win-agent-usage-collector: planning
- after:
  - phase1-win-agent-usage-collector: coding
- 전이 이유:
  - 저장소 클론 + 기본 실행 코드/테스트 통과로 Coding 단계에 진입했다.

### 리스크 및 블로커
- 리스크:
  - 현재는 샘플 이벤트 기반 수집기라 실제 프로세스 감지는 후속 구현 필요
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Review
- 담당 스킬:
  - podonote-review

## Cycle 16 (2026-02-18 22:37)

### 입력
- 선택 태스크:
  - phase1-win-agent-usage-collector
- Git Release 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/git-release/GitRelease.md

### 사용자 확인 게이트
- 핵심 내용:
  - pre-deploy 통과 태스크를 git release 단계로 전이한다.
- 방향:
  - 검증된 변경만 commit/tag/push 기준선으로 확정한다.
- 고민거리:
  - 없음

### 상태 전이
- before:
  - phase1-win-agent-usage-collector: integration_test_pre
- after:
  - phase1-win-agent-usage-collector: git_release
- 전이 이유:
  - 릴리즈 커밋(`88fd6e9`)과 태그(`v0.1.1-phase1`)가 원격에 반영되었다.

### 리스크 및 블로커
- 리스크:
  - 없음
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - terminal_stage reached (`git_release`)
- 담당 스킬:
  - podonote-cycle-manager

## Cycle 17 (2026-02-18 22:37)

### 입력
- 선택 태스크:
  - phase1-desktop-dashboard
- Git Release 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/git-release/GitRelease.md

### 사용자 확인 게이트
- 핵심 내용:
  - 대시보드 태스크를 git release 단계로 전이한다.
- 방향:
  - 동일 릴리즈 기준선으로 파이프라인 상태를 동기화한다.
- 고민거리:
  - 없음

### 상태 전이
- before:
  - phase1-desktop-dashboard: integration_test_pre
- after:
  - phase1-desktop-dashboard: git_release
- 전이 이유:
  - 통합 테스트 통과 후 동일 릴리즈 커밋 기준으로 전이했다.

### 리스크 및 블로커
- 리스크:
  - 없음
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - terminal_stage reached (`git_release`)
- 담당 스킬:
  - podonote-cycle-manager

## Cycle 18 (2026-02-18 22:37)

### 입력
- 선택 태스크:
  - phase1-budget-alert-rule
- Git Release 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/git-release/GitRelease.md

### 사용자 확인 게이트
- 핵심 내용:
  - 예산 규칙 태스크를 git release 단계로 전이한다.
- 방향:
  - project override에 맞춰 Deploy 없이 릴리즈 기준선까지 확정한다.
- 고민거리:
  - 없음

### 상태 전이
- before:
  - phase1-budget-alert-rule: integration_test_pre
- after:
  - phase1-budget-alert-rule: git_release
- 전이 이유:
  - 릴리즈 기준선 확정으로 다음 파이프라인 처리 대기 상태가 되었다.

### 리스크 및 블로커
- 리스크:
  - 없음
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - terminal_stage reached (`git_release`)
- 담당 스킬:
  - podonote-cycle-manager

## Cycle 13 (2026-02-18 22:37)

### 입력
- 선택 태스크:
  - phase1-win-agent-usage-collector
- Integration Test 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md

### 사용자 확인 게이트
- 핵심 내용:
  - 리뷰 완료 태스크를 pre-deploy 통합 테스트 단계로 전이한다.
- 방향:
  - `ui_optional` 프로파일로 자동 테스트 + 정적 검증 증적을 확보한다.
- 고민거리:
  - 인터랙티브 UI E2E는 후속 환경에서 확장 필요

### 상태 전이
- before:
  - phase1-win-agent-usage-collector: review
- after:
  - phase1-win-agent-usage-collector: integration_test_pre
- 전이 이유:
  - pre-deploy 검증이 pass(`9 passed`)로 확인되었다.

### 리스크 및 블로커
- 리스크:
  - UI 수동 시나리오는 별도 운영 점검 필요
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Git Release
- 담당 스킬:
  - podonote-git-release

## Cycle 14 (2026-02-18 22:37)

### 입력
- 선택 태스크:
  - phase1-desktop-dashboard
- Integration Test 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md

### 사용자 확인 게이트
- 핵심 내용:
  - 대시보드 태스크를 pre-deploy 통합 테스트 단계로 전이한다.
- 방향:
  - 동일 테스트 증적을 공유하고 태스크별 상태만 개별 전이한다.
- 고민거리:
  - UI 운영 환경 해상도별 수동 점검 필요

### 상태 전이
- before:
  - phase1-desktop-dashboard: review
- after:
  - phase1-desktop-dashboard: integration_test_pre
- 전이 이유:
  - pre-deploy 게이트가 pass로 판정되었다.

### 리스크 및 블로커
- 리스크:
  - UI 상호작용 테스트 자동화 범위는 제한적
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Git Release
- 담당 스킬:
  - podonote-git-release

## Cycle 15 (2026-02-18 22:37)

### 입력
- 선택 태스크:
  - phase1-budget-alert-rule
- Integration Test 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md

### 사용자 확인 게이트
- 핵심 내용:
  - 예산 알림 태스크를 pre-deploy 통합 테스트 단계로 전이한다.
- 방향:
  - 동일 검증 증적 기반으로 단계 전이를 마무리한다.
- 고민거리:
  - 토큰 기반 경고 모델의 비용 정합성은 후속 태스크에서 고도화

### 상태 전이
- before:
  - phase1-budget-alert-rule: review
- after:
  - phase1-budget-alert-rule: integration_test_pre
- 전이 이유:
  - pre-deploy 게이트 pass로 다음 단계 진입 조건을 충족했다.

### 리스크 및 블로커
- 리스크:
  - 비용 모델 정밀화 필요
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Git Release
- 담당 스킬:
  - podonote-git-release

## Cycle 6 (2026-02-18 21:40)

### 입력
- 선택 태스크:
  - phase1-win-agent-usage-collector
- Review 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

### 사용자 확인 게이트
- 핵심 내용:
  - 첫 태스크에 대해 Planning/Coding 정합성과 게이트 충족 여부를 확정한다.
- 방향:
  - 결함이 없으면 Review 단계까지 전이하고 Integration Test는 사용자 보류 요청을 따른다.
- 고민거리:
  - 로컬 환경에서 `pytest` 미설치 상태로 자동 테스트 증적이 제한됨

### 상태 전이
- before:
  - phase1-win-agent-usage-collector: coding
- after:
  - phase1-win-agent-usage-collector: review
- 전이 이유:
  - Review 판정이 pass(조건부)로 기록되어 Review 단계까지 완료했다.

### 리스크 및 블로커
- 리스크:
  - 테스트 러너 부재로 자동 테스트 재실행 미완료
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Integration Test (Pre) 대기 (사용자 보류)
- 담당 스킬:
  - integration-test-pre

## Cycle 7 (2026-02-18 21:43)

### 입력
- 선택 태스크:
  - phase1-desktop-dashboard
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md

### 사용자 확인 게이트
- 핵심 내용:
  - 두 번째 큐 태스크를 단일 태스크 Planning으로 진입시킨다.
- 방향:
  - 일/주 집계 분리와 UI 가독성 개선 중심으로 계획화한다.
- 고민거리:
  - 소형 화면에서 정보 밀도 증가를 어떻게 제어할지

### 상태 전이
- before:
  - phase1-desktop-dashboard: queued
- after:
  - phase1-desktop-dashboard: planning
- 전이 이유:
  - Active Queue 2번 태스크를 실행 대상으로 승격했다.

### Handoff To Planning (단일 태스크)
- task-id:
  - phase1-desktop-dashboard
- 입력:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 출력:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-desktop-dashboard.md

### 리스크 및 블로커
- 리스크:
  - 주차 표기가 사용자 친화적이지 않을 수 있음
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Coding
- 담당 스킬:
  - podonote-coding

## Cycle 8 (2026-02-18 21:44)

### 입력
- 선택 태스크:
  - phase1-desktop-dashboard
- Planning 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-desktop-dashboard.md

### 사용자 확인 게이트
- 핵심 내용:
  - 계획된 일/주 대시보드 범위를 실제 코드에 반영한다.
- 방향:
  - 저장소 쿼리 + 서비스 계층 + UI 탭을 최소 변경으로 확장한다.
- 고민거리:
  - 기존 기능(OAuth/자동갱신)에 회귀 영향이 없는지

### 상태 전이
- before:
  - phase1-desktop-dashboard: planning
- after:
  - phase1-desktop-dashboard: coding
- 전이 이유:
  - 구현 파일 변경과 검증 증적을 생성했다.

### 리스크 및 블로커
- 리스크:
  - pytest 부재로 신규 테스트 실행 미완료
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Review
- 담당 스킬:
  - podonote-review

## Cycle 9 (2026-02-18 21:45)

### 입력
- 선택 태스크:
  - phase1-desktop-dashboard
- Review 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

### 사용자 확인 게이트
- 핵심 내용:
  - 대시보드 확장 코드의 결함 유무와 문서 정합성을 확정한다.
- 방향:
  - 결함이 없으면 Review 단계까지 전이하고 이후 단계는 사용자 보류 요청을 따른다.
- 고민거리:
  - 테스트 미실행 상태를 조건부 통과로 둘지 여부

### 상태 전이
- before:
  - phase1-desktop-dashboard: coding
- after:
  - phase1-desktop-dashboard: review
- 전이 이유:
  - Review 판정 pass(조건부)로 기록되어 Review 단계까지 완료했다.

### 리스크 및 블로커
- 리스크:
  - 자동 테스트 재실행 미완료
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Integration Test (Pre) 대기 (사용자 보류)
- 담당 스킬:
  - integration-test-pre

## Cycle 10 (2026-02-18 21:46)

### 입력
- 선택 태스크:
  - phase1-budget-alert-rule
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md

### 사용자 확인 게이트
- 핵심 내용:
  - 세 번째 큐 태스크를 Planning 상태로 진입시킨다.
- 방향:
  - 토큰 기반 예산 임계치 규칙을 최소한의 정책으로 문서화한다.
- 고민거리:
  - 토큰 기준 경고와 실제 비용 경고의 괴리

### 상태 전이
- before:
  - phase1-budget-alert-rule: queued
- after:
  - phase1-budget-alert-rule: planning
- 전이 이유:
  - 큐 마지막 태스크를 실행 대상으로 승격했다.

### Handoff To Planning (단일 태스크)
- task-id:
  - phase1-budget-alert-rule
- 입력:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 출력:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-budget-alert-rule.md

### 리스크 및 블로커
- 리스크:
  - 임계치 기본값이 실제 사용 패턴에 맞지 않을 수 있음
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Coding
- 담당 스킬:
  - podonote-coding

## Cycle 11 (2026-02-18 21:47)

### 입력
- 선택 태스크:
  - phase1-budget-alert-rule
- Planning 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-budget-alert-rule.md

### 사용자 확인 게이트
- 핵심 내용:
  - 예산 규칙 모듈과 UI 연동을 구현해 운영 경고를 제공한다.
- 방향:
  - 환경변수 기반 정책 + 화면 상태 텍스트를 우선 구현한다.
- 고민거리:
  - 경고 상태 알림 빈도/표현 방식의 사용자 피로 가능성

### 상태 전이
- before:
  - phase1-budget-alert-rule: planning
- after:
  - phase1-budget-alert-rule: coding
- 전이 이유:
  - 규칙 모듈/테스트/문서 반영을 포함한 구현 작업을 완료했다.

### 리스크 및 블로커
- 리스크:
  - pytest 부재로 테스트 자동 실행 미완료
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Review
- 담당 스킬:
  - podonote-review

## Cycle 12 (2026-02-18 21:48)

### 입력
- 선택 태스크:
  - phase1-budget-alert-rule
- Review 산출물:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

### 사용자 확인 게이트
- 핵심 내용:
  - 예산 임계치 규칙의 정확성과 운영 문서 정합성을 검토한다.
- 방향:
  - 결함이 없으면 Review 단계까지 전이하고 이후 단계는 사용자가 추후 진행한다.
- 고민거리:
  - 토큰 기반 규칙에 대한 추후 비용 모델 고도화 필요성

### 상태 전이
- before:
  - phase1-budget-alert-rule: coding
- after:
  - phase1-budget-alert-rule: review
- 전이 이유:
  - Review 판정 pass(조건부)로 기록되어 Review 단계까지 완료했다.

### 리스크 및 블로커
- 리스크:
  - 자동 테스트 재실행 미완료
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Integration Test (Pre) 대기 (사용자 보류)
- 담당 스킬:
  - integration-test-pre

## Cycle 3 (2026-02-18 16:32)

### 입력
- 선택 태스크:
  - phase1-win-agent-usage-collector
- 사용자 추가 요구:
  - Codex 사용량 UI 우선
  - OAuth 최초 로그인
  - Windows 프로그램 형태

### 사용자 확인 게이트
- 핵심 내용:
  - 기존 CLI 우선 구현에 Windows UI + OAuth를 같은 사이클에서 우선 반영한다.
- 방향:
  - Tkinter 기반 대시보드와 OAuth(PKCE) 모듈을 추가해 즉시 가시성을 확보한다.
- 고민거리:
  - OAuth 공급자별 엔드포인트 차이를 공통 설정으로 얼마나 단순화할지

### 상태 전이
- before:
  - phase1-win-agent-usage-collector: coding
- after:
  - phase1-win-agent-usage-collector: coding
- 전이 이유:
  - 범위 확장 구현을 진행 중이며, Review 전 추가 검증/문서 정리를 수행한다.

### 리스크 및 블로커
- 리스크:
  - 현재 OAuth는 provider 설정 주입 방식이라 실제 운영 연동값 확정이 필요
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Review
- 담당 스킬:
  - podonote-review

## Cycle 4 (2026-02-18 16:31)

### 입력
- 선택 태스크:
  - phase1-win-agent-usage-collector
- 사용자 추가 요구:
  - Windows 사용법 문서 정리
  - 5인치 화면 기본 전체화면

### 사용자 확인 게이트
- 핵심 내용:
  - 실제 운영자가 바로 실행할 수 있는 Windows 중심 가이드를 제공한다.
- 방향:
  - 앱 시작 시 전체화면을 기본값으로 하고, 소형 해상도에서 자동 컴팩트 레이아웃을 적용한다.
- 고민거리:
  - 전체화면 기본 적용이 일반 모니터 사용성에 미치는 영향

### 상태 전이
- before:
  - phase1-win-agent-usage-collector: coding
- after:
  - phase1-win-agent-usage-collector: coding
- 전이 이유:
  - UI/문서 고도화 반영 후 Review 게이트로 전달한다.

### 리스크 및 블로커
- 리스크:
  - OAuth 공급자별 redirect URL 정책 차이로 초기 설정 실패 가능성
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Review
- 담당 스킬:
  - podonote-review

## Cycle 5 (2026-02-18 16:33)

### 입력
- 선택 태스크:
  - phase1-win-agent-usage-collector
- 사용자 추가 요구:
  - 데이터는 1시간에 1회 정도만 갱신

### 사용자 확인 게이트
- 핵심 내용:
  - 과도한 갱신 대신 시간 기반 자동 갱신으로 운영 부하를 줄인다.
- 방향:
  - 기본 자동 갱신 주기를 3600초로 설정하고 UI에 마지막 갱신 시각을 노출한다.
- 고민거리:
  - 추후 실시간 감시 모드가 필요할 때 주기를 어떻게 정책화할지

### 상태 전이
- before:
  - phase1-win-agent-usage-collector: coding
- after:
  - phase1-win-agent-usage-collector: coding
- 전이 이유:
  - 운영 요구 반영을 Coding에 추가 적용했고 Review 게이트 준비를 진행한다.

### 리스크 및 블로커
- 리스크:
  - 너무 긴 주기로 설정 시 최신성 요구가 있는 화면에서 체감 지연 가능
- 블로커:
  - 없음

### 다음 액션
- 다음 단계:
  - Review
- 담당 스킬:
  - podonote-review
