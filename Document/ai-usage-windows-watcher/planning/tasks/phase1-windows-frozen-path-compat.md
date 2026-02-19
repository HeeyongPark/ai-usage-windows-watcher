# Task phase1-windows-frozen-path-compat

## Metadata
- project-id: ai-usage-windows-watcher
- source_mode: from_cycle_manager
- created_at: 2026-02-19 16:49 KST

## Collaboration Mode
- selected_mode: confirm_each_cycle
- re-confirm triggers:
  - frozen 경로 전략 변경(`sys._MEIPASS`/`_internal`/exe dir)
  - PyInstaller 빌드 산출물 구조 정책 변경
  - 무설치 배포 형식 변경(onedir -> 기타)

## 입력
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
- Cycle 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 태스크 요약:
  - onedir frozen 런타임에서 `_internal` 구조 차이로 발생 가능한 import 실패를 제거하고 경로 전략을 고정한다.

## 사용자 확인 게이트
- 핵심 내용:
  - 무설치 실행 목표를 막는 핵심 결함(`ModuleNotFoundError` 가능성)을 우선 제거해야 한다.
- 방향:
  - 런타임 경로 탐색 전략과 빌드 산출물 구조를 함께 확정한다.
- 고민거리:
  - `sys._MEIPASS` 기반 탐색과 `--contents-directory` 고정의 조합에서 유지보수성이 가장 높은 기준

## 문제 정의
- 해결 문제:
  - 코드가 `sys.executable` 부모만 기준으로 경로를 찾을 때, PyInstaller onedir 기본 `_internal` 구조에서 import 실패가 발생할 수 있다.
- 비목표:
  - 코드서명 자동화
  - MSI/MSIX 배포 체계 도입
  - OAuth 공급자 확장

## 구현 단위 (Coding 실행 단위)
- 작업 A: frozen 런타임 경로 해석기 확정
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py
  - 구현 상세:
    - 런타임 경로 탐색 우선순위를 명시한다.
      - 1) `sys._MEIPASS`
      - 2) `Path(sys.executable).parent`
      - 3) `Path(sys.executable).parent / "_internal"`
    - `agent/src/collector.py` 또는 `.env` 존재 여부를 기준으로 유효 경로를 선택한다.
  - 테스트:
    - frozen 시뮬레이션 단위 테스트에서 평탄 구조/`_internal` 구조 모두 통과

- 작업 B: 빌드 산출물 구조 정책 고정
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/run_ai_usage_watcher.bat
  - 구현 상세:
    - PyInstaller 옵션(`--contents-directory` 포함 여부)을 코드 경로 전략과 일치시킨다.
    - 런처에서 핵심 경로 누락 시 안내 메시지를 명확히 한다.
  - 테스트:
    - 빌드 산출물 경로 체크(실행 파일/핵심 폴더/런처 존재) 자동 검증

- 작업 C: 테스트/운영 문서 정합성 보강
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_usage_service.py
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_env_loader.py
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
  - 구현 상세:
    - frozen import 실패 케이스를 테스트/문서 게이트에 반영한다.
    - 실행 증적 템플릿에 bundle layout(flat/`_internal`) 필드를 고정한다.
  - 테스트:
    - 로컬 pytest/py_compile 통과
    - Windows 실기기에서 onedir 첫 실행 시 import 오류 없음 확인(후속 증적)

## 테스트 설계
- 기능 테스트:
  - onedir 번들 실행 시 로그인 전 앱 기동 성공 확인
- 회귀 테스트:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py`
- 실패/예외 테스트:
  - `_internal` 구조에서 import 실패 재현 여부
  - `.env` 누락 시 안내 메시지 동작
  - 런처/실행 파일 누락 시 에러 경로 확인

## 리스크 및 대응
- 리스크:
  - 플랫폼별 PyInstaller 동작 차이로 로컬 테스트와 실기기 결과가 다를 수 있음
  - 대응:
    - Windows 실기기 기준 검증 결과를 최종 판정 근거로 고정
- 리스크:
  - Notion 원문 동기화 지연으로 문서 이중 기준 발생
  - 대응:
    - 현재 사이클은 로컬 문서를 기준 소스 오브 트루스로 운영하고 인증 복구 후 재동기화

## 완료 조건 (Definition of Done)
- DoD 1:
  - frozen 런타임 경로 탐색이 `_MEIPASS`/exe dir/`_internal`을 포괄한다.
- DoD 2:
  - onedir 번들 첫 실행에서 `ModuleNotFoundError`가 재현되지 않는다.
- DoD 3:
  - pytest/py_compile가 최신 기준으로 통과한다.
- DoD 4:
  - Windows 운영 문서/체크리스트/증적 템플릿이 frozen 경로 전략과 일치한다.

## Handoff
- To Coding:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- To Integration Test (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
- To Cycle Manager (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md

## Planning Refresh (2026-02-19 17:25 KST)
- Notion 인증 복구 후 원문/하위 문서 동기화 재검증 결과, 본 태스크의 문제 정의/우선순위/DoD를 유지한다.
- Coding 진입 조건은 변경하지 않는다.
