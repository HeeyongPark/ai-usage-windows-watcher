# 주제
AI Usage Watcher for Windows (윈도우 AI 사용량 워처)

## 문서 구조 원칙
- Track A (Phase 실행 트랙):
  - 경로: `./phases/`
  - 역할: 단계별 구현 범위와 릴리즈 기준 정의
- Track B (기능/운영 모듈 트랙):
  - 경로: `./overview/modules/`
  - 역할: 수집 대상, 정책, 지표, 테스트/운영 검증 기준 정의
- 중복 방지 규칙:
  - 실행 항목은 `phases`, 정책/요건은 `overview/modules`에 작성

## 제품 비전
윈도우 환경에서 AI 도구(Codex, ChatGPT 등) 사용량을 로컬 우선으로 수집/분석해 비용과 생산성을 함께 관리하는 사용량 관측 플랫폼을 만든다.

## 코드 저장소
- remote: `git@github.com:HeeyongPark/ai-usage-windows-watcher.git`
- local: `/Users/mirador/Documents/ai-usage-windows-watcher`

## 장기 목표 (North Star)
- 도구/모델별 사용량(요청 수, 토큰, 세션 시간) 가시화
- 예산 임계치 알림과 주간 리포트 자동화
- 로컬 우선 저장 + 선택적 클라우드 동기화 구조 확립

## 비목표 (Out of Scope)
- 초기 단계에서 macOS/Linux 동시 지원
- 키 입력/화면 캡처 기반의 침습형 모니터링
- 기업용 멀티테넌트 권한 체계

## 현재 단계 로드맵
- Phase 1: Windows 에이전트 + 로컬 저장 + 기본 대시보드 MVP + 테스트 게이트 확정
- Phase 2: 비용/예산 알림 + 리포트 내보내기
- Phase 3: 팀 단위 정책/프로필 + 동기화 옵션
- Phase 4: 사용 패턴 분석/추천 자동화

## 하위 문서 인덱스
- [Phase 1](./phases/Phase-1.md)
- [Phase 2](./phases/Phase-2.md)
- [Phase 3](./phases/Phase-3.md)
- [Phase 4](./phases/Phase-4.md)

## 기능/운영 모듈 인덱스
- [서비스 개요](./overview/Service-Overview.md)
- [수집 정책](./overview/modules/01-collection-policy.md)
- [지표 정의](./overview/modules/02-metrics-definition.md)
- [개인정보/보안 원칙](./overview/modules/03-privacy-security.md)
- [테스트 전략](./overview/modules/04-test-strategy.md)
- [Windows 실기기 검증](./overview/modules/05-windows-runtime-validation.md)

## Notion 구조 동기화 상태
- source 매핑 파일:
  - `Document/ai-usage-windows-watcher/_meta/notion-sources.yaml`
- 소스 페이지:
  - https://www.notion.so/mirador/30be497bcfdf807a877bdccfbdcbd8c4?source=copy_link
- 동기화 결과:
  - 2026-02-18 22:49 KST 기준 Notion 본문 + 로컬 Big Picture 정합성 점검 완료
  - 테스트/Windows 검증 하위 문서(04, 05) 추가 반영 대기 상태

## Planning Input Snapshot (Latest)
- 이번 루프 핵심 내용:
  - 기능 MVP는 구현되었고 로컬 단위 테스트(`9 passed`)도 확보되었지만, Windows 실기기 기반 검증 증적이 부족하다.
- 이번 사이클 방향:
  - 테스트 자동화 범위를 넓히고, Windows 10/11 실기기 스모크를 표준 체크리스트로 고정한다.
- 고민거리:
  - OAuth 공급자 실연동 테스트를 어디까지 자동화할지
  - 소형 해상도에서 UI 가독성을 수치화할지 여부
- 고정 제약:
  - Windows 우선, 개인정보 최소 수집, 오프라인 우선 동작
- 성공 기준:
  - 테스트/실기기 검증 하위 문서가 생성되고 Notion 하위 페이지로 동기화된다.
  - Phase 1 테스트 게이트의 자동/수동 검증 항목이 Planning 입력으로 사용 가능해진다.

### Task Candidate Backlog (task-decomposer)
1. `phase1-windows-runtime-smoke`
- 한 줄 목표:
  - Win10/Win11 실기기에서 설치~OAuth~집계~예산알림까지 스모크를 증적과 함께 완료한다.
- 근거 문서:
  - `./phases/Phase-1.md`
  - `./overview/modules/05-windows-runtime-validation.md`
- 핵심 AC/DoD:
  - 필수 시나리오 6개 모두 pass 또는 실패 원인/재현 절차 기록
  - P0 이슈 0건

2. `phase1-test-harness-expansion`
- 한 줄 목표:
  - 현재 단위 테스트 중심 체계를 서비스 통합 검증 중심으로 확장한다.
- 근거 문서:
  - `./overview/modules/04-test-strategy.md`
  - `./overview/Service-Overview.md`
- 핵심 AC/DoD:
  - 자동 테스트로 Gate A를 반복 실행 가능
  - 실패 케이스(DB 경로/OAuth 설정/갱신 주기) 재현 테스트 추가

3. `phase1-oauth-live-provider-smoke`
- 한 줄 목표:
  - 실 OAuth 공급자(staging 또는 운영 테스트 계정) 기준 로그인 성공/실패 경로를 검증한다.
- 근거 문서:
  - `./overview/modules/05-windows-runtime-validation.md`
  - `./overview/modules/03-privacy-security.md`
- 핵심 AC/DoD:
  - 콜백/토큰 저장/재시작 지속성 검증
  - 실패 시 민감정보가 로그에 남지 않음을 확인

4. `phase1-release-readiness-windows`
- 한 줄 목표:
  - 새 Windows 머신에서 문서만으로 재현 설치 가능한 배포 준비 상태를 확보한다.
- 근거 문서:
  - `./phases/Phase-1.md`
  - `./overview/modules/04-test-strategy.md`
- 핵심 AC/DoD:
  - `desktop_win/WINDOWS_USAGE.md` 절차대로 설치/실행 재현
  - 체크리스트 증적 1회 이상 기록

### 정렬 기준 (의존성/리스크)
- 우선순위:
  - `phase1-windows-runtime-smoke` -> `phase1-test-harness-expansion` -> `phase1-oauth-live-provider-smoke` -> `phase1-release-readiness-windows`
- 정렬 이유:
  - 실기기 기본 동작(P0)을 먼저 닫아야 자동화/릴리즈 기준이 의미를 가진다.

- Planning/Cycle 입력 하위 문서:
  - `./phases/Phase-1.md`
  - `./overview/modules/04-test-strategy.md`
  - `./overview/modules/05-windows-runtime-validation.md`
  - https://www.notion.so/mirador/30be497bcfdf807a877bdccfbdcbd8c4?source=copy_link

## Cycle History
### Cycle 1 (2026-02-18 16:03)
- 이번 변경:
  - 새 subject(`ai-usage-windows-watcher`)를 생성하고 Big Picture/Cycle/Planning 초기 골격을 구성했다.
- 방향 변경:
  - Notion 원문이 비어 있어 로컬 초안 기준으로 사이클을 시작한다.
- 새 리스크:
  - 원문 요구사항 공백으로 MVP 범위가 추정 기반이 될 수 있음
- 다음 Cycle 전달사항:
  - Notion 본문을 채운 뒤 Big Picture 동기화를 재실행한다.

### Cycle 2 (2026-02-18 16:06)
- 이번 변경:
  - Notion 페이지 제목을 `AI Usage Watcher for Windows (윈도우 AI 사용량 워처)`로 확정했다.
  - Notion 본문에 프로젝트 개요, 로드맵, 수집 정책, 첫 사이클 태스크를 작성했다.
- 방향 변경:
  - 로컬 초안 상태에서 Notion 원문 기반 동기화 가능한 상태로 전환했다.
- 새 리스크:
  - 추정 기반 지표(`token_estimate`) 정의가 실제 구현 단계에서 변경될 수 있음
- 다음 Cycle 전달사항:
  - `phase1-win-agent-usage-collector` Coding 진입 전 지표 수집 정밀도 기준을 확정한다.

### Cycle 3 (2026-02-18 22:49)
- 이번 변경:
  - 테스트/Windows 실기기 검증을 위한 하위 문서 2종을 추가했다.
    - `./overview/modules/04-test-strategy.md`
    - `./overview/modules/05-windows-runtime-validation.md`
  - Planning Input Snapshot을 검증 중심 task 후보로 재정렬했다.
  - Notion source 매핑(`_meta/notion-sources.yaml`)을 복구했다.
- 방향 변경:
  - 기능 추가 중심에서 "Windows 실제 동작 검증 + 테스트 게이트 확정" 중심으로 우선순위를 이동한다.
- 새 리스크:
  - 실 OAuth 공급자 테스트 계정/환경이 준비되지 않으면 Gate C 지연 가능
- 다음 Cycle 전달사항:
  - `phase1-windows-runtime-smoke`를 우선 Planning으로 승격해 실기기 증적을 먼저 확보한다.
