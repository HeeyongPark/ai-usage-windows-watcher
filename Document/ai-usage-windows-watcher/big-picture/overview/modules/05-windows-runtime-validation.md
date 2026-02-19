# Windows 실기기 검증

## 목적
- "로컬에서 코드가 돌아간다"를 넘어 "Windows 사용자 환경에서 실제로 동작한다"를 검증한다.
- 본 모듈의 실기기 증적은 현재 프로젝트 운영 정책상 권장 항목이며, push 차단 게이트는 자동 테스트로 운영한다.

## 검증 매트릭스
- OS:
  - Windows 10 (22H2 이상)
  - Windows 11
- 배포 형태:
  - 무설치 실행 번들(내장 런타임 포함)
  - 개발자 경로(venv/pip, 회귀 비교용)
- 화면:
  - 800x480 (5인치)
  - 1920x1080

## 필수 시나리오
1. 무설치 실행:
- Python/Git 미설치 환경에서 번들 실행 파일(또는 런처) 실행 성공
  - onedir 경로(`_internal` 포함)에서 `collector` import 오류가 발생하지 않음
2. OAuth 로그인:
- 브라우저 로그인 후 앱 상태가 `OAuth 완료`로 전환
3. 데이터 표시:
- `Codex 샘플 1건 생성` 후 일/주 탭 수치 반영
4. 자동 갱신:
- `AUIW_REFRESH_INTERVAL_SEC` 설정이 최소값 규칙(60초)과 함께 반영
5. 예산 알림:
- 임계치 초과 조건에서 `warning/critical` 상태 표시
6. 재시작 내구성:
- 앱 재시작 후 OAuth 토큰 및 DB 데이터 유지

## 실패 우선순위
- P0:
  - 앱 기동 실패, 런처/번들 실행 실패, OAuth 로그인 불가, 데이터 조회 불가
- P1:
  - 자동 갱신 미동작, 예산 상태 오표시
- P2:
  - 소형 해상도 가독성 저하, 텍스트 잘림

## 증적 기록 규칙
- 실행 1회당 아래를 남긴다.
  - 실행 시각, Windows 버전, 배포 방식(무설치/개발자 경로)
  - 번들 구조 정보(평탄/`_internal`)
  - 시나리오별 pass/fail
  - 실패 시 재현 단계 + 스크린샷 경로

## 증적 수집 표준 경로
- 번들 단독(권장):
  - `collect_windows_smoke_evidence.bat` 실행
  - 출력: `smoke_evidence/artifacts/runtime-context-<run-id>.json`
  - 출력: `smoke_evidence/artifacts/windows-runtime-smoke-checklist-<run-id>.md`
  - 출력: `smoke_evidence/artifacts/windows-runtime-evidence-<run-id>.md`
- 저장소 경로(빌드/개발 머신):
  - `scripts/prepare_windows_smoke_evidence.ps1 -BundleRoot .\\dist\\AIUsageWatcher`
  - 출력: `tests/manual/artifacts/*`
