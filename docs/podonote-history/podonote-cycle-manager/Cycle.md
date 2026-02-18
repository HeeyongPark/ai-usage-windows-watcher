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

## Active Queue
1. [coding] phase1-win-agent-usage-collector :: Windows 사용량 수집기 에이전트 MVP
2. [queued] phase1-desktop-dashboard :: 로컬 대시보드 MVP
3. [queued] phase1-budget-alert-rule :: 예산 임계치 알림 규칙

## Stage Board (Latest)
- queued:
  - phase1-desktop-dashboard
  - phase1-budget-alert-rule
- planning:
- coding:
  - phase1-win-agent-usage-collector
- review:
- integration_test_pre:
- git_release:
- deploy:
- integration_test_post:
- done:
- blocked:

## Cycle 1 (2026-02-18 16:03)

### 입력
- Big Picture 소스:
  - /Users/mirador/Documents/PodoNoteProject/Document/PodoNote/ai-usage-windows-watcher/podonote-big-picture/BigPicture.md
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
  - /Users/mirador/Documents/PodoNoteProject/Document/PodoNote/ai-usage-windows-watcher/podonote-cycle-manager/Cycle.md
- 출력:
  - /Users/mirador/Documents/PodoNoteProject/Document/PodoNote/ai-usage-windows-watcher/podonote-planning/tasks/phase1-win-agent-usage-collector.md

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
