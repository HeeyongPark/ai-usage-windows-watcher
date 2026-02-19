# Task phase1-windows-noinstall-bundle

## Metadata
- project-id: ai-usage-windows-watcher
- source_mode: from_cycle_manager
- created_at: 2026-02-18 23:33 KST

## Collaboration Mode
- selected_mode: confirm_each_cycle
- re-confirm triggers:
  - 배포 형식(onefile/onedir/MSIX) 변경
  - 코드 서명/보안 정책 변경
  - OAuth 토큰 저장 경로 정책 변경

## 입력
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
- Cycle 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 태스크 요약:
  - Windows 사용자가 Python/Git/터미널 설치 없이 더블클릭으로 실행 가능한 무설치 번들을 제공한다.

## 사용자 확인 게이트
- 핵심 내용:
  - 터미널 기반 설치 절차가 사용자 온보딩을 막고 있어 실행 진입 장벽을 낮춰야 한다.
- 방향:
  - Phase 1에서는 설치 마법사보다 무설치 실행 번들(launcher + 실행 파일) 경로를 우선 제공한다.
- 고민거리:
  - 번들 크기/오탐/코드 서명 이슈를 어느 수준까지 허용할지

## 문제 정의
- 해결 문제:
  - 현재 배포 방식은 개발자 중심이라 일반 Windows 사용자에게 복잡한 설치 절차를 요구한다.
- 비목표:
  - 기업용 MSI 배포 체계 구축
  - macOS/Linux 무설치 배포 동시 지원

## 구현 단위 (Coding 실행 단위)
- 작업 A: Windows 무설치 번들 빌드 파이프라인 추가
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
  - 구현 상세:
    - Windows 빌드 머신에서 실행 가능한 번들 빌드 스크립트를 추가한다.
    - 결과물 구조(`dist/AIUsageWatcher/` 또는 동등 구조)와 실행 진입 파일명을 고정한다.
  - 테스트:
    - 스크립트 실행 시 번들 산출물 생성 여부 확인
    - 산출물 누락 시 에러 코드/메시지 검증

- 작업 B: 무설치 런처/실행 진입 경로 표준화
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/run_ai_usage_watcher.bat
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
  - 구현 상세:
    - 사용자가 더블클릭으로 실행 가능한 런처를 제공한다.
    - 런처가 `.env`/데이터 경로 전제를 명확히 안내하도록 한다.
  - 테스트:
    - Python/Git 미설치 Windows 환경에서 런처 실행 성공 확인
    - `.env` 누락/오류 시 사용자 안내 메시지 확인

- 작업 C: 실기기 검증 체크리스트를 무설치 기준으로 업데이트
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/overview/modules/05-windows-runtime-validation.md
  - 구현 상세:
    - 필수 시나리오 첫 단계를 "무설치 실행"으로 고정한다.
    - 증적에 배포 방식/실행 진입 파일 정보를 필수 항목으로 추가한다.
  - 테스트:
    - Win10/Win11 각 1회 체크리스트 수행 시 누락 없이 기록 가능한지 점검

## 테스트 설계
- 기능 테스트:
  - 무설치 번들 실행 후 OAuth 로그인/집계 조회/예산 알림/재시작 내구성 동작 확인
- 회귀 테스트:
  - `agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile agent/src/*.py desktop_win/src/*.py`
- 실패/예외 테스트:
  - 런처 파일 누락
  - `.env` 누락 또는 OAuth 필수 값 누락
  - 데이터 경로 쓰기 권한 부족 시나리오

## 리스크 및 대응
- 리스크:
  - 번들 파일이 커져 배포/다운로드 체감이 나빠질 수 있음
  - 대응:
    - 초기 Phase 1은 onedir 우선으로 안정성 확보 후 최적화는 Phase 2로 분리
- 리스크:
  - 코드 서명 부재 시 Windows SmartScreen 경고가 발생할 수 있음
  - 대응:
    - 실행 가이드에 경고 대응 절차와 해시 검증 안내를 명시

## 완료 조건 (Definition of Done)
- DoD 1:
  - Win10/Win11 클린 환경(Python/Git 미설치)에서 더블클릭 실행 성공 증적 1회 이상 확보
- DoD 2:
  - 무설치 번들 생성/실행 절차가 `WINDOWS_USAGE.md`와 `README.md`에 반영됨
- DoD 3:
  - 체크리스트/증적 템플릿이 무설치 실행 기준으로 갱신됨
- DoD 4:
  - 기존 자동 테스트(`pytest`, `py_compile`)가 회귀 없이 통과함

## Handoff
- To Coding:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- To Integration Test (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
- To Cycle Manager (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md

## Planning Update (2026-02-18 23:39 KST)
- 결정 사항:
  - 사용자 확정: `onefile`은 제외하고 `onedir`만 Phase 1 공식 배포 경로로 사용한다.
- 범위 조정:
  - 작업 A의 번들 빌드 파이프라인은 `onedir` 산출물(`dist/AIUsageWatcher/`) 고정 기준으로 구현한다.
  - `onefile` 빌드 옵션/검증 항목은 본 태스크 범위에서 제외한다.
- 테스트 조정:
  - Win10/Win11 실기기 검증은 `onedir` 런처 경로 기준으로만 통과 판정한다.
  - 실패 케이스에 `onedir` 폴더 누락/권한 오류 시나리오를 포함한다.
- DoD 보강:
  - `WINDOWS_USAGE.md`에 `onedir` 배포/실행 절차와 폴더 구조 예시를 명시한다.

## Planning Update (2026-02-18 23:58 KST)
- 재계획 배경:
  - Review(`fail`)에서 frozen 런타임 경로 불일치 가능성이 확인되어 planning으로 복귀한다.
- 핵심 결함:
  - onedir 기본 구조(`_internal`)와 코드의 `agent/src` 탐색 경로가 불일치할 수 있음
- 범위 조정:
  - 작업 A에 `--contents-directory` 정책을 명시해 빌드 산출물 구조를 고정한다.
  - 작업 B에 런처 사전 점검(실행 파일/핵심 폴더 존재 여부) 메시지를 보강한다.
  - 작업 C에 frozen 경로 해석 테스트를 추가한다(`sys._MEIPASS`, exe dir, `_internal`).
- 구현 지침:
  - 런타임 경로 탐색 우선순위:
    1) `sys._MEIPASS` 존재 시 우선
    2) `Path(sys.executable).parent`
    3) `Path(sys.executable).parent / \"_internal\"`
  - 세 경로 중 `agent/src/collector.py`가 존재하는 경로를 채택한다.
- 테스트 조정:
  - 단위 테스트에 frozen 시나리오 2종(평탄 구조, `_internal` 구조)을 추가한다.
  - Windows 실기기에서 번들 실행 후 import 오류 없음 증적을 필수로 남긴다.
- DoD 보강:
  - DoD 5: Win10/Win11 실기기에서 onedir 번들 첫 실행 시 `ModuleNotFoundError`가 재현되지 않는다.
