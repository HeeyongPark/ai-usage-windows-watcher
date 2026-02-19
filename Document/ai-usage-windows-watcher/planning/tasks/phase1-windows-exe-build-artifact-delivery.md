# Task phase1-windows-exe-build-artifact-delivery

## Metadata
- project-id: ai-usage-windows-watcher
- source_mode: standalone
- created_at: 2026-02-19 23:36 KST

## Collaboration Mode
- selected_mode: confirm_each_cycle
- re-confirm triggers:
  - Windows 빌드 채널 정책 변경(로컬 수동 전용 <-> CI 기본)
  - 배포 산출물 형식 변경(onedir <-> other)
  - 아티팩트 보관/전달 방식 변경(GitHub artifact <-> release asset)

## 입력
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
- Cycle 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 태스크 요약:
  - Windows가 없는 개발 환경에서도 `AIUsageWatcher.exe`를 일관되게 생성/전달할 수 있도록 Windows CI 빌드 경로를 표준화한다.

## 사용자 확인 게이트
- 핵심 내용:
  - 현재 환경(macOS)에서는 PowerShell/Windows 제약으로 `exe`를 직접 생성할 수 없다.
- 방향:
  - GitHub Actions `windows-latest`에서 공식 빌드 스크립트를 실행해 번들 + 체크섬을 artifact로 제공한다.
- 고민거리:
  - 트리거 정책을 수동(`workflow_dispatch`) 중심으로 둘지, push/PR 자동 빌드를 병행할지

## 문제 정의
- 해결 문제:
  - Windows 빌드 머신이 없는 개발자가 `AIUsageWatcher.exe` 산출물을 즉시 확보할 수 없다.
- 비목표:
  - 코드서명 자동화
  - GitHub Release 태깅/업로드 자동화
  - 실기기 스모크 테스트 자동화

## 구현 단위 (Coding 실행 단위)
- 작업 A: Windows CI 빌드 워크플로 추가
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/.github/workflows/windows-exe-build.yml
  - 구현 상세:
    - `windows-latest` 러너에서 checkout 후 PowerShell로 `desktop_win/scripts/build_windows_bundle.ps1` 실행
    - 결과물 경로 `desktop_win/dist/AIUsageWatcher/` 존재를 검증
    - `AIUsageWatcher.exe` SHA-256 파일 생성 후 번들/체크섬을 artifact로 업로드
  - 테스트:
    - 로컬 정적 검토(`git diff`, YAML key 구조 점검)
    - GitHub Actions 수동 실행(`workflow_dispatch`) 성공 여부 확인

- 작업 B: 운영 문서에 CI 빌드 경로 반영
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
  - 구현 상세:
    - 로컬 Windows 빌드가 어려운 경우 GitHub Actions artifact를 다운로드하는 절차를 추가
  - 테스트:
    - 문서 절차와 워크플로 artifact 이름/경로 정합성 확인

## 테스트 설계
- 기능 테스트:
  - GitHub Actions `Windows EXE Build` 수동 실행 시 artifact(`AIUsageWatcher-windows-bundle`)가 생성된다.
- 회귀 테스트:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py`
- 실패/예외 테스트:
  - 빌드 실패 시 job 로그에서 `build_windows_bundle.ps1` 오류가 명확히 노출된다.
  - `AIUsageWatcher.exe` 누락 시 checksum 단계에서 즉시 실패한다.

## 리스크 및 대응
- 리스크:
  - CI 캐시 미사용 시 빌드 시간이 길어질 수 있음
  - 대응:
    - 초기 버전은 단순성 우선, 필요 시 pip 캐시를 후속 최적화로 추가
- 리스크:
  - GitHub Actions 권한/분 제한으로 빌드가 지연될 수 있음
  - 대응:
    - 수동 워크플로 + 로컬 Windows 빌드(백업 경로) 병행 안내

## 완료 조건 (Definition of Done)
- DoD 1:
  - `windows-latest`에서 `desktop_win/scripts/build_windows_bundle.ps1`가 실행된다.
- DoD 2:
  - `desktop_win/dist/AIUsageWatcher/AIUsageWatcher.exe`와 SHA-256 파일이 artifact에 포함된다.
- DoD 3:
  - 운영 문서에 CI 빌드/다운로드 절차가 반영된다.
- DoD 4:
  - 기존 Python 테스트가 회귀 없이 통과한다.

## Handoff
- To Coding:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- To Integration Test (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
- To Cycle Manager (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
