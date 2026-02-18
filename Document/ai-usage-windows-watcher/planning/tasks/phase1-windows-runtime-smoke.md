# Task phase1-windows-runtime-smoke

## Metadata
- project-id: ai-usage-windows-watcher
- source_mode: from_cycle_manager
- created_at: 2026-02-18 22:57 KST

## Collaboration Mode
- selected_mode: confirm_each_cycle
- re-confirm triggers:
  - Windows 지원 범위(Win10/Win11) 변경
  - OAuth 공급자/콜백 정책 변경
  - 실기기 검증 결과에서 P0 결함 발견

## 입력
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
- Cycle 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 태스크 요약:
  - Windows 10/11 실기기에서 설치 -> OAuth -> 집계 조회 -> 예산 알림 -> 재시작 내구성까지 스모크 검증을 수행하고 증적 포맷을 표준화한다.

## 사용자 확인 게이트
- 핵심 내용:
  - 기능 구현 완료 상태를 실사용 검증 가능한 상태로 전환해야 한다.
- 방향:
  - 자동 테스트(`pytest`) + 실기기 체크리스트(수동)를 함께 게이트로 운영한다.
- 고민거리:
  - OAuth 실공급자 테스트 계정 준비 상태에 따라 일부 시나리오가 지연될 수 있다.

## 문제 정의
- 해결 문제:
  - 현재 문서와 테스트는 구현 정합성은 보장하지만, Windows 실기기 동작 증적이 부족해 릴리즈 신뢰도가 낮다.
- 비목표:
  - 신규 기능 개발
  - macOS/Linux 런타임 공식 검증 확대

## 구현 단위 (Coding 실행 단위)
- 작업 A: 실기기 검증 체크리스트/증적 템플릿 작성
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
  - 구현 상세:
    - Win10/Win11 공통 체크리스트(필수 시나리오 6개) 정의
    - P0/P1/P2 실패 등급 기준과 증적 수집 규칙 명시
  - 테스트:
    - 체크리스트 항목이 Big Picture의 `04-test-strategy`, `05-windows-runtime-validation`과 1:1 대응하는지 점검

- 작업 B: Windows 런타임 환경 수집 스크립트 추가
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
  - 구현 상세:
    - OS 버전, Python 버전, 화면 해상도, APPDATA/DB 경로 등 실행 환경 정보를 JSON으로 저장
  - 테스트:
    - PowerShell 실행 시 JSON 파일이 정상 생성되는지 확인

- 작업 C: 운영 가이드에 스모크 실행 절차 반영
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
  - 구현 상세:
    - 실기기 스모크 수행 순서, 증적 저장 위치, 실패 리포트 규칙 문서화
  - 테스트:
    - 신규 섹션 기준으로 "새 Windows 머신에서 문서만 보고 재현" 가능한지 자체 점검

## 테스트 설계
- 기능 테스트:
  - `agent/.venv/bin/python -m pytest -q` 통과로 자동 게이트(Gate A) 확인
- 회귀 테스트:
  - `python3 -m py_compile`로 agent/desktop_win 코드 정적 컴파일 확인
- 실패/예외 테스트:
  - OAuth 설정 누락, DB 경로 변경, 최소 갱신 주기(60초 미만 입력) 시 기대 동작 확인
- 실기기 스모크:
  - Win10/Win11 각 1회 체크리스트 수행 후 pass/fail 증적 기록

## 리스크 및 대응
- 리스크:
  - 실제 OAuth 공급자 인증 환경이 즉시 준비되지 않을 수 있음
  - 대응:
    - 공급자 의존 항목은 `blocked`로 분리 기록하고 로컬 시나리오부터 선검증
- 리스크:
  - 수동 테스트 결과 포맷이 불일치할 수 있음
  - 대응:
    - 템플릿 기반 기록을 강제하고 파일 경로 규칙을 문서에 명시

## 완료 조건 (Definition of Done)
- DoD 1:
  - 실기기 스모크 체크리스트/증적 템플릿이 저장소에 추가되고 Big Picture 기준과 정합성을 가진다.
- DoD 2:
  - Windows 환경 수집 스크립트로 실행 컨텍스트를 JSON으로 저장할 수 있다.
- DoD 3:
  - Windows 가이드에 스모크 실행/증적 관리 절차가 반영된다.
- DoD 4:
  - 자동 테스트(`pytest`, `py_compile`) 증적이 최신 상태로 기록된다.

## Handoff
- To Coding:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- To Integration Test (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
- To Cycle Manager (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
