# Task phase1-win-agent-usage-collector

## Metadata
- subject: ai-usage-windows-watcher
- source_mode: from_cycle_manager
- created_at: 2026-02-18 16:03

## Collaboration Mode
- selected_mode: confirm_each_cycle
- re-confirm triggers:
  - 수집 지표 변경
  - 스택 변경
  - 개인정보 정책 변경

## 입력
- Big Picture 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
- Cycle 소스:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
- Notion 소스:
  - https://www.notion.so/mirador/30be497bcfdf807a877bdccfbdcbd8c4?source=copy_link
- 태스크 요약:
  - Windows에서 AI 도구 사용 세션을 감지하고 로컬 DB에 누적하는 최소 수집기를 만든다.

## 사용자 확인 게이트
- 핵심 내용:
  - 첫 배포 전, 수집 신뢰성과 개인정보 최소 수집 원칙을 동시에 만족해야 한다.
- 방향:
  - 로컬 우선(offline-first) 수집기로 시작하고 서버 전송은 비목표로 둔다.
- 고민거리:
  - 요청 수/토큰을 어떤 수준에서 정확히 측정할지(직접 수집 vs 추정)

## 문제 정의
- 해결 문제:
  - AI 사용량이 도구별로 분산되어 비용/활용 현황을 한 번에 파악하기 어렵다.
- 비목표:
  - 원격 계정 통합/SSO
  - 팀 단위 권한 관리

## 구현 단위 (Coding 실행 단위)
- 작업 A: 세션 수집기 에이전트 기본 골격
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/agent/README.md
    - /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/collector.py
    - /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/config.py
  - 구현 상세:
    - 수집 대상 프로세스 식별 규칙 정의(Codex/ChatGPT/브라우저 기반 툴)
    - 세션 시작/종료 이벤트 모델 작성
  - 테스트:
    - 더미 이벤트 입력 시 세션 레코드 생성 확인

- 작업 B: 로컬 저장소(SQLite) 스키마/저장 로직
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/storage.py
    - /Users/mirador/Documents/ai-usage-windows-watcher/agent/sql/schema.sql
  - 구현 상세:
    - `usage_sessions`, `usage_events` 기본 테이블 설계
    - idempotent upsert/append 정책 명시
  - 테스트:
    - 동일 세션 재수집 시 중복 정책 검증

- 작업 C: CLI 점검/내보내기 초안
  - 변경 파일:
    - /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/cli.py
    - /Users/mirador/Documents/ai-usage-windows-watcher/agent/tests/test_cli.py
  - 구현 상세:
    - 일별 집계 출력 커맨드 제공(`summary --daily`)
  - 테스트:
    - 샘플 DB 기준 요약 출력 스냅샷 테스트

## 테스트 설계
- 기능 테스트:
  - 세션 감지 -> 저장 -> 요약 조회 단일 흐름 검증
- 회귀 테스트:
  - 수집 루프 장시간 실행 시 메모리/중복 레코드 점검
- 실패/예외 테스트:
  - 권한 부족/DB 잠금/대상 프로세스 미발견 시 복구 전략 검증

## 리스크 및 대응
- 리스크:
  - Windows 환경별 프로세스 식별 편차
  - 대응:
    - 프로세스 매칭 규칙을 설정 파일로 외부화
- 리스크:
  - 토큰 정확도 확보 난이도
  - 대응:
    - 1차는 추정치로 명시하고, 2차에서 API/로그 연동 고도화

## 완료 조건 (Definition of Done)
- DoD 1:
  - 로컬에서 사용 세션 샘플이 누적 저장된다.
- DoD 2:
  - CLI로 일별 요약값을 확인할 수 있다.
- DoD 3:
  - 수집 제외 항목(민감 본문 미수집) 정책이 문서에 명시된다.

## Handoff
- To Coding:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
- To Integration Test (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
- To Cycle Manager (조건부):
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md

## Planning Update (2026-02-18 16:30)
- 사용자 추가 요구:
  - Codex 사용량을 먼저 UI에서 확인
  - 최초 로그인 방식은 OAuth
  - Windows 데스크톱 프로그램 형태로 진행
- 확장 구현 단위:
  - 작업 D: Windows UI 대시보드 MVP(Tkinter)
    - 목표: 일별 Codex 사용량 테이블/요약 지표 표시
  - 작업 E: OAuth 로그인(PKCE)
    - 목표: Authorization Code + PKCE + 로컬 콜백 기반 최초 로그인
- 범위 조정 근거:
  - 기존 CLI 중심 MVP에서 UI-first 확인 흐름으로 우선순위 변경
- 검증 추가:
  - desktop UI 모듈 정적 컴파일 통과
  - OAuth 토큰 저장/로드 단위 테스트 통과

## Planning Update (2026-02-18 16:31)
- 사용자 추가 요구:
  - Windows 사용법 문서화
  - 5인치 모니터 기본 전체화면 구성
- 확장 구현 단위:
  - 작업 F: Windows 운영 가이드 문서 작성
    - 목표: PowerShell 기준 설치/실행/OAuth 설정/운영 팁 정리
  - 작업 G: 소형 화면 대응 UI 개선
    - 목표: 기본 전체화면 시작 + 소형 해상도 요약 영역 세로 배치
- 검증 추가:
  - `desktop_win/.env` 자동 로드 동작 단위 테스트 통과

## Planning Update (2026-02-18 16:33)
- 사용자 추가 요구:
  - 데이터 자동 갱신 주기를 1시간 수준으로 제한
- 확장 구현 단위:
  - 작업 H: 시간 기반 자동 새로고침 스케줄러
    - 목표: 기본 3600초 주기로 백그라운드 갱신 수행
  - 작업 I: 운영 가시성 표시
    - 목표: 마지막 갱신 시각/갱신 주기 표시
- 검증 추가:
  - refresh interval 기본값/최소값 단위 테스트 통과

## Planning Update (2026-02-22 23:21 KST) - OAuth Browser Policy (Chrome-first)
- 사용자 추가 요구:
  - OAuth 로그인을 크롬에서 진행하는지 명확화하고, 필요 시 크롬 우선 실행으로 고정
- 확장 구현 단위:
  - 작업 J: OAuth 브라우저 정책 제어
    - 목표: 기본 동작을 `chrome` 우선으로 설정하고 fallback/강제 모드를 환경변수로 제공
- 변경 파일:
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/oauth_client.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_oauth_client.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
- 세부 정책:
  - `AUIW_OAUTH_BROWSER=chrome`(기본): Chrome 우선, 실패 시 시스템 기본 브라우저 fallback
  - `AUIW_OAUTH_BROWSER=chrome_only`: Chrome으로만 실행, 실패 시 즉시 오류
  - `AUIW_OAUTH_BROWSER=default`: 시스템 기본 브라우저 사용
  - `AUIW_CHROME_PATH`: 자동 탐색 실패 시 Chrome 실행 파일 절대 경로 지정
- 검증 추가:
  - 브라우저 모드별 단위 테스트(`default`, `chrome`, `chrome_only`, invalid mode)
  - py_compile + desktop_win 테스트 통과
