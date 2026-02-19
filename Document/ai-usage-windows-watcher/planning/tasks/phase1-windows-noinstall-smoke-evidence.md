# Task phase1-windows-noinstall-smoke-evidence

## Metadata
- project-id: ai-usage-windows-watcher
- source_mode: from_cycle_manager
- created_at: 2026-02-19 20:00 KST

## Collaboration Mode
- selected_mode: confirm_each_cycle
- re-confirm triggers:
  - Windows 검증 범위(Win10/Win11) 변경
  - 증적 포맷/보관 경로 정책 변경
  - 무설치 번들 구조(flat/`_internal`) 기준 변경

## 입력
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
- Cycle 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 태스크 요약:
  - Win10/Win11 onedir 무설치 실행 증적을 누락 없이 수집할 수 있도록 증적 수집 절차와 보조 스크립트를 강화한다.

## 사용자 확인 게이트
- 핵심 내용:
  - 현재 잔여 리스크는 코드 결함이 아니라 실기기 증적 미확보다.
- 방향:
  - 증적 생성 절차를 스크립트화해 누락 가능성을 낮추고 실행자 편차를 줄인다.
- 고민거리:
  - Windows 환경에서 수동 시나리오가 남는 항목을 어떤 수준까지 자동화할지

## 문제 정의
- 해결 문제:
  - 실기기 스모크를 수행해도 체크리스트/런타임 컨텍스트/증적 템플릿이 분산되어 기록 누락이 발생할 수 있다.
- 비목표:
  - OAuth 실공급자 신규 연동 개발
  - SmartScreen/코드서명 정책 확정
  - macOS/Linux 런타임 검증 확대

## 구현 단위 (Coding 실행 단위)
- 작업 A: 증적 수집 스크립트 확장
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
  - 구현 상세:
    - 런타임 컨텍스트에 번들 경로/레이아웃/핵심 파일 존재 여부/실행파일 해시를 포함한다.
    - 단일 명령으로 `run-id` 기반 증적 세트를 생성한다.
  - 테스트:
    - PowerShell 스크립트 정적 검토 + 문서 명령 정합성 점검

- 작업 B: 증적 템플릿/체크리스트 정합성 보강
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
  - 구현 상세:
    - run-id, artifact 경로, 번들 레이아웃 기록 항목을 고정한다.
  - 테스트:
    - 체크리스트 항목이 Big Picture Gate B/C 요구사항과 1:1로 대응되는지 확인

- 작업 C: 운영 문서 업데이트
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
  - 구현 상세:
    - 실기기 실행자가 복붙 가능한 명령으로 증적 생성 -> 체크리스트 수행 -> 제출 흐름을 문서화한다.
  - 테스트:
    - 신규 문서 절차를 따라 artifact 파일 경로가 일관되게 생성되는지 점검

## 테스트 설계
- 기능 테스트:
  - 실기기에서 `prepare_windows_smoke_evidence.ps1` 실행 시 run-id별 artifact 파일이 생성된다.
- 회귀 테스트:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/*.py`
- 실패/예외 테스트:
  - 번들 경로 누락 시 스크립트가 오류를 명확히 안내한다.
  - `_internal`/flat 레이아웃 모두에서 메타데이터가 정상 기록된다.

## 리스크 및 대응
- 리스크:
  - macOS 환경에서는 PowerShell 스크립트 실실행 검증이 불가
  - 대응:
    - Review/Integration 단계에서 Windows 실기기 실행 증적을 게이트로 강제
- 리스크:
  - 수동 체크리스트 입력 누락 가능성
  - 대응:
    - run-id 기반 아티팩트 생성 스크립트로 필수 파일 생성을 선행

## 완료 조건 (Definition of Done)
- DoD 1:
  - run-id 기준 증적 세트(runtime json/checklist/evidence)가 생성된다.
- DoD 2:
  - 번들 레이아웃(flat/`_internal`)과 실행파일/런처 존재 여부가 artifact에 기록된다.
- DoD 3:
  - Windows 운영 문서가 신규 증적 흐름을 반영한다.
- DoD 4:
  - 기존 자동 테스트가 회귀 없이 통과한다.

## Handoff
- To Coding:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- To Integration Test (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
- To Cycle Manager (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
