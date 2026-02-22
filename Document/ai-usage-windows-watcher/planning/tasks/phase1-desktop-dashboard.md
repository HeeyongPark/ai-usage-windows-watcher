# Task phase1-desktop-dashboard

## Metadata
- project-id: ai-usage-windows-watcher
- source_mode: from_cycle_manager
- created_at: 2026-02-18 21:38 KST

## Collaboration Mode
- selected_mode: confirm_each_cycle
- re-confirm triggers:
  - 대시보드 정보 구조 변경
  - 핵심 UI 프레임워크 변경
  - 개인정보 표시 정책 변경

## 입력
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
- Cycle 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- 태스크 요약:
  - 로컬 사용량 데이터를 Windows UI에서 일/주 단위로 빠르게 확인할 수 있는 대시보드 MVP를 완성한다.

## 사용자 확인 게이트
- 핵심 내용:
  - 운영자가 즉시 사용량 추세를 확인할 수 있는 화면을 제공한다.
- 방향:
  - Tkinter UI를 유지하며 데이터 조회/표현 계층을 확장한다.
- 고민거리:
  - 작은 해상도에서도 정보 과밀 없이 일/주 데이터를 동시에 제공하는 방법

## 문제 정의
- 해결 문제:
  - 기존 화면이 일별 집계 중심이라 주간 추세를 빠르게 판단하기 어렵다.
- 비목표:
  - 고급 차트 라이브러리 도입
  - 클라우드 동기화/원격 데이터 연동

## 구현 단위 (Coding 실행 단위)
- 작업 A: 주간 집계 조회 로직 추가
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/storage.py
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
  - 구현 상세:
    - SQLite 주간 집계 쿼리(`YYYY-Www`) 추가
    - Codex 필터가 적용된 `codex_weekly_summary()` 서비스 제공
  - 테스트:
    - 주간 집계 반환 형식/도구 필터 단위 테스트

- 작업 B: UI 일/주 탭 분리
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
  - 구현 상세:
    - Notebook 탭으로 일별/주별 표를 분리
    - 새로고침 시 두 표를 동시에 갱신
  - 테스트:
    - py_compile 및 데이터 샘플 주입 후 조회 동작 확인

- 작업 C: 운영 문서 정합성 업데이트
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
  - 구현 상세:
    - 일/주 탭 사용 흐름을 문서에 반영
  - 테스트:
    - 실행 가이드 단계별 재현성 점검

## 테스트 설계
- 기능 테스트:
  - 샘플 세션 생성 후 일별/주별 탭에 집계가 노출되는지 검증
- 회귀 테스트:
  - 기존 OAuth 로그인/새로고침 흐름이 그대로 동작하는지 점검
- 실패/예외 테스트:
  - DB 비어있음/경로 변경 시 앱 오류 없이 동작하는지 확인

## 리스크 및 대응
- 리스크:
  - 주차 포맷이 연말/연초 경계에서 직관적이지 않을 수 있음
  - 대응:
    - `YYYY-Www` 고정 포맷으로 표기하고 후속 태스크에서 라벨 개선
- 리스크:
  - UI 컴포넌트 증가로 소형 화면 가독성 저하 가능
  - 대응:
    - 탭 구조로 정보 밀도를 분리

## 완료 조건 (Definition of Done)
- DoD 1:
  - Codex 일별/주별 집계가 모두 대시보드에서 조회된다.
- DoD 2:
  - 주간 집계 서비스와 관련 테스트가 추가된다.
- DoD 3:
  - 사용자 가이드 문서가 UI 동작과 일치한다.

## Handoff
- To Coding:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- To Integration Test (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
- To Cycle Manager (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md

## Addendum (2026-02-22 22:55 KST) - Tk Font Spec Crash Hotfix

### 입력 증상
- Windows 실행 시 대시보드 초기 레이아웃 생성 단계에서 아래 오류로 앱이 종료됨.
  - `_tkinter.TclError: expected integer but got "UI"`
- traceback 기준:
  - `desktop_win/src/app.py` `UsageDashboardApp.__init__` -> `_build_layout()`

### 문제 정의
- `self.option_add("*Font", "Segoe UI 11")` 형태 문자열은 Tk 폰트 파서에서 `family=Segoe`, `size=UI`로 오해될 수 있다.
- 결과적으로 공백이 포함된 폰트 패밀리(`Segoe UI`)가 정수 크기 파싱 오류를 유발한다.

### 구현 단위 (Hotfix)
- 작업 D: 기본 폰트 옵션 문자열 안전화
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
  - 구현 상세:
    - 폰트 옵션 헬퍼 `_font_option_value(size)` 추가
    - `*Font` 값을 `"{Segoe UI} 11"` 형태로 지정해 Tk 파서 오해 방지
  - 테스트:
    - `desktop_win/tests/test_refresh_interval.py`에 헬퍼 회귀 테스트 추가

### 테스트 설계 (Hotfix)
- 기능 테스트:
  - 앱 초기화 시 `LabelFrame/Notebook` 생성 구간에서 TclError 미발생 확인
- 회귀 테스트:
  - 기존 refresh interval 테스트 영향 없음
- 실패/예외 테스트:
  - 숫자 크기 파싱이 필요한 폰트 옵션이 brace 형식으로 유지되는지 단위 테스트 검증

### 완료 조건 (Hotfix DoD)
- DoD 1:
  - `expected integer but got "UI"` 오류가 재현되지 않는다.
- DoD 2:
  - desktop_win 테스트가 통과한다.
- DoD 3:
  - Coding/Review 문서에 수정 근거와 검증 결과가 연결된다.
