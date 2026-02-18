# Task phase1-budget-alert-rule

## Metadata
- project-id: ai-usage-windows-watcher
- source_mode: from_cycle_manager
- created_at: 2026-02-18 21:38 KST

## Collaboration Mode
- selected_mode: confirm_each_cycle
- re-confirm triggers:
  - 예산 정책/임계치 기준 변경
  - 경고 정책의 자동 액션 도입
  - 개인/팀 단위 정책 범위 확장

## 입력
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
- Cycle 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 태스크 요약:
  - 토큰 사용량 기반의 일/주 예산 임계치 알림 규칙을 UI에 표시하고 운영자가 즉시 대응할 수 있게 한다.

## 사용자 확인 게이트
- 핵심 내용:
  - 예산 초과 위험을 사전 인지할 수 있는 단순하고 명확한 규칙이 필요하다.
- 방향:
  - 환경변수 기반 임계치(일/주/경고비율) + UI 상태 텍스트 표시로 구현한다.
- 고민거리:
  - 비용이 아닌 토큰 기반 규칙이 실제 결제 체감과 다를 수 있음

## 문제 정의
- 해결 문제:
  - 현재 대시보드는 사용량 수치만 보여주고 임계치 상태를 알려주지 않는다.
- 비목표:
  - 외부 알림 채널(Slack/메일) 전송
  - 도구/모델별 가격표 자동 반영

## 구현 단위 (Coding 실행 단위)
- 작업 A: 예산 규칙 도메인 모듈 추가
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/budget_rules.py
  - 구현 상세:
    - 일/주 예산, 경고 비율 환경변수 로더
    - `normal/warning/critical` 판정 함수
  - 테스트:
    - 기본값 로딩, 경고/초과 판정 단위 테스트

- 작업 B: 대시보드 알림 패널 연동
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
  - 구현 상세:
    - 예산 상태/상세 텍스트 표시 패널 추가
    - 새로고침 시 최신 일/주 토큰 기준 상태 계산
  - 테스트:
    - 샘플 데이터 삽입 후 상태 문자열 갱신 확인

- 작업 C: 설정/가이드 문서 반영
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/.env.example
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
  - 구현 상세:
    - 예산 규칙 환경변수와 상태 의미를 문서화
  - 테스트:
    - 문서 예시 설정값으로 동작 확인

## 테스트 설계
- 기능 테스트:
  - 임계치 미만/근접/초과 데이터에서 상태가 올바르게 바뀌는지 확인
- 회귀 테스트:
  - 기존 일별/주별 집계와 OAuth 기능이 영향을 받지 않는지 점검
- 실패/예외 테스트:
  - 잘못된 환경변수 값(음수/문자열) 입력 시 기본값 폴백 검증

## 리스크 및 대응
- 리스크:
  - 토큰 기준과 실제 비용의 차이로 경고 피로 발생 가능
  - 대응:
    - 문서에 “토큰 기반 추정 규칙”임을 명시하고 추후 가격모델 태스크로 분리
- 리스크:
  - 임계치 기본값이 사용자 환경과 불일치할 수 있음
  - 대응:
    - `.env`로 빠르게 커스터마이즈 가능하도록 안내

## 완료 조건 (Definition of Done)
- DoD 1:
  - 예산 규칙 모듈이 환경변수 기반으로 동작한다.
- DoD 2:
  - 대시보드에 예산 상태(정상/주의/예산 경고)가 표시된다.
- DoD 3:
  - 환경변수/운영 가이드 문서가 최신 동작과 일치한다.

## Handoff
- To Coding:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- To Integration Test (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
- To Cycle Manager (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
