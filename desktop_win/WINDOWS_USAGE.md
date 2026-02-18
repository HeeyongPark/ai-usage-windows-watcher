# Windows 사용 가이드

## 1) 사전 준비
- Windows 10/11
- Python 3.11 이상
- Git

## 2) 프로젝트 받기
PowerShell:
```powershell
cd C:\Users\<사용자>\Documents
git clone git@github.com:HeeyongPark/ai-usage-windows-watcher.git
cd .\ai-usage-windows-watcher\
```

## 3) 가상환경/의존성 설치
PowerShell:
```powershell
cd .\agent\
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\requirements.txt
```

## 4) OAuth 환경변수 설정
1. `desktop_win\.env.example`를 복사해 `desktop_win\.env` 생성
2. 아래 3개를 반드시 채움
- `AUIW_OAUTH_AUTH_URL`
- `AUIW_OAUTH_TOKEN_URL`
- `AUIW_OAUTH_CLIENT_ID`

참고:
- 앱 실행 시 `desktop_win\.env`를 자동 로드한다.

## 5) 앱 실행
PowerShell:
```powershell
cd ..\desktop_win\
python .\src\app.py
```

## 6) 기본 사용 순서
1. `OAuth 로그인` 버튼 클릭
2. 브라우저에서 로그인 완료
3. 앱으로 돌아와 로그인 상태 확인
4. `Codex 샘플 1건 생성`으로 테스트 데이터 생성
5. 일별 사용량 표에서 세션/요청/토큰 확인
6. 주별 탭에서 주차별 합계를 확인
7. 예산 알림 규칙 패널에서 정상/주의/경고 상태 확인

## 7) 5인치 모니터 사용 팁
- 앱은 기본 전체화면으로 시작한다.
- `F11`: 전체화면 토글
- `Esc`: 전체화면 종료
- 작은 해상도(예: 800x480)에서는 요약 영역이 세로 배치로 자동 전환된다.

## 8) 데이터 갱신 주기
- 기본 자동 갱신 주기: 1시간(3600초)
- 화면 우측에 `최근 갱신`과 `자동 갱신` 정보가 표시된다.
- 즉시 반영이 필요하면 `새로고침` 버튼 사용
- 주기 변경 시 `desktop_win\.env`에 설정
  - `AUIW_REFRESH_INTERVAL_SEC=3600`
  - 최소 60초 이상만 허용

## 9) 예산 임계치 알림 규칙
- 앱은 토큰 사용량 기준으로 일/주 예산 상태를 계산한다.
- 설정 파일(`desktop_win\.env`) 예시:
  - `AUIW_DAILY_TOKEN_BUDGET=20000`
  - `AUIW_WEEKLY_TOKEN_BUDGET=100000`
  - `AUIW_ALERT_THRESHOLD_PCT=80`
- 상태 의미:
  - `정상`: 임계치 미만
  - `주의`: 임계치 비율 이상
  - `예산 경고`: 예산 초과

## 10) 데이터/토큰 저장 위치
- OAuth 토큰: `%APPDATA%\AIUsageWatcher\oauth_token.json`
- 사용량 DB 기본 경로: `%USERPROFILE%\.ai-usage-watcher\usage.db`
- DB 경로 변경 시 `AUIW_DB_PATH` 환경변수 사용

## 11) Windows 실기기 스모크 검증(권장)
1. 런타임 정보 수집
PowerShell:
```powershell
cd .\desktop_win\
powershell -ExecutionPolicy Bypass -File .\scripts\windows_runtime_probe.ps1 -OutputPath .\tests\manual\artifacts\runtime-context-win11-devbox.json
```
2. 체크리스트 수행
- `desktop_win\tests\manual\windows-runtime-smoke-checklist.md`의 6개 필수 시나리오를 순서대로 점검
3. 증적 정리
- 템플릿: `desktop_win\tests\manual\windows-runtime-evidence-template.md`
- 실패 시 스크린샷/로그 경로를 반드시 기록

## 12) Phase 1 게이트 기준
- Gate A: 자동 테스트(`agent\.venv\Scripts\python -m pytest -q`) 통과
- Gate B: Win10/Win11 실기기 스모크 각 1회 이상 수행
- Gate C: 실패 케이스(OAuth 설정 누락/DB 경로 변경/갱신 주기 최소값) 증적 확보
