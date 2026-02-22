# Coding

## Subject
- ai-usage-windows-watcher

## Latest Handoff
- from_task:
  - phase1-windows-exe-build-artifact-delivery
- source:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-exe-build-artifact-delivery.md
- status:
  - completed

## Coding Update (2026-02-18 16:20)
- code_repository:
  - git@github.com:HeeyongPark/ai-usage-windows-watcher.git
- local_path:
  - /Users/mirador/Documents/ai-usage-windows-watcher

### 변경 파일
- /Users/mirador/Documents/ai-usage-windows-watcher/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/.gitignore
- /Users/mirador/Documents/ai-usage-windows-watcher/agent/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/agent/requirements.txt
- /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/config.py
- /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/collector.py
- /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/storage.py
- /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/cli.py
- /Users/mirador/Documents/ai-usage-windows-watcher/agent/sql/schema.sql
- /Users/mirador/Documents/ai-usage-windows-watcher/agent/tests/test_cli.py

### 구현 요약
- agent MVP 골격(수집 이벤트 모델, SQLite 저장, 일별 요약 CLI)을 생성했다.
- `record-sample` 실행 시 외래키 오류를 수정해 세션 선저장 -> 이벤트 저장 순서로 고정했다.

### 검증 증적
- 실행 커맨드:
  - `python src/cli.py init-db`
  - `python src/cli.py record-sample --tool codex --requests 3 --tokens 1200`
  - `python src/cli.py summary --daily`
  - `pytest -q`
- 결과:
  - summary 출력 정상
  - 테스트 1건 통과 (`1 passed`)

### 다음 핸드오프
- To Review:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Coding Update (2026-02-18 21:38)
- from_task:
  - phase1-desktop-dashboard
- scope_update:
  - Codex 사용량 대시보드 일/주 집계 분리
- 구현 전략:
  - 저장소/서비스 계층에 주간 집계 API 추가
  - UI를 Notebook 탭 구조로 전환해 일/주 보기를 분리

### 변경 파일
- /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/storage.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_usage_service.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md

### 구현 요약
- `list_weekly_summary`/`codex_weekly_summary`를 추가해 주차 단위 집계를 제공했다.
- 대시보드에서 일별/주별 표를 탭으로 분리해 운영자가 추세를 빠르게 확인할 수 있게 했다.

### 검증 증적
- 실행 커맨드:
  - `python3 -m py_compile agent/src/*.py desktop_win/src/*.py`
  - `python3 - <<'PY' ... insert_codex_sample_session/codex_daily_summary/codex_weekly_summary ... PY`
- 결과:
  - 정적 컴파일 통과
  - 샘플 데이터 기준 `daily_rows=1`, `weekly_rows=1` 확인
  - `pytest`는 로컬 환경 미설치(`No module named pytest`)로 미실행

### 다음 핸드오프
- To Review:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Coding Update (2026-02-18 21:39)
- from_task:
  - phase1-budget-alert-rule
- scope_update:
  - 토큰 기반 예산 임계치 알림 규칙 도입
- 구현 전략:
  - 예산 설정/판정을 UI와 분리한 `budget_rules` 모듈 신설
  - 대시보드 갱신 시 일/주 토큰 집계로 상태(`normal/warning/critical`) 계산

### 변경 파일
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/budget_rules.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_budget_rules.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/.env.example
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- /Users/mirador/Documents/ai-usage-windows-watcher/README.md

### 구현 요약
- 환경변수 기반 예산 설정(`AUIW_DAILY_TOKEN_BUDGET`, `AUIW_WEEKLY_TOKEN_BUDGET`, `AUIW_ALERT_THRESHOLD_PCT`)을 추가했다.
- 대시보드에 예산 상태/상세 패널을 추가해 사용량 초과 위험을 즉시 확인 가능하게 했다.

### 검증 증적
- 실행 커맨드:
  - `python3 -m py_compile agent/src/*.py desktop_win/src/*.py`
  - `python3 - <<'PY' ... evaluate_budget_alert ... PY`
- 결과:
  - 정적 컴파일 통과
  - 샘플 데이터 기준 `alert_level=normal` 계산 확인
  - `pytest`는 로컬 환경 미설치(`No module named pytest`)로 미실행

### 다음 핸드오프
- To Review:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Coding Update (2026-02-18 16:31)
- scope_update:
  - Windows 사용법 문서화
  - 5인치 모니터 기본 전체화면 UI 적용
- 구현 전략:
  - 앱 시작 시 기본 fullscreen, F11/Esc 단축키 제공
  - 작은 해상도에서 요약 영역을 세로 배치해 가독성 확보
  - `desktop_win/.env` 자동 로드로 설정 절차 단순화

### 변경 파일
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_env_loader.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md

### 구현 요약
- UI를 기본 전체화면 시작으로 변경하고 소형 화면(<=1024x768) 자동 컴팩트 레이아웃을 적용했다.
- Windows 운영자를 위한 PowerShell 중심 사용 가이드를 추가했다.
- 앱 실행 시 `desktop_win/.env`를 자동으로 읽어 OAuth 설정 주입을 단순화했다.

### 검증 증적
- 실행 커맨드:
  - `python -m py_compile desktop_win/src/*.py agent/src/*.py`
  - `pytest -q`
- 결과:
  - 정적 컴파일 통과
  - 테스트 4건 통과 (`4 passed`)

### 다음 핸드오프
- To Review:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Coding Update (2026-02-18 16:33)
- scope_update:
  - 데이터 자동 갱신 주기 1시간 적용
- 구현 전략:
  - 앱 시작 시 자동 새로고침 스케줄러 등록
  - 기본값 3600초, 최소 60초 가드
  - 화면에 `최근 갱신`, `자동 갱신` 텍스트 표시

### 변경 파일
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/.env.example
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_refresh_interval.py

### 구현 요약
- 기본 자동 갱신을 1시간 주기로 적용하고 수동 새로고침 버튼은 유지했다.
- `.env`에서 `AUIW_REFRESH_INTERVAL_SEC`로 주기 조정 가능하게 구성했다.

### 검증 증적
- 실행 커맨드:
  - `python -m py_compile desktop_win/src/*.py agent/src/*.py`
  - `pytest -q`
- 결과:
  - 정적 컴파일 통과
  - 테스트 6건 통과 (`6 passed`)

### 다음 핸드오프
- To Review:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Coding Update (2026-02-18 16:32)
- scope_update:
  - Codex 사용량 UI 우선 제공 + OAuth 최초 로그인 요구 반영
- 구현 전략:
  - Windows MVP는 Tkinter 데스크톱 앱으로 구현
  - OAuth는 provider 독립적인 PKCE 클라이언트로 구성

### 변경 파일
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/oauth_client.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/paths.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/.env.example
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_oauth_client.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_usage_service.py
- /Users/mirador/Documents/ai-usage-windows-watcher/README.md

### 구현 요약
- 데스크톱 대시보드에서 Codex 일별 사용량(세션/요청/토큰)을 즉시 조회 가능하게 구성했다.
- OAuth 로그인 버튼을 통해 Authorization Code + PKCE 흐름을 수행하고 토큰을 로컬에 저장하도록 구현했다.
- 샘플 Codex 세션 생성 버튼으로 초기 데모 데이터를 빠르게 확인할 수 있게 했다.

### 검증 증적
- 실행 커맨드:
  - `python -m py_compile desktop_win/src/*.py agent/src/*.py`
  - `pytest -q`
- 결과:
  - 정적 컴파일 통과
  - 테스트 3건 통과 (`3 passed`)

### 다음 핸드오프
- To Review:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Coding Update (2026-02-18 22:57)
- from_task:
  - phase1-windows-runtime-smoke
- scope_update:
  - Windows 실기기 스모크 검증 표준화
- 구현 전략:
  - 수동 체크리스트/증적 템플릿을 저장소 표준으로 추가
  - PowerShell 런타임 프로브 스크립트로 환경 증적 수집 자동화
  - Windows 운영 가이드에 스모크 게이트 절차를 반영

### 변경 파일
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md

### 구현 요약
- Win10/Win11 공통 필수 시나리오 6개를 체크리스트로 고정했다.
- `windows_runtime_probe.ps1`로 OS/Python/해상도/저장 경로 정보를 JSON으로 추출 가능하게 했다.
- 운영 문서에 Gate A/B/C 실행 절차와 증적 경로를 반영했다.

### 검증 증적
- 실행 커맨드:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/tests/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/*.py`
- 결과:
  - `9 passed`
  - py_compile 오류 없음
- 제한:
  - PowerShell 스크립트의 실기기 실행 검증은 Windows 머신에서 수행 필요

### 다음 핸드오프
- To Review:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 28 (2026-02-18 23:39)

## 입력 요약
- from_task:
  - phase1-windows-noinstall-bundle
- planning source:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-noinstall-bundle.md
- 사용자 결정:
  - onefile 제외, onedir 배포만 지원

## 설계 개요
- Windows 빌드 머신에서 PyInstaller onedir 결과물을 생성하는 스크립트를 추가한다.
- 번들 폴더에서 더블클릭 실행 가능한 런처 배치 파일을 추가한다.
- 번들 런타임(`frozen`)에서도 agent 모듈/`.env`를 올바르게 찾도록 경로 해석 로직을 보강한다.
- 운영 문서와 실기기 체크리스트를 onedir 기준으로 갱신한다.

## 원칙 적용 체크
- KISS:
  - PyInstaller onedir + 단일 런처 `.bat` 조합으로 최소 경로를 제공
- YAGNI:
  - MSI/MSIX, onefile 최적화, 코드서명 자동화는 범위에서 제외
- DRY:
  - 경로 계산 로직을 `usage_service`/`env_loader`에 함수화
- SOLID:
  - 런타임 경로 결정 책임을 헬퍼 함수로 분리해 테스트 가능성 확보

## 작업 분해
- 작업 1:
  - `desktop_win/scripts/build_windows_bundle.ps1` 추가 (onedir 번들 빌드)
- 작업 2:
  - `desktop_win/scripts/run_ai_usage_watcher.bat` 추가 (무설치 실행 런처)
- 작업 3:
  - `desktop_win/src/usage_service.py`, `desktop_win/src/env_loader.py` 런타임 경로 보강
- 작업 4:
  - `desktop_win/README.md`, `desktop_win/WINDOWS_USAGE.md`, 수동 검증 문서 갱신
- 작업 5:
  - 테스트 보강 (`desktop_win/tests/test_usage_service.py`, `desktop_win/tests/test_env_loader.py`)

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/run_ai_usage_watcher.bat
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_usage_service.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_env_loader.py
- /Users/mirador/Documents/ai-usage-windows-watcher/.gitignore

## 의존성/통합 포인트
- 빌드 의존성:
  - `pyinstaller==6.11.1` (빌드 시점 설치)
- 런타임 통합:
  - onedir 번들 내부 `agent/src`, `agent/sql` 데이터 경로 사용
  - 번들 루트 `.env` 자동 로드

## 테스트 전략
- 자동:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py`
- 수동(Windows):
  - `build_windows_bundle.ps1` 실행 후 `dist\AIUsageWatcher\run_ai_usage_watcher.bat` 실행 확인
  - 무설치 런처/onedir 폴더 누락 실패 시나리오 확인

## 일정
- Coding 완료 후 즉시 Review 요청

## 리스크와 대응
- 리스크:
  - macOS 환경에서는 PowerShell 빌드 스크립트 실행 검증 불가
  - 대응:
    - Review에서 Windows 실행 증적 확보를 명시
- 리스크:
  - SmartScreen 경고로 사용자 혼란 가능
  - 대응:
    - 운영 가이드에 경고 대응 절차를 명시

## 오픈 이슈
- 코드서명/배포 해시 검증 자동화는 Phase 2로 이관

## Handoff To Review
- 검토 대상 범위:
  - onedir 번들 빌드/런처 경로, frozen 런타임 경로 안전성, 문서 정합성
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/run_ai_usage_watcher.bat
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py
- 테스트 결과/검증 포인트:
  - pytest/py_compile 결과
  - Windows 실기기에서 onedir 실행 증적 필요
- 잔여 리스크:
  - Windows 빌드/실행 실증 미첨부 시 조건부 판정 가능
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-noinstall-bundle.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 33 (2026-02-19 17:52)

## 입력 요약
- from_task:
  - phase1-windows-frozen-path-compat
- planning source:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-frozen-path-compat.md
- 목표:
  - frozen 런타임 경로 우선순위(`sys._MEIPASS` -> exe dir -> `_internal`)를 코드/빌드/문서에 일관되게 반영

## 설계 개요
- `usage_service`와 `env_loader`에 동일한 경로 후보 우선순위를 도입하고, 실제 파일 존재(`collector.py`, `.env`) 기반으로 최종 경로를 선택한다.
- 빌드 스크립트에서 PyInstaller onedir `--contents-directory "_internal"`을 명시해 산출물 구조를 고정한다.
- 런처에서 번들 레이아웃(flat/`_internal`)을 사전 검증해 실행 전 결함을 빠르게 안내한다.

## 원칙 적용 체크
- KISS:
  - 경로 후보 3개를 순서대로 평가하는 단순 규칙으로 구현
- YAGNI:
  - onefile/MSI/MSIX/코드서명 자동화는 범위에서 제외
- DRY:
  - 두 모듈에서 동일한 런타임 루트 탐색 패턴을 사용
- SOLID:
  - 경로 결정 함수를 분리해 단위 테스트에서 frozen 케이스를 직접 검증

## 작업 분해
- 작업 1:
  - `usage_service.py` frozen 경로 해석 로직 보강
- 작업 2:
  - `env_loader.py` `.env` 탐색 우선순위 보강
- 작업 3:
  - `_MEIPASS`/`_internal` 레이아웃 검증 테스트 추가
- 작업 4:
  - 빌드/런처 스크립트에 레이아웃 검증 및 안내 메시지 추가
- 작업 5:
  - README/WINDOWS_USAGE/증적 템플릿 정합성 갱신

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_usage_service.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_env_loader.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/run_ai_usage_watcher.bat
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md

## 의존성/통합 포인트
- 런타임:
  - frozen 경로에서 `agent/src/collector.py` 탐색 가능 여부
- 빌드:
  - PyInstaller onedir `_internal` 구조 고정
- 문서:
  - 운영자 가이드와 실제 런처 검증 기준 동기화

## 테스트 전략
- 자동:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/*.py`
- 수동(Windows):
  - `build_windows_bundle.ps1` 실행 후 레이아웃 출력 확인
  - `run_ai_usage_watcher.bat`로 번들 레이아웃 감지 메시지 확인

## 일정
- Coding 완료, 다음 단계 Review 요청

## 리스크와 대응
- 리스크:
  - macOS 환경에서는 PowerShell 스크립트 실실행 검증이 불가
  - 대응:
    - Windows 실기기에서 번들 빌드/런처 실행 증적을 Review 게이트로 요구
- 리스크:
  - Notion 문서와 로컬 운영 수치의 시점 차이
  - 대응:
    - Cycle/Planning 최신 문서를 기준으로 게이트 판단

## 오픈 이슈
- SmartScreen/백신 오탐 대응(코드서명)은 후속 태스크(`phase1-windows-noinstall-smoke-evidence`)에서 증적 기반으로 정리

## Handoff To Review
- 검토 대상 범위:
  - frozen 런타임 경로 선택 우선순위와 `_internal` 레이아웃 호환성
  - 빌드/런처 사전 검증 메시지의 운영 적합성
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/run_ai_usage_watcher.bat
- 테스트 결과/검증 포인트:
  - `15 passed`
  - py_compile 오류 없음
- 잔여 리스크:
  - Windows 실기기 번들 실행 증적은 아직 미첨부(후속 task)
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-frozen-path-compat.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 37 (2026-02-19 20:03)

## 입력 요약
- from_task:
  - phase1-windows-noinstall-smoke-evidence
- planning source:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-noinstall-smoke-evidence.md
- 목표:
  - Win10/Win11 실기기 스모크 증적 누락을 줄이기 위해 run-id 기반 증적 생성 흐름을 스크립트/문서에 반영

## 설계 개요
- 기존 `windows_runtime_probe.ps1`를 확장해 번들 메타데이터(레이아웃/핵심 파일 존재/sha256)를 함께 수집한다.
- 신규 `prepare_windows_smoke_evidence.ps1`를 추가해 증적 세트(runtime context/checklist/evidence)를 run-id 기준으로 자동 생성한다.
- 운영 문서/체크리스트/증적 템플릿을 run-id 기반 artifact 흐름으로 정렬한다.

## 원칙 적용 체크
- KISS:
  - 실기기에서 한 번의 스크립트 호출로 증적 기본 세트를 생성
- YAGNI:
  - 수동 시나리오 자체 자동화는 제외하고 증적 생성 보조에 집중
- DRY:
  - 경로 해석 유틸리티를 PowerShell 스크립트 내 공통 함수로 재사용
- SOLID:
  - 런타임 수집(`probe`)과 증적 패키징(`prepare`) 책임을 분리

## 작업 분해
- 작업 1:
  - `desktop_win/scripts/windows_runtime_probe.ps1` 메타데이터 확장
- 작업 2:
  - `desktop_win/scripts/prepare_windows_smoke_evidence.ps1` 신규 추가
- 작업 3:
  - 체크리스트/증적 템플릿 run-id 필드 보강
- 작업 4:
  - Windows 운영 문서와 README에 실행 절차 반영

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md

## 의존성/통합 포인트
- PowerShell 실행 환경:
  - Windows 실기기에서 `prepare_windows_smoke_evidence.ps1` 실행 필요
- 기존 런타임 점검 흐름:
  - `windows_runtime_probe.ps1`를 단독 실행/패키지 실행 모두 지원

## 테스트 전략
- 자동:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/*.py`
- 수동(Windows):
  - `prepare_windows_smoke_evidence.ps1` 실행 후 artifact 3종 생성 확인

## 일정
- Coding 완료, 다음 단계 Review 요청

## 리스크와 대응
- 리스크:
  - 현재 개발 환경(macOS)에서는 PowerShell 실실행 검증 불가
  - 대응:
    - Review에서 Win10/Win11 실기기 실행 증적을 필수 게이트로 유지

## 오픈 이슈
- SmartScreen/백신 경고 대응의 운영 문구 확정은 실기기 증적 확보 후 후속 정리

## Handoff To Review
- 검토 대상 범위:
  - 증적 수집 자동화 스크립트 품질과 문서 정합성
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- 테스트 결과/검증 포인트:
  - `15 passed`
  - py_compile 오류 없음
  - `pwsh not found`로 로컬 PowerShell 실행 검증은 미수행
- 잔여 리스크:
  - Win10/Win11 실기기 artifact 미첨부
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-noinstall-smoke-evidence.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 40 (2026-02-19 21:57)

## 입력 요약
- from_task:
  - phase1-windows-noinstall-smoke-evidence
- planning source:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-noinstall-smoke-evidence.md
- 목표:
  - 저장소 경로 없이 onedir 번들 폴더만으로 run-id 증적 세트를 생성할 수 있게 증적 수집 UX를 보강한다.

## 설계 개요
- `prepare_windows_smoke_evidence.ps1`/`windows_runtime_probe.ps1`를 repo 모드 + bundle 단독 모드 모두 지원하도록 확장한다.
- 번들 루트에서 더블클릭 가능한 `collect_windows_smoke_evidence.bat`를 추가해 PowerShell 명령 입력 부담을 제거한다.
- 번들 빌드 시 증적 스크립트/템플릿을 함께 복사해 운영자가 추가 파일 없이 실행할 수 있게 한다.

## 원칙 적용 체크
- KISS:
  - 번들 루트에서 `collect_windows_smoke_evidence.bat` 1회 실행으로 기본 증적 세트 생성
- YAGNI:
  - 수동 시나리오(로그인/데이터 확인) 자체 자동화는 제외
- DRY:
  - 경로 해석 함수를 PowerShell 스크립트 공통 패턴으로 정리
- SOLID:
  - 런타임 탐지/컨텍스트 수집(`probe`)과 증적 패키징(`prepare`) 책임 분리 유지

## 작업 분해
- 작업 1:
  - `prepare_windows_smoke_evidence.ps1`의 템플릿/출력 경로를 bundle 모드까지 확장
- 작업 2:
  - `windows_runtime_probe.ps1`에 bundle 모드 기본 경로(`smoke_evidence/artifacts`)와 번들 메타데이터 수집 유지
- 작업 3:
  - `collect_windows_smoke_evidence.bat` 신규 추가(원클릭 증적 수집)
- 작업 4:
  - `build_windows_bundle.ps1`에서 증적 스크립트/템플릿을 번들에 동봉
- 작업 5:
  - `README.md`, `WINDOWS_USAGE.md`, 증적 템플릿의 실행 경로 안내 갱신

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/collect_windows_smoke_evidence.bat
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md

## 의존성/통합 포인트
- Windows onedir 번들:
  - `collect_windows_smoke_evidence.bat` -> `prepare_windows_smoke_evidence.ps1` -> `windows_runtime_probe.ps1` 체인
- artifact 경로:
  - 번들 모드: `smoke_evidence/artifacts/*`
  - 저장소 모드: `tests/manual/artifacts/*`

## 테스트 전략
- 자동:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/tests/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/*.py`
- 수동(Windows):
  - `dist\AIUsageWatcher\collect_windows_smoke_evidence.bat` 실행 후 artifact 3종 생성 확인

## 일정
- Coding 완료, 다음 단계 Review 요청

## 리스크와 대응
- 리스크:
  - macOS 환경에서는 PowerShell 스크립트 실실행 검증이 불가
  - 대응:
    - Integration Test (Pre)에서 Win10/Win11 실기기 artifact 첨부를 게이트로 유지
- 리스크:
  - 번들만 전달받은 운영자가 run-id 네이밍 규칙을 생략할 가능성
  - 대응:
    - 스크립트 기본 run-id 자동 생성 + 문서에 수동 지정 예시 병기

## 오픈 이슈
- SmartScreen/코드서명 정책은 실기기 배포 피드백 수집 후 후속 태스크로 분리

## Handoff To Review
- 검토 대상 범위:
  - 번들 단독 증적 수집 흐름의 경로 해석/실행 가능성
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/collect_windows_smoke_evidence.bat
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
- 테스트 결과/검증 포인트:
  - `15 passed in 0.09s`
  - py_compile 오류 없음
- 잔여 리스크:
  - Windows 실기기에서 번들 스크립트 실행 증적 미첨부
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-noinstall-smoke-evidence.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 45 (2026-02-19 23:37)

## 입력 요약
- from_task:
  - phase1-windows-exe-build-artifact-delivery
- planning source:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-exe-build-artifact-delivery.md
- 목표:
  - Windows 머신 없이도 GitHub Actions에서 `AIUsageWatcher.exe` 번들을 생성/전달 가능한 경로를 고정한다.

## 설계 개요
- GitHub Actions `windows-latest`에서 기존 공식 빌드 스크립트(`build_windows_bundle.ps1`)를 그대로 실행한다.
- CI 단계에서 `AIUsageWatcher.exe` 존재를 검증하고 SHA-256 파일을 생성해 artifact에 동봉한다.
- 운영 문서에 수동 실행 경로(`workflow_dispatch`)와 artifact 확인 절차를 추가한다.

## 원칙 적용 체크
- KISS:
  - 신규 스크립트 작성 없이 기존 빌드 스크립트를 재사용
- YAGNI:
  - Release asset 업로드/코드서명 자동화는 제외
- DRY:
  - 로컬/CI 모두 `desktop_win/scripts/build_windows_bundle.ps1` 단일 진입점 사용
- SOLID:
  - 빌드(job), 체크섬 생성(step), 전달(artifact upload) 책임을 단계별로 분리

## 작업 분해
- 작업 1:
  - `.github/workflows/windows-exe-build.yml` 추가
- 작업 2:
  - `desktop_win/README.md`에 CI 빌드/다운로드 절차 추가
- 작업 3:
  - 회귀 테스트(`pytest`, `py_compile`) 실행 및 증적 기록

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/.github/workflows/windows-exe-build.yml
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md

## 의존성/통합 포인트
- GitHub Actions:
  - `actions/checkout@v4`
  - `actions/setup-python@v5`
  - `actions/upload-artifact@v4`
- Windows 빌드 스크립트:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1`

## 테스트 전략
- 자동:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py`
- 수동/원격:
  - GitHub Actions `Windows EXE Build`를 `workflow_dispatch`로 실행 후 artifact 생성 확인

## 일정
- Coding 완료, 다음 단계 Review 요청

## 리스크와 대응
- 리스크:
  - 로컬 환경에 `actionlint`가 없어 워크플로 정적 검증 도구 기반 확인이 제한된다.
  - 대응:
    - GitHub Actions 실제 실행 결과를 1차 판정 기준으로 사용
- 리스크:
  - CI 빌드 시간이 상대적으로 길 수 있음
  - 대응:
    - 초기 버전은 단순 구성 유지, 필요 시 cache 최적화를 후속 반영

## 오픈 이슈
- 코드서명/Release asset 업로드는 현재 범위 밖이며 후속 태스크로 분리 필요

## Handoff To Review
- 검토 대상 범위:
  - Windows CI 빌드 워크플로가 Planning DoD를 충족하는지
  - README 절차와 artifact 이름/경로 정합성
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/.github/workflows/windows-exe-build.yml
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- 테스트 결과/검증 포인트:
  - `15 passed in 0.09s`
  - py_compile 오류 없음
  - `actionlint not found`
- 잔여 리스크:
  - GitHub Actions 원격 실행 증적(첫 성공 run) 미첨부
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-exe-build-artifact-delivery.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 46 (2026-02-20 09:21)

## 입력 요약
- from_task:
  - phase1-windows-exe-build-artifact-delivery
- 실패 증적:
  - GitHub Actions `Windows EXE Build` run `#8` (`22192393163`) failure
  - failure annotation: `Bundle sqlite stdlib missing: sqlite3/__init__.pyc was not found in base_library.zip.`
- 목표:
  - `_sqlite3` fallback 설계와 빌드 검증 규칙을 일치시켜 CI false-negative를 제거한다.

## 설계 개요
- `base_library.zip` 내 `sqlite3` stdlib 누락을 hard fail에서 warning으로 전환한다.
- `_sqlite3.pyd` 존재 검증은 기존 guardrail을 유지해 실제 런타임 누락은 계속 차단한다.

## 원칙 적용 체크
- KISS:
  - 실패 조건 1개만 정밀 조정하고 기존 빌드 플로우는 유지
- YAGNI:
  - sqlite 번들 방식 재설계 없이 검증 기준만 보정
- DRY:
  - 기존 검증 루틴 재사용(새 함수 추가 없음)
- SOLID:
  - 런타임 바이너리 존재 검증과 stdlib 보조 검증 책임을 분리

## 작업 분해
- 작업 1:
  - `desktop_win/scripts/build_windows_bundle.ps1` sqlite stdlib 검증 분기 수정
- 작업 2:
  - 로컬 회귀 테스트 실행
- 작업 3:
  - 원격 Actions 재실행 결과 확인

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1

## 테스트 전략
- 자동:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/tests/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/*.py`
- 원격:
  - GitHub Actions `Windows EXE Build` run `#9` (`22205898127`) 성공 확인

## 일정
- Coding 완료, 다음 단계 Review 요청

## 리스크와 대응
- 리스크:
  - stdlib 부재를 warning으로 바꾸면 잠재 오류를 놓칠 수 있음
  - 대응:
    - `_sqlite3.pyd` 필수 검증은 계속 유지하고 runtime fallback 테스트를 별도 유지

## Handoff To Review
- 검토 대상 범위:
  - sqlite stdlib 누락 시 fallback 정책과 빌드 검증 규칙 정합성
  - 원격 CI(run `#9`) 성공 여부
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
- 테스트 결과/검증 포인트:
  - `16 passed in 0.09s`
  - py_compile 오류 없음
  - Actions run `#9` success + artifact 생성 확인
- 잔여 리스크:
  - Windows 실기기 수동 스모크는 권장 항목으로 별도 유지
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-exe-build-artifact-delivery.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/.github/workflows/windows-exe-build.yml
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 47 (2026-02-20 10:24)

## 입력 요약
- from_task:
  - phase1-windows-noinstall-smoke-evidence
- 사용자 오류 제보:
  - `prepare_windows_smoke_evidence.ps1` Markdown 치환 줄에서 PowerShell parser error
  - `windows_runtime_probe.ps1` `IsPathRooted` 호출 중 `경로에 잘못된 문자가 있습니다.`
- 목표:
  - bundle 단독 실행 경로 입력을 방어적으로 정규화하고, 증적 치환 문자열 구문 오류를 제거한다.

## 설계 개요
- 경로 입력 정규화(`Normalize-PathInput`)를 공통으로 적용해 제어문자/래핑 따옴표를 제거한다.
- `IsPathRooted`/`GetFullPath`를 `try/catch`로 감싸 실패 시 원인 포함 메시지를 남긴다.
- 백틱을 포함하는 문자열은 single-quoted format 표현식으로 치환해 파서 충돌을 방지한다.

## 원칙 적용 체크
- KISS:
  - 스크립트 2개에 동일 패턴의 최소 보강만 반영
- YAGNI:
  - 신규 의존성/템플릿 구조 변경 없이 기존 흐름 유지
- DRY:
  - 경로 정규화 함수 재사용
- SOLID:
  - 경로 정규화 책임과 실제 프로브/증적 생성 책임 분리

## 작업 분해
- 작업 1:
  - `prepare_windows_smoke_evidence.ps1` 포맷 문자열/경로 정규화 보강
- 작업 2:
  - `windows_runtime_probe.ps1` 경로 정규화 보강
- 작업 3:
  - 로컬 회귀 테스트 + GitHub Actions 원격 빌드 재검증

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1

## 테스트 전략
- 자동:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/tests/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/*.py`
- 원격:
  - GitHub Actions `Windows EXE Build` run `#10` (`22206380280`) success
  - GitHub Actions `Windows EXE Build` run `#11` (`22207320762`) success

## 일정
- Coding 완료, 다음 단계 Review 요청

## 리스크와 대응
- 리스크:
  - 사용자 PC에 남아 있는 구버전 `dist`를 실행하면 동일 오류가 재현될 수 있음
  - 대응:
    - 최신 commit(`42c7a80`) 기준으로 bundle 재생성 또는 최신 artifact 재다운로드 안내

## Handoff To Review
- 검토 대상 범위:
  - 경로 정규화 보강이 bundle 단독 실행 경로에 안전하게 적용됐는지
  - run `#10/#11` 성공 및 artifact 생성 정합성
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
- 테스트 결과/검증 포인트:
  - `16 passed in 0.09s`
  - py_compile 오류 없음
  - Actions run `#10`, `#11` success + artifact 생성 확인
- 잔여 리스크:
  - 기존 로컬 dist 캐시를 지우지 않으면 구버전 스크립트가 실행될 수 있음
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-noinstall-smoke-evidence.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 48 (2026-02-22 22:55)

## 입력 요약
- from_task:
  - phase1-desktop-dashboard (hotfix addendum)
- 사용자 오류 제보:
  - `_tkinter.TclError: expected integer but got "UI"`
- 목표:
  - Tkinter 기본 폰트 설정의 파싱 오류를 제거해 앱 초기화 크래시를 해결한다.

## 설계 개요
- Tk `option_add("*Font", ...)`에 공백 패밀리명을 안전하게 전달하기 위한 헬퍼 `_font_option_value(size)`를 추가한다.
- 반환 포맷을 `"{Segoe UI} {size}"`로 고정해 Tk 폰트 파서가 패밀리/크기를 정확히 구분하게 한다.

## 원칙 적용 체크
- KISS:
  - 폰트 옵션 문자열 포맷만 수정하고 레이아웃 구조는 유지
- YAGNI:
  - 테마 시스템 재구성 없이 오류 원인 구간만 국소 수정
- DRY:
  - compact/normal 모드가 동일 헬퍼를 재사용
- SOLID:
  - 폰트 문자열 생성 책임을 헬퍼로 분리

## 작업 분해
- 작업 1:
  - `desktop_win/src/app.py`에 `_font_option_value` 추가 및 `option_add` 호출부 교체
- 작업 2:
  - `desktop_win/tests/test_refresh_interval.py`에 폰트 스펙 회귀 테스트 추가
- 작업 3:
  - py_compile + pytest 실행으로 회귀 검증

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_refresh_interval.py

## 의존성/통합 포인트
- Tkinter `option_add` 폰트 스펙 파싱 규칙
- 기존 대시보드 UI 컴포넌트 생성 흐름(`LabelFrame`, `Notebook`, `Treeview`)

## 테스트 전략
- 자동:
  - `python3 -m py_compile desktop_win/src/*.py desktop_win/tests/*.py`
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q desktop_win/tests`
- 수동:
  - Windows 런타임에서 앱 실행 후 초기 화면 진입 확인(다음 단계 권장)

## 일정
- Coding 완료, 다음 단계 Review 요청

## 리스크와 대응
- 리스크:
  - 폰트 미설치 환경에서 대체 폰트로 렌더링 차이가 발생할 수 있음
  - 대응:
    - 본 수정은 파싱 크래시 제거에 집중하고, 폰트 fallback 정책은 별도 개선 태스크로 분리

## 오픈 이슈
- 없음(이번 hotfix 범위 내)

## Handoff To Review
- 검토 대상 범위:
  - 폰트 문자열 변경이 실제 traceback 원인을 해소하는지
  - compact/normal 모드 양쪽에서 동일하게 적용되는지
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_refresh_interval.py
- 테스트 결과/검증 포인트:
  - `15 passed in 0.12s`
  - py_compile 오류 없음
- 잔여 리스크:
  - Windows 실기기 시각적 폰트 fallback 차이는 미확인
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-desktop-dashboard.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 49 (2026-02-22 23:21)

## 입력 요약
- from_task:
  - phase1-win-agent-usage-collector (OAuth Browser Policy update)
- 사용자 요구:
  - OAuth 로그인을 Chrome에서 진행하는지 확인하고, Planning/Coding/Review 후 push까지 완료
- 목표:
  - OAuth 브라우저 실행 정책을 명시적으로 제어하고 기본값을 Chrome 우선으로 설정

## 설계 개요
- `oauth_client._open_auth_page()`에서 브라우저 모드를 환경변수로 해석한다.
- 기본 정책은 `chrome`으로 두고, Chrome 실행 실패 시 기본 브라우저 fallback을 허용한다.
- `chrome_only` 모드에서는 fallback 없이 즉시 실패해 운영자가 정책 위반을 바로 인지할 수 있게 한다.

## 원칙 적용 체크
- KISS:
  - 기존 OAuth 플로우(auth URL 생성/콜백/토큰교환)는 유지, 브라우저 오픈 정책만 분리
- YAGNI:
  - 외부 라이브러리 추가 없이 표준 라이브러리(`subprocess`, `webbrowser`)로 해결
- DRY:
  - 브라우저 모드/Chrome 후보 탐색을 helper 함수로 분리
- SOLID:
  - 인증 로직과 브라우저 실행 정책 책임을 분리

## 작업 분해
- 작업 1:
  - `desktop_win/src/oauth_client.py`에 브라우저 정책 helper 추가
- 작업 2:
  - `desktop_win/tests/test_oauth_client.py`에 모드별 회귀 테스트 추가
- 작업 3:
  - `desktop_win/README.md` OAuth 환경변수 문서 업데이트
- 작업 4:
  - py_compile + pytest 검증

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/oauth_client.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_oauth_client.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md

## 의존성/통합 포인트
- Python stdlib:
  - `subprocess.Popen` (Chrome 실행)
  - `webbrowser.open` (fallback)
- OAuth 기존 플로우:
  - `OAuthPKCEClient.authenticate()` 내 auth URL 오픈 단계

## 테스트 전략
- 자동:
  - `python3 -m py_compile desktop_win/src/*.py desktop_win/tests/*.py`
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q desktop_win/tests`
- 수동:
  - Windows 실기기에서 `AUIW_OAUTH_BROWSER` 값별 동작 확인 권장

## 일정
- Coding 완료, 다음 단계 Review 요청

## 리스크와 대응
- 리스크:
  - 사용자 PC에서 Chrome 경로 자동 탐색이 실패할 수 있음
  - 대응:
    - `AUIW_CHROME_PATH` 환경변수로 절대경로 강제 지정 경로 제공

## 오픈 이슈
- 없음(현재 범위 내)

## Handoff To Review
- 검토 대상 범위:
  - OAuth 브라우저 정책이 요구사항(Chrome 우선)과 일치하는지
  - 모드별 동작(`chrome/chrome_only/default`)이 테스트로 보장되는지
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/oauth_client.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_oauth_client.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- 테스트 결과/검증 포인트:
  - `21 passed in 0.10s`
  - py_compile 오류 없음
- 잔여 리스크:
  - Windows 실기기에서 실제 설치 경로 편차 확인 필요
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-win-agent-usage-collector.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md

## Cycle 50 (2026-02-22 23:41)

## 입력 요약
- from_task:
  - phase1-win-agent-usage-collector (Codex CLI Auth Bridge)
- 사용자 요구:
  - OpenClaw처럼 ChatGPT OAuth(Codex) 승인 플로우를 쓰고, 해당 사용량을 대시보드로 확인
- 목표:
  - 기존 일반 OAuth(PKCE custom endpoint) 대신 Codex CLI 인증 상태 재사용 방식으로 로그인 UX 전환

## 설계 개요
- 신규 모듈 `codex_auth.py`를 추가해 Codex CLI 명령을 캡슐화한다.
  - 상태 조회: `codex login status`
  - 로그인 실행: `codex login --device-auth`
- 앱 로그인 버튼은 위 모듈을 비동기 호출해 UI를 갱신한다.
- `.env`의 OAuth 필수값 의존을 제거하고, Codex CLI 준비/로그인 절차를 문서로 안내한다.

## 원칙 적용 체크
- KISS:
  - 기존 대시보드/집계 로직은 유지, 인증 경로만 교체
- YAGNI:
  - OpenAI 비공개 OAuth endpoint 추정 구현 없이 공식 CLI 플로우 재사용
- DRY:
  - Codex CLI 실행/출력 파싱 로직을 `codex_auth.py`로 단일화
- SOLID:
  - 인증 명령 실행 책임(app 분리)과 UI 갱신 책임(app 유지) 분리

## 작업 분해
- 작업 1:
  - `desktop_win/src/codex_auth.py` 추가 (status/device-auth/timeout 처리)
- 작업 2:
  - `desktop_win/src/app.py` 로그인 버튼 흐름을 Codex CLI 기반으로 교체
- 작업 3:
  - 테스트 추가/수정 (`test_codex_auth.py`, `test_refresh_interval.py`)
- 작업 4:
  - 운영 문서/설정 파일 업데이트 (`README`, `WINDOWS_USAGE`, `.env.example`)

## 변경 파일/모듈
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/codex_auth.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_codex_auth.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_refresh_interval.py
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/.env.example
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md

## 의존성/통합 포인트
- Codex CLI executable (`codex`) 설치 여부
- CLI 출력 문자열(`Logged in using ...`, `Not logged in`) 파싱
- Tkinter 비동기 UI 큐 업데이트

## 테스트 전략
- 자동:
  - `python3 -m py_compile desktop_win/src/*.py desktop_win/tests/*.py`
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q desktop_win/tests`
- 수동:
  - Windows에서 `codex login --device-auth` 이후 앱 `Codex 로그인` 버튼 동작 확인

## 일정
- Coding 완료, 다음 단계 Review 요청

## 리스크와 대응
- 리스크:
  - Windows 번들 환경에서 `codex` CLI가 PATH에 없으면 로그인 실패
  - 대응:
    - 명시적 오류 메시지로 안내하고, 사전 설치/로그인 절차를 문서화
- 리스크:
  - CLI 출력 포맷이 바뀌면 상태 파싱이 흔들릴 수 있음
  - 대응:
    - 실패 시 raw output을 그대로 사용자 오류창에 전달

## 오픈 이슈
- 없음(현재 범위 내)

## Handoff To Review
- 검토 대상 범위:
  - OpenClaw 유사 흐름(Codex CLI auth bridge) 요구사항 충족 여부
  - 테스트/문서/앱 동작의 정합성
- 핵심 변경 파일/모듈:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/codex_auth.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_codex_auth.py
- 테스트 결과/검증 포인트:
  - `28 passed in 0.13s`
  - py_compile 오류 없음
- 잔여 리스크:
  - 실사용 Windows 환경의 Codex CLI 설치 경로/PATH 편차
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-win-agent-usage-collector.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
- 출력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md
