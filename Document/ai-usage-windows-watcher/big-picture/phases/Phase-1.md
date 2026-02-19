# Phase 1

## 목표
- Windows 사용량 수집기 에이전트와 기본 대시보드를 MVP로 제공한다.
- 기능 구현 완료 상태를 넘어, Windows 실기기 동작 검증 기준을 확정한다.
- 일반 사용자 기준의 무설치 실행 경로를 Phase 1 완료 조건으로 확정한다.

## 범위
- AI 도구 실행 세션 감지
- 로컬 저장소(SQLite) 적재
- 일/주 단위 집계 뷰
- OAuth 로그인(PKCE), 예산 임계치 알림, 1시간 자동 새로고침
- Windows 무설치 실행 번들(더블클릭 실행) 제공
- 테스트 게이트(자동 + 실기기 스모크) 정의

## 현재 상태 (2026-02-19)
- 코드 구현: 완료 (agent + desktop_win MVP)
- 로컬 자동화 테스트: `15 passed` (agent/.venv 기준)
- 미완료 항목:
  - Windows 10/11 실기기 E2E 증적(권장 수집)
  - OAuth 실공급자 연동 스모크 결과 기록
  - 실기기 기반 회귀 점검 루틴 정례화

## 완료 기준
- 수집 -> 저장 -> 조회 흐름이 단일 머신에서 재현된다.
- Python/Git 미설치 Windows 환경에서 앱 실행이 재현된다.
- OAuth 로그인, 예산 알림, 자동 새로고침이 자동 테스트/로컬 런타임 검증으로 재현된다.
- Integration Test (Pre)에서 자동 테스트(`pytest`, `py_compile`)가 통과한다.
- Integration Test (Pre) pass 이후 Git Release(publish/push)를 수행한다.
- `overview/modules/04-test-strategy.md`와 `overview/modules/05-windows-runtime-validation.md`의 게이트를 충족한다.
