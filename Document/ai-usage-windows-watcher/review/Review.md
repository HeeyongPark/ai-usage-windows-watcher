# Review

## Subject
- ai-usage-windows-watcher

## Latest Review
- status:
  - completed_up_to_review

## Review Request (2026-02-18 16:32)
- 대상 태스크:
  - phase1-win-agent-usage-collector
- 검토 범위:
  - Windows UI(Tkinter) Codex usage dashboard
  - OAuth PKCE 로그인 흐름
  - 로컬 SQLite 연동 및 요약 표시
- 핵심 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/oauth_client.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py

## Review Request (2026-02-18 16:31)
- 대상 태스크:
  - phase1-win-agent-usage-collector
- 검토 범위:
  - 5인치 화면 대응(fullscreen 기본 + compact layout)
  - Windows 사용법 문서 신설
  - `.env` 자동 로드 안정성
- 핵심 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md

## Review Request (2026-02-18 16:33)
- 대상 태스크:
  - phase1-win-agent-usage-collector
- 검토 범위:
  - 1시간 자동 갱신 스케줄러 동작
  - 주기 설정 환경변수/최소값 가드
  - 운영 문서와 실제 동작 정합성
- 핵심 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_refresh_interval.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md

## Review Result (2026-02-18 21:40) - phase1-win-agent-usage-collector

### 검토 범위
- Planning/Coding 산출물 정합성
- agent 수집/저장/조회 흐름
- desktop_win OAuth + 1시간 자동 갱신 반영 상태

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(요구된 수집기/대시보드/OAuth/갱신 주기 항목 반영 확인)
- Coding -> Planning 역추적 불가 항목:
  - 없음(모든 변경이 Planning 업데이트 항목으로 추적 가능)

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(로컬 수집/요약 조회/UI 확인 흐름 존재)
- 성능/리소스 병목 가능성:
  - 중간(자동 새로고침 주기 고정, 데이터 증가 시 조회비용 점검 필요)
- 오류 처리/예외 케이스 누락:
  - 낮음(주요 UI/OAuth 예외 메시지 처리 존재)
- 테스트 전략의 빈틈:
  - 있음(`pytest` 미설치 환경으로 자동 테스트 재실행 미완료)
- 기술 부채 또는 과설계 위험:
  - 낮음(MVP 범위 내 구현)
- 배포 준비 상태:
  - 본 프로젝트는 Git Release까지만 진행

### 발견 사항
- 결함(Blocking): 0건
- 주의 사항: 테스트 러너 부재로 단위 테스트 재실행 증적은 미확보

### 리스크/우려
- 토큰 추정치 기반 집계 특성상 실제 비용과 차이가 생길 수 있음

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 조건부 가능(테스트 러너 준비 후)
- 선행 보완 필요 항목:
  - `pytest` 실행 환경 구성

### 결정/후속 조치
- Review 판정:
  - pass (조건부)
- 다음 단계:
  - Integration Test (Pre) 대기

## Review Result (2026-02-18 21:41) - phase1-desktop-dashboard

### 검토 범위
- 주간 집계 쿼리/서비스 추가
- 대시보드 일/주 탭 분리
- 운영 문서 업데이트

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(일별/주별 탭 동시 제공)
- 성능/리소스 병목 가능성:
  - 낮음(집계 질의 2회로 제한)
- 오류 처리/예외 케이스 누락:
  - 낮음(빈 결과 처리 가능)
- 테스트 전략의 빈틈:
  - 있음(`pytest` 미설치)
- 기술 부채 또는 과설계 위험:
  - 낮음(기존 구조 확장)
- 배포 준비 상태:
  - Git Release 전 단계까지 문제 없음

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `py_compile` 통과
  - 샘플 데이터 기준 일/주 집계 행 생성 확인

### 리스크/우려
- 주차 표기(`YYYY-Www`)의 사용자 가독성 개선 여지

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 조건부 가능(테스트 러너 준비 후)
- 선행 보완 필요 항목:
  - `pytest` 환경에서 신규 테스트 실행

### 결정/후속 조치
- Review 판정:
  - pass (조건부)
- 다음 단계:
  - Integration Test (Pre) 대기

## Review Result (2026-02-18 21:42) - phase1-budget-alert-rule

### 검토 범위
- 예산 규칙 모듈 신규 추가
- 예산 상태 패널 UI 연동
- .env/README/Windows 가이드 정합성

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(정상/주의/예산 경고 규칙 구현)
- 성능/리소스 병목 가능성:
  - 낮음(새로고침 시 단순 계산)
- 오류 처리/예외 케이스 누락:
  - 낮음(환경변수 잘못된 값 폴백 처리)
- 테스트 전략의 빈틈:
  - 있음(`pytest` 미설치)
- 기술 부채 또는 과설계 위험:
  - 낮음(규칙 모듈 분리로 유지보수성 확보)
- 배포 준비 상태:
  - Git Release 전 단계까지 문제 없음

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `alert_level` 계산 결과 확인
  - 환경변수 기본값/판정 테스트 코드 추가

### 리스크/우려
- 토큰 기반 규칙은 실제 비용 임계와 1:1 매칭되지 않을 수 있음

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 조건부 가능(테스트 러너 준비 후)
- 선행 보완 필요 항목:
  - `pytest` 기반 자동 테스트 실행

### 결정/후속 조치
- Review 판정:
  - pass (조건부)
- 다음 단계:
  - Integration Test (Pre) 대기

## Review Follow-up (2026-02-18 22:37)
- 조치:
  - 테스트 러너(`pytest`) 실행 환경을 복구하고 전체 테스트를 재실행했다.
- 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - 결과: `9 passed in 0.09s`
- 상태 정리:
  - 기존 조건부 pass의 테스트 실행 제약을 해소했고 Integration Test (Pre)로 전이 가능 상태를 확인했다.

## Review Request (2026-02-18 22:59)
- 대상 태스크:
  - phase1-windows-runtime-smoke
- 검토 범위:
  - 실기기 스모크 체크리스트/증적 템플릿 신규 추가
  - Windows 런타임 프로브 스크립트(PowerShell) 추가
  - Windows 운영 가이드의 Gate A/B/C 반영
- 핵심 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md

## Review Result (2026-02-18 23:00) - phase1-windows-runtime-smoke

### 검토 범위
- Planning/Coding 산출물 정합성
- 수동 스모크 템플릿의 실행 가능성
- 자동 테스트 증적 최신화 여부

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(체크리스트/증적 템플릿/PowerShell 프로브/운영 가이드 반영 확인)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(계획된 산출물 파일이 모두 생성됨)
- 성능/리소스 병목 가능성:
  - 낮음(문서/스크립트 중심 변경)
- 오류 처리/예외 케이스 누락:
  - 낮음(스크립트에서 python/해상도 조회 실패 시 fallback 처리)
- 테스트 전략의 빈틈:
  - 있음(실기기에서 `windows_runtime_probe.ps1` 실제 실행 증적은 아직 없음)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 프로젝트 규칙상 Git Release 이전 단계 기준 문제 없음

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - 결과: `9 passed`
  - `python3 -m py_compile ...` 오류 없음

### 리스크/우려
- 실기기 증적 수집은 Windows 환경에서 최종 수행해야 하므로 현재 단계에서는 문서/자동 검증 중심 판정이다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 가능(조건부)
- 선행 보완 필요 항목:
  - Win10/Win11 각 1회 체크리스트 실행 결과 첨부

### 결정/후속 조치
- Review 판정:
  - pass (조건부)
- 다음 단계:
  - Integration Test (Pre)

## Review Request (2026-02-18 23:58)
- 대상 태스크:
  - phase1-windows-noinstall-bundle
- 검토 범위:
  - onedir 번들 빌드 스크립트와 실제 frozen 런타임 경로 정합성
  - 무설치 런처/운영 문서와 코드 경로 해석 일치 여부
- 핵심 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py

## Review Result (2026-02-18 23:58) - phase1-windows-noinstall-bundle

### 검토 범위
- Planning/Coding 산출물 정합성
- PyInstaller onedir 결과물 구조와 런타임 import 경로 안전성
- 무설치 실행 경로의 재현 가능성

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(빌드/런처/문서/테스트 항목 모두 반영)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 부분 충족(문서/스크립트/테스트 추가는 완료)
- 성능/리소스 병목 가능성:
  - 중간(onedir 번들 용량 증가 가능)
- 오류 처리/예외 케이스 누락:
  - 있음(frozen 런타임 경로 차이 처리 불충분 가능성)
- 테스트 전략의 빈틈:
  - 있음(Windows 실기기 번들 실행 증적 없음)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 미충족(실행 실패 가능성 해소 전)

### 발견 사항
- 결함(Blocking): 1건
  - [P1] `usage_service.py`가 `sys.executable` 부모 기준 `agent/src`만 탐색하는데, PyInstaller onedir 기본 구조(`_internal`)에서는 import 실패 가능
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - 결과: `12 passed` (비-frozen 경로만 검증)

### 리스크/우려
- frozen 환경에서 `collector` import 실패 시 무설치 실행 목표가 직접적으로 실패한다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - frozen 런타임 경로 탐색 전략 확정(`sys._MEIPASS`/`_internal`/exe dir 호환)
  - 빌드 스크립트 산출물 구조를 코드와 명시적으로 일치
- Coding으로 되돌릴 항목:
  - 없음(재계획 확정 후 실행)

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 불가(결함 수정 전)
- 선행 보완 필요 항목:
  - 경로 전략 재계획 + Windows 실기기 번들 실행 증적

### 결정/후속 조치
- Review 판정:
  - fail (planning return)
- 다음 단계:
  - Planning (single task) 재진입

## Review Request (2026-02-19 19:53)
- 대상 태스크:
  - phase1-windows-frozen-path-compat
- 검토 범위:
  - frozen 런타임 경로 우선순위(`_MEIPASS`/exe dir/`_internal`) 적용 여부
  - onedir 빌드/런처 스크립트와 런타임 경로 전략 정합성
  - 테스트/운영 문서 업데이트와 계획 대비 누락 여부
- 핵심 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/run_ai_usage_watcher.bat
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_usage_service.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_env_loader.py

## Review Result (2026-02-19 19:53) - phase1-windows-frozen-path-compat

### 검토 범위
- Planning/Coding 산출물 정합성
- frozen/onedir 경로 해석과 빌드 산출물 구조 일치 여부
- 자동 테스트 증적 최신화 여부

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(경로 우선순위, 빌드/런처 검증, 테스트/문서 갱신 항목 반영 확인)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(경로 우선순위와 `_internal` 호환 로직 반영)
- 성능/리소스 병목 가능성:
  - 낮음(경로 탐색은 앱 시작 시 소규모 파일 존재 확인만 수행)
- 오류 처리/예외 케이스 누락:
  - 낮음(런처에서 런타임 경로 누락 시 즉시 안내 후 중단)
- 테스트 전략의 빈틈:
  - 있음(Windows 실기기에서 onedir 빌드/런처 실실행 증적은 아직 없음)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 부분 충족(코드/테스트는 준비 완료, 실기기 증적은 후속 태스크 필요)

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - 결과: `15 passed`
  - `python3 -m py_compile ...` 오류 없음

### 리스크/우려
- Windows 실기기에서 번들 생성/실행 증적이 없으면 런처 경고/SmartScreen 대응 품질을 최종 확정하기 어렵다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 가능(조건부)
- 선행 보완 필요 항목:
  - Win10/Win11 onedir 실행 증적(`phase1-windows-noinstall-smoke-evidence`) 확보

### 결정/후속 조치
- Review 판정:
  - pass (조건부)
- 다음 단계:
  - Cycle Manager에서 `phase1-windows-noinstall-smoke-evidence`를 다음 실행 대상으로 승격

## Review Request (2026-02-19 21:30)
- 대상 태스크:
  - phase1-windows-noinstall-smoke-evidence
- 검토 범위:
  - run-id 기반 증적 생성 스크립트(`prepare_windows_smoke_evidence.ps1`)의 안정성
  - `windows_runtime_probe.ps1` 메타데이터 확장과 증적 템플릿/운영 문서 정합성
  - Planning/Coding 대비 누락/회귀 여부
- 핵심 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md

## Review Result (2026-02-19 21:30) - phase1-windows-noinstall-smoke-evidence

### 검토 범위
- Planning/Coding 산출물 정합성
- 증적 수집 스크립트의 경로/출력 일관성
- 자동 테스트 증적 최신화 여부

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(run-id 기반 증적 세트 생성, 문서/템플릿 갱신 반영 확인)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(증적 생성 스크립트/템플릿/운영 절차가 계획 범위를 충족)
- 성능/리소스 병목 가능성:
  - 낮음(실행 시 파일 복사 + JSON 생성 중심)
- 오류 처리/예외 케이스 누락:
  - 낮음(템플릿 누락/런타임 컨텍스트 생성 실패 시 명시적 오류 처리)
- 테스트 전략의 빈틈:
  - 있음(macOS 환경에서 PowerShell 실실행 검증 불가)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 부분 충족(코드/문서는 준비 완료, Win10/Win11 실기기 실행 증적 필요)

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - 결과: `15 passed`
  - `python3 -m py_compile ...` 오류 없음

### 리스크/우려
- 실기기(Win10/Win11)에서 `prepare_windows_smoke_evidence.ps1` 실행 결과를 아직 첨부하지 않아 Gate B/C 최종 판정은 보류다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 가능(조건부)
- 선행 보완 필요 항목:
  - Win10/Win11에서 run-id artifact 1세트 이상 수집 후 첨부

### 결정/후속 조치
- Review 판정:
  - pass (조건부)
- 다음 단계:
  - Cycle Manager에서 `phase1-windows-runtime-smoke`를 integration_test_pre 대상으로 재승격

## Review Request (2026-02-19 21:57)
- 대상 태스크:
  - phase1-windows-noinstall-smoke-evidence
- 검토 범위:
  - 번들 단독 실행 기준 증적 수집 흐름(`collect_windows_smoke_evidence.bat`) 추가
  - `prepare_windows_smoke_evidence.ps1`/`windows_runtime_probe.ps1`의 repo+bundle 듀얼 모드 경로 정합성
  - 번들 빌드 산출물에 증적 스크립트/템플릿 포함 여부
- 핵심 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/collect_windows_smoke_evidence.bat
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md

## Review Result (2026-02-19 21:57) - phase1-windows-noinstall-smoke-evidence

### 검토 범위
- Planning/Coding 산출물 정합성
- 번들 단독 증적 수집 UX와 경로 해석 안전성
- 자동 테스트 회귀 여부

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(증적 생성 절차 스크립트화/문서화 요구를 충족)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(번들 루트 원클릭 증적 수집 경로 추가)
- 성능/리소스 병목 가능성:
  - 낮음(파일 복사 + JSON 생성 중심)
- 오류 처리/예외 케이스 누락:
  - 낮음(스크립트/템플릿/실행파일 누락 시 명시적 에러 처리)
- 테스트 전략의 빈틈:
  - 있음(Windows 실기기에서 BAT/PowerShell 체인 실실행 증적은 아직 없음)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 부분 충족(코드/문서 준비 완료, 실기기 증적 필요)

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - 결과: `15 passed in 0.09s`
  - `python3 -m py_compile ...` 오류 없음

### 리스크/우려
- Win10/Win11 실기기에서 `collect_windows_smoke_evidence.bat` 실행 산출물이 첨부되지 않으면 Integration Test (Pre) `ui_required` 게이트를 닫을 수 없다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 가능(조건부)
- 선행 보완 필요 항목:
  - Win10/Win11 각 1회 `collect_windows_smoke_evidence.bat` 또는 `prepare_windows_smoke_evidence.ps1` 실행 artifact 첨부

### 결정/후속 조치
- Review 판정:
  - pass (조건부)
- 다음 단계:
  - Integration Test (Pre) 재실행 전 Windows 실기기 artifact 수집

## Review Request (2026-02-19 23:37)
- 대상 태스크:
  - phase1-windows-exe-build-artifact-delivery
- 검토 범위:
  - GitHub Actions 기반 Windows onedir 빌드 워크플로 추가
  - `AIUsageWatcher.exe` 체크섬 생성/아티팩트 업로드 경로
  - Planning 대비 README 운영 절차 누락 여부
- 핵심 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/.github/workflows/windows-exe-build.yml
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-exe-build-artifact-delivery.md

## Review Result (2026-02-19 23:37) - phase1-windows-exe-build-artifact-delivery

### 검토 범위
- Planning/Coding 산출물 정합성
- Windows CI 빌드 워크플로의 실행 가능성
- 아티팩트 전달/문서화 완결성

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(워크플로 추가, 체크섬 생성, README 절차 반영 확인)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(Windows 러너 빌드 + checksum + artifact 업로드 경로 구현)
- 성능/리소스 병목 가능성:
  - 중간(CI 빌드 시간은 길 수 있으나 기능상 blocking 이슈는 아님)
- 오류 처리/예외 케이스 누락:
  - 낮음(`AIUsageWatcher.exe` 미생성 시 checksum 단계에서 명시적 실패)
- 테스트 전략의 빈틈:
  - 있음(로컬 `actionlint` 미설치, GitHub Actions 원격 첫 실행 증적 미첨부)
- 기술 부채 또는 과설계 위험:
  - 낮음(기존 빌드 스크립트 재사용으로 단순성 유지)
- 배포 준비 상태:
  - 부분 충족(워크플로 코드는 준비 완료, 첫 원격 run 확인 필요)

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - 결과: `15 passed in 0.09s`
  - `python3 -m py_compile ...` 오류 없음
  - `actionlint not found`

### 리스크/우려
- GitHub Actions 첫 실행이 실패하면 artifact 전달 체인이 완결되지 않을 수 있다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 가능(조건부)
- 선행 보완 필요 항목:
  - GitHub Actions `Windows EXE Build` 1회 실행 성공 증적(run URL + artifact 캡처) 첨부

### 결정/후속 조치
- Review 판정:
  - pass (조건부)
- 다음 단계:
  - Integration Test (Pre) 또는 Git Release 전, 원격 CI 성공 증적 1회 확보

## Review Follow-up (2026-02-20 09:22) - phase1-windows-exe-build-artifact-delivery

### 검토 범위
- 최신 CI 실패 원인 수정(`sqlite3` stdlib 누락 대응) 반영 여부
- GitHub Actions `Windows EXE Build` 재실행 성공 여부
- 로컬 회귀 테스트 최신화 여부

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(실패 원인 보정 + 워크플로 성공 증적 확보)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(최신 run `#9` 성공 + artifact 업로드 확인)
- 성능/리소스 병목 가능성:
  - 중간(CI 빌드 시간 변동성은 존재)
- 오류 처리/예외 케이스 누락:
  - 낮음(`sqlite3` stdlib 부재 시 fallback 경로로 처리)
- 테스트 전략의 빈틈:
  - 낮음(로컬 자동 테스트 + 원격 CI 성공 증적 확보)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 충족(project terminal stage = `git_release`)

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q` -> `16 passed in 0.09s`
  - `python3 -m py_compile ...` 오류 없음
  - GitHub Actions run `#9` (`22205898127`) `success`
  - artifact `AIUsageWatcher-windows-bundle` (`5582483073`) 생성 확인

### 리스크/우려
- Windows 실기기 수동 스모크는 여전히 권장 항목이며 push 차단 게이트는 아님(project override 유지).

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 완료(pass)
- 선행 보완 필요 항목:
  - 없음

### 결정/후속 조치
- Review 판정:
  - pass
- 다음 단계:
  - Git Release 기록 동기화 및 Cycle `done` 반영

## Review Follow-up (2026-02-20 10:24) - phase1-windows-noinstall-smoke-evidence

### 검토 범위
- 사용자 제보 기반 스크립트 오류 2건 재검토
  - `prepare_windows_smoke_evidence.ps1` 파서 오류
  - `windows_runtime_probe.ps1` 경로 정규화 예외
- 최신 원격 CI run 성공 여부 및 bundle 반영 여부

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(Hotfix addendum에서 정의한 보강 항목 모두 반영)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(경로 정규화 보강 + 문자열 파서 오류 제거 + 최신 CI success)
- 성능/리소스 병목 가능성:
  - 낮음(스크립트 입력 정규화만 추가)
- 오류 처리/예외 케이스 누락:
  - 낮음(`IsPathRooted`/`GetFullPath` 예외에 원인 포함 메시지 추가)
- 테스트 전략의 빈틈:
  - 중간(실사용자 PC에 남은 구버전 dist 실행 시 동일 오류 가능)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 충족(project terminal stage = `git_release`)

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q` -> `16 passed in 0.09s`
  - `python3 -m py_compile ...` 오류 없음
  - GitHub Actions run `#10` (`22206380280`) `success`
  - GitHub Actions run `#11` (`22207320762`) `success`
  - artifact `AIUsageWatcher-windows-bundle` (`5583044121`) 생성 확인

### 리스크/우려
- 사용자 환경에서 이전 bundle(`line 13 == IsPathRooted`)을 계속 실행하면 동일 증상이 재발한다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 완료(pass)
- 선행 보완 필요 항목:
  - 사용자 실행 환경 dist 교체(최신 artifact 또는 재빌드)

### 결정/후속 조치
- Review 판정:
  - pass
- 다음 단계:
  - Integration Test/Git Release/Process Verification 기록 동기화

## Review Follow-up (2026-02-20 10:45) - phase1-windows-noinstall-smoke-evidence

### 검토 범위
- 사용자 제보 기반 버그 수정 재검토
  - `collect_windows_smoke_evidence.bat` → PowerShell `-BundleRoot` 인수 전달 시 trailing backslash 버그
  - `windows_runtime_probe.ps1` `Normalize-PathInput` 이중 방어 보강
  - `prepare_windows_smoke_evidence.ps1` `Normalize-PathInput` 동일 보강

### 근본 원인 분석
- `%~dp0`(cmd.exe)은 경로 끝에 `\`를 포함한다. (예: `C:\...\AIUsageWatcher\`)
- 이를 `"..."` 안에 넣으면 `"C:\...\AIUsageWatcher\"` → `\"` 가 이스케이프로 처리되어 닫는 `"` 가 사라진다.
- 결과적으로 PowerShell이 받는 `-BundleRoot` 값 = `C:\...\AIUsageWatcher"` (끝에 `"` 포함)
- `Normalize-PathInput`의 대칭 따옴표 감지 로직이 비대칭(`앞 없음, 뒤만 있음`)에 반응하지 못해 `IsPathRooted` 예외 발생

### 수정 내용
- `collect_windows_smoke_evidence.bat` (근본 수정)
  - `set "BUNDLE_ROOT=%BASE_DIR:~0,-1%"` 로 trailing `\` 제거 후 PowerShell 인수 전달
- `windows_runtime_probe.ps1` (방어 보강)
  - `Normalize-PathInput`에 비대칭 홀로 따옴표 제거 로직 추가 (Case 2/3 분기)
- `prepare_windows_smoke_evidence.ps1` (방어 보강)
  - 동일한 `Normalize-PathInput` 강화 적용

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(버그 수정 범위는 기존 스크립트 안정성 개선으로 Planning 범위 내)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(경로 전달 버그 수정으로 실기기 증적 수집 흐름이 정상 작동)
- 성능/리소스 병목 가능성:
  - 낮음(문자열 처리 변경만 포함)
- 오류 처리/예외 케이스 누락:
  - 낮음(이중 방어로 비대칭 따옴표 케이스 추가 대응)
- 테스트 전략의 빈틈:
  - 중간(수정된 `.bat` 파일은 Windows 실기기에서만 최종 검증 가능)
- 기술 부채 또는 과설계 위험:
  - 낮음(최소한의 방어적 수정)
- 배포 준비 상태:
  - 충족(project terminal stage = `git_release`)

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - 버그 재현 경로: `collect_windows_smoke_evidence.bat` → PowerShell → `Resolve-WorkspacePath` → `IsPathRooted` 예외
  - 수정 후 로직: `set "BUNDLE_ROOT=%BASE_DIR:~0,-1%"` 로 trailing `\` 제거, `Normalize-PathInput` 비대칭 따옴표 방어
  - py_compile/pytest 변경 없음 (PowerShell/BAT 파일 전용 수정)

### 리스크/우려
- 이전 dist 번들을 그대로 쓰는 경우 구버전 스크립트가 남아 동일 버그 재발 가능.
- 해결: artifact 재빌드 또는 수정된 스크립트 3개를 bundle 폴더에 수동 교체 필요.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 완료(pass)
- 선행 보완 필요 항목:
  - 없음(단, 실행 환경의 dist 번들을 최신 버전으로 교체 권장)

### 결정/후속 조치
- Review 판정:
  - pass
- 다음 단계:
  - Git Release (수정 3개 파일 commit/tag/push)

## Review Follow-up (2026-02-22 22:55) - phase1-desktop-dashboard (Tk Font Spec Hotfix)

### 검토 범위
- 대시보드 초기화 크래시 원인(`expected integer but got "UI"`) 수정 정합성
- Planning addendum과 Coding 결과의 추적 가능성
- 테스트 증적(py_compile/pytest) 확인

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(폰트 파싱 원인, 수정 방식, 테스트 계획 모두 반영)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(문제 원인 구간 직접 수정 + 회귀 테스트 추가)
- 성능/리소스 병목 가능성:
  - 낮음(문자열 생성 헬퍼 추가 수준)
- 오류 처리/예외 케이스 누락:
  - 낮음(공백 패밀리명 파싱 오류 재발 방지)
- 테스트 전략의 빈틈:
  - 중간(Windows 실기기 UI 실행 확인은 별도)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 충족(핫픽스 단위 변경)

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q desktop_win/tests` -> `15 passed in 0.12s`
  - `python3 -m py_compile desktop_win/src/*.py desktop_win/tests/*.py` 오류 없음

### 리스크/우려
- 실제 Windows 폰트 설치 상태에 따라 렌더링 차이는 있을 수 있으나, 본 건의 크래시(`TclError`)와는 분리된 범주다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 가능(pass)
- 선행 보완 필요 항목:
  - 없음

### 결정/후속 조치
- Review 판정:
  - pass
- 다음 단계:
  - Windows 실기기에서 앱 실행 smoke 1회 확인 후 Integration Test 문서 반영 권장

## Review Follow-up (2026-02-22 23:21) - phase1-win-agent-usage-collector (OAuth Browser Policy)

### 검토 범위
- OAuth 브라우저 실행 정책이 Chrome-first 요구사항을 충족하는지
- 코드/테스트/문서 간 정합성
- 회귀 테스트 결과 확인

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(브라우저 모드 정의, 변경 파일, 검증 항목 반영)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(`chrome` 기본 정책 + `chrome_only/default` 지원)
- 성능/리소스 병목 가능성:
  - 낮음(로그인 시작 시 1회 프로세스 실행)
- 오류 처리/예외 케이스 누락:
  - 낮음(Chrome 실패/invalid mode/브라우저 오픈 실패 모두 예외 처리)
- 테스트 전략의 빈틈:
  - 중간(Windows 실기기 경로 편차는 수동 확인 권장)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 충족

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q desktop_win/tests` -> `21 passed in 0.10s`
  - `python3 -m py_compile desktop_win/src/*.py desktop_win/tests/*.py` 오류 없음

### 리스크/우려
- 일부 Windows 환경에서 Chrome 탐색 경로가 다를 수 있어 `AUIW_CHROME_PATH` 수동 지정이 필요할 수 있다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 가능(pass)
- 선행 보완 필요 항목:
  - 없음(권장: 실기기 smoke 1회)

### 결정/후속 조치
- Review 판정:
  - pass
- 다음 단계:
  - Git push 및 Windows 실기기에서 `AUIW_OAUTH_BROWSER` 모드별 smoke 체크

## Review Follow-up (2026-02-22 23:41) - phase1-win-agent-usage-collector (Codex CLI Auth Bridge)

### 검토 범위
- 로그인 경로가 일반 OAuth 설정 기반에서 Codex CLI(ChatGPT OAuth 재사용)로 올바르게 전환됐는지
- 앱/테스트/문서 산출물 정합성

### 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 없음(작업 K/L 및 검증 항목 반영 완료)
- Coding -> Planning 역추적 불가 항목:
  - 없음

### 보수 검토 체크리스트
- AC 충족 여부:
  - 충족(`Codex 로그인` 버튼이 CLI 상태조회 + device-auth 실행 흐름을 수행)
- 성능/리소스 병목 가능성:
  - 낮음(로그인 시에만 외부 프로세스 호출)
- 오류 처리/예외 케이스 누락:
  - 낮음(CLI 미설치, timeout, 미로그인, 비정상 출력 처리)
- 테스트 전략의 빈틈:
  - 중간(Windows 실기기에서 CLI PATH 편차 수동 점검 권장)
- 기술 부채 또는 과설계 위험:
  - 낮음
- 배포 준비 상태:
  - 충족

### 발견 사항
- 결함(Blocking): 0건
- 확인 증적:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q desktop_win/tests` -> `28 passed in 0.13s`
  - `python3 -m py_compile desktop_win/src/*.py desktop_win/tests/*.py` 오류 없음

### 리스크/우려
- Codex CLI 미설치 또는 PATH 미노출 환경에서는 로그인 버튼 동작이 실패할 수 있다.

### 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음
- Coding으로 되돌릴 항목:
  - 없음

### 배포 게이트 판정
- Integration Test 진행 가능:
  - 가능(pass)
- 선행 보완 필요 항목:
  - 없음(권장: Windows에서 `codex login --device-auth` 실기기 smoke 1회)

### 결정/후속 조치
- Review 판정:
  - pass
- 다음 단계:
  - Git push 및 실기기 smoke 체크리스트 업데이트
