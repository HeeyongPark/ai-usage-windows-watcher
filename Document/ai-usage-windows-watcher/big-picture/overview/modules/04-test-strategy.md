# 테스트 전략

## 목적
- 기능 구현 완료 여부가 아니라 "재현 가능한 품질 상태"를 기준으로 Phase 1을 통과시킨다.

## 현재 기준선 (2026-02-19)
- 자동 테스트 결과: `15 passed`
- 포함 범위:
  - agent 저장/집계 로직 단위 테스트
  - desktop 환경변수/OAuth 토큰 저장/예산 규칙/집계 서비스 테스트
  - frozen 런타임 경로 해석 단위 테스트
- 공백:
  - Windows 실기기 UI + OAuth 전체 흐름 E2E 증적 부재(권장 수집)
  - onedir `_internal` 구조 실기기 검증 증적 부재(권장 수집)

## 테스트 레벨
- Unit:
  - `agent/tests/`, `desktop_win/tests/` 유지
- Integration (로컬):
  - 샘플 데이터 삽입 후 UI 일/주 집계 일관성 확인
- Runtime Smoke (Windows 실기기):
  - 무설치 번들 실행/로그인/집계/예산 상태/재시작 후 토큰 유지 확인

## 게이트 (Phase 1)
- Gate A:
  - 로컬 자동 테스트 전부 통과
- Gate B:
  - Windows 10/11 최소 각 1회 무설치 실행 스모크 완료(권장, non-blocking)
- Gate C:
  - 실패 케이스(잘못된 OAuth 설정, DB 경로 변경, 최소 갱신 주기, 런처 실행 실패, frozen import 실패) 재현 기록 확보(권장, non-blocking)

## 프로젝트 한정 Override (2026-02-19)
- 적용 대상:
  - `ai-usage-windows-watcher` 프로젝트 한정
- Integration Test (Pre) 판정:
  - `ui_optional` 프로파일을 기본으로 사용
  - `pytest` + `py_compile` 통과 시 pass
- Push 게이트:
  - 자동 테스트 통과된 pre-deploy pass 상태에서만 git_release/push 진행

## 산출물 포맷
- 필수 증적:
  - 실행 환경 정보(OS/해상도/배포 방식)
  - 테스트 체크리스트 결과(pass/fail)
  - 실패 시 로그/스크린샷/재현 절차
