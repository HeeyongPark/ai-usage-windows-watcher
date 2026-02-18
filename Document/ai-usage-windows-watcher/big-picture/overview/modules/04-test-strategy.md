# 테스트 전략

## 목적
- 기능 구현 완료 여부가 아니라 "재현 가능한 품질 상태"를 기준으로 Phase 1을 통과시킨다.

## 현재 기준선 (2026-02-18)
- 자동 테스트 결과: `9 passed`
- 포함 범위:
  - agent 저장/집계 로직 단위 테스트
  - desktop 환경변수/OAuth 토큰 저장/예산 규칙/집계 서비스 테스트
- 공백:
  - Windows 실기기 UI + OAuth 전체 흐름 E2E 부재
  - 운영 환경(PowerShell 설치/실행) 스모크 부재

## 테스트 레벨
- Unit:
  - `agent/tests/`, `desktop_win/tests/` 유지
- Integration (로컬):
  - 샘플 데이터 삽입 후 UI 일/주 집계 일관성 확인
- Runtime Smoke (Windows 실기기):
  - 앱 실행/로그인/집계/예산 상태/재시작 후 토큰 유지 확인

## 게이트 (Phase 1)
- Gate A:
  - 로컬 자동 테스트 전부 통과
- Gate B:
  - Windows 10/11 최소 각 1회 실기기 스모크 완료
- Gate C:
  - 실패 케이스(잘못된 OAuth 설정, DB 경로 변경, 최소 갱신 주기) 재현 기록 확보

## 산출물 포맷
- 필수 증적:
  - 실행 환경 정보(OS/Python/해상도)
  - 테스트 체크리스트 결과(pass/fail)
  - 실패 시 로그/스크린샷/재현 절차
