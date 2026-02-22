# Windows 사용 가이드

## 1) 사전 준비
- Windows 10/11
- (사용자 실행용) 추가 설치 불필요
- (빌드 머신 전용) Python 3.11 이상

## 2) onedir 번들 받기 또는 생성
### A. 이미 빌드된 번들 받기 (권장)
- `AIUsageWatcher` 폴더 전체를 Windows PC로 복사
- 폴더에는 최소 아래 파일이 있어야 함
  - `AIUsageWatcher.exe`
  - `run_ai_usage_watcher.bat`
  - `.env.example`
  - `_internal\python3*.dll` 및 `_internal\python3.dll` (또는 flat 동등 파일)
  - `_internal\agent\src\collector.py` 또는 `agent\src\collector.py`

### B. 직접 번들 생성 (빌드 머신)
PowerShell:
```powershell
cd C:\Users\<사용자>\Documents
git clone git@github.com:HeeyongPark/ai-usage-windows-watcher.git
cd .\ai-usage-windows-watcher\
cd .\desktop_win\
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows_bundle.ps1
```

## 3) Codex 로그인 준비
1. Codex CLI 설치 확인:
```powershell
codex --version
```
2. ChatGPT OAuth로 Codex 로그인:
```powershell
codex login --device-auth
```
3. 로그인 상태 확인:
```powershell
codex login status
```
4. 앱에서 `Codex 로그인` 버튼을 누르면 상태를 재확인하고, 필요 시 device-auth를 재실행한다.

## 4) 앱 실행 (무설치)
- `AIUsageWatcher\run_ai_usage_watcher.bat` 더블클릭 (권장)
- 또는 `AIUsageWatcher\AIUsageWatcher.exe` 직접 실행

### DLL 로드 오류 트러블슈팅
- 오류 예시: `Failed to load Python DLL ... _internal\python312.dll`
- 오류 예시: `ModuleNotFoundError: No module named 'sqlite3'`
- 실행 위치를 먼저 확인:
  - 표준 경로: `desktop_win\dist\AIUsageWatcher\run_ai_usage_watcher.bat`
  - 비표준 경로(예: `desktop_win\build\dist\UsageWatcher\...`) 산출물은 사용하지 않음
- OneDrive 경로에서 실행 중이면 폴더를 `Always keep on this device`로 고정
- 번들 내 `_internal\python3*.dll`, `_internal\python3.dll` 존재를 확인
- 번들 내 `_internal\_sqlite3.pyd` 존재를 확인
- 누락 시 아래 명령으로 재빌드:
```powershell
cd C:\path\to\ai-usage-windows-watcher\desktop_win\
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows_bundle.ps1
```

## 5) 기본 사용 순서
1. `Codex 로그인` 버튼 클릭
2. 브라우저에서 로그인 완료
3. 앱으로 돌아와 로그인 상태 확인
4. `Codex 샘플 1건 생성`으로 테스트 데이터 생성
5. 일별 사용량 표에서 세션/요청/토큰 확인
6. 주별 탭에서 주차별 합계를 확인
7. 예산 알림 규칙 패널에서 정상/주의/경고 상태 확인

## 6) 5인치 모니터 사용 팁
- 앱은 기본 전체화면으로 시작한다.
- `F11`: 전체화면 토글
- `Esc`: 전체화면 종료
- 작은 해상도(예: 800x480)에서는 요약 영역이 세로 배치로 자동 전환된다.

## 7) 데이터 갱신 주기
- 기본 자동 갱신 주기: 1시간(3600초)
- 화면 우측에 `최근 갱신`과 `자동 갱신` 정보가 표시된다.
- 즉시 반영이 필요하면 `새로고침` 버튼 사용
- 주기 변경 시 번들 폴더의 `.env`에 설정
  - `AUIW_REFRESH_INTERVAL_SEC=3600`
  - 최소 60초 이상만 허용

## 8) 예산 임계치 알림 규칙
- 앱은 토큰 사용량 기준으로 일/주 예산 상태를 계산한다.
- 설정 파일(`AIUsageWatcher\.env`) 예시:
  - `AUIW_DAILY_TOKEN_BUDGET=20000`
  - `AUIW_WEEKLY_TOKEN_BUDGET=100000`
  - `AUIW_ALERT_THRESHOLD_PCT=80`
- 상태 의미:
  - `정상`: 임계치 미만
  - `주의`: 임계치 비율 이상
  - `예산 경고`: 예산 초과

## 9) 데이터/토큰 저장 위치
- Codex 인증 토큰: Codex CLI 기본 저장소(플랫폼 기본 경로)
- 사용량 DB 기본 경로: `%USERPROFILE%\.ai-usage-watcher\usage.db`
- DB 경로 변경 시 `AUIW_DB_PATH` 환경변수 사용

## 10) Windows 실기기 스모크 검증(권장)
1. 증적 세트(run-id) 초기화
- A. 번들 폴더에서 원클릭 실행 (권장)
  - `AIUsageWatcher\\collect_windows_smoke_evidence.bat` 더블클릭
  - 필요 시 run-id 지정:
    - `collect_windows_smoke_evidence.bat win11-devbox-01`
- B. 저장소 경로에서 실행 (빌드/개발 머신)
PowerShell:
```powershell
cd C:\path\to\ai-usage-windows-watcher\desktop_win\
powershell -ExecutionPolicy Bypass -File .\scripts\prepare_windows_smoke_evidence.ps1 -BundleRoot .\dist\AIUsageWatcher
```
- 출력:
  - 번들 모드: `smoke_evidence\artifacts\runtime-context-<run-id>.json`
  - 번들 모드: `smoke_evidence\artifacts\windows-runtime-smoke-checklist-<run-id>.md`
  - 번들 모드: `smoke_evidence\artifacts\windows-runtime-evidence-<run-id>.md`
  - 저장소 모드: `tests\manual\artifacts\...`

2. 런타임 정보 단독 수집(선택)
PowerShell:
```powershell
cd C:\path\to\AIUsageWatcher\
powershell -ExecutionPolicy Bypass -File .\windows_runtime_probe.ps1 -BundleRoot . -OutputPath .\smoke_evidence\artifacts\runtime-context-win11-devbox.json
```
3. 체크리스트 수행
- `smoke_evidence\artifacts\windows-runtime-smoke-checklist-<run-id>.md` (또는 저장소 모드의 `desktop_win\tests\manual\artifacts\...`) 6개 필수 시나리오를 순서대로 점검 (1번은 onedir 실행 기준)
  - 실행 시 번들 구조가 `AIUsageWatcher\_internal\...`인지(또는 flat) 함께 기록
4. 증적 정리
- 템플릿(자동 생성본 우선): `smoke_evidence\artifacts\windows-runtime-evidence-<run-id>.md` (또는 저장소 모드 경로)
- 실패 시 스크린샷/로그 경로를 반드시 기록

## 11) Phase 1 게이트 기준
- Gate A: 자동 테스트(`agent\.venv\Scripts\python -m pytest -q`) 통과
- Gate B: Win10/Win11 실기기 무설치(onedir) 스모크 각 1회 이상 수행
- Gate C: 실패 케이스(Codex CLI 미설치/미로그인/DB 경로 변경/갱신 주기 최소값/런처 또는 onedir 폴더 누락/frozen import 실패) 증적 확보

## 12) 개발자 경로(참고)
- 일반 사용자 경로가 아닌 개발/디버깅 목적일 때만 사용
```powershell
cd C:\path\to\ai-usage-windows-watcher\agent\
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\requirements.txt

cd ..\desktop_win\
python .\src\app.py
```
