# Coding

## Subject
- ai-usage-windows-watcher

## Latest Handoff
- from_task:
  - phase1-win-agent-usage-collector
- source:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-win-agent-usage-collector.md
- status:
  - in_progress

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
