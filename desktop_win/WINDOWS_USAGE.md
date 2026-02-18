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
## 9) 데이터/토큰 저장 위치
- OAuth 토큰: `%APPDATA%\AIUsageWatcher\oauth_token.json`
- 사용량 DB 기본 경로: `%USERPROFILE%\.ai-usage-watcher\usage.db`
- DB 경로 변경 시 `AUIW_DB_PATH` 환경변수 사용
