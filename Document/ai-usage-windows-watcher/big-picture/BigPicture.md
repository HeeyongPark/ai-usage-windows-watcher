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
- Phase 1: Windows 에이전트 + 로컬 저장 + 기본 대시보드 MVP + 무설치 실행 경로 + 테스트 게이트 확정
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
  - 2026-02-19 16:49 KST 동기화 시 Notion fetch는 인증 이슈(`Auth required`)로 실패했다.
  - 2026-02-19 17:25 KST 재시도에서 Notion 원문 + 하위 문서 2종 fetch에 성공했다.
  - Notion 원문과 로컬 파이프라인 문서를 대조한 결과, 현재 사이클 우선순위를 뒤집는 신규 상충 요구사항은 없음을 확인했다.
  - Planning/Cycle 입력 소스를 Notion 연동 상태로 복귀했다.

## Planning Input Snapshot (Latest)
- 이번 루프 핵심 내용:
  - onedir 무설치 번들/frozen 경로 호환성 보강은 완료했고 자동 테스트 기준선(`15 passed`)을 유지했다.
  - 사용자 실행 환경 제약으로 실기기 수동 스모크를 push 차단 게이트에서 제외하는 프로젝트 한정 override를 적용했다.
- 이번 사이클 방향:
  - `phase1-windows-runtime-smoke`는 `ui_optional` pre-deploy 게이트로 운영하고 자동 테스트 통과 시 git_release로 전이한다.
  - 실기기 증적 수집(`phase1-windows-noinstall-smoke-evidence`)은 권장 트랙으로 유지한다.
- 고민거리:
  - 실기기 회귀를 비차단으로 운영할 때 발견 지연 리스크를 어떻게 관리할지
  - 코드서명 전 SmartScreen/백신 오탐 대응 가이드를 어느 수준까지 문서화할지
- 고정 제약:
  - Windows 우선, 개인정보 최소 수집, 오프라인 우선 동작
  - Phase 1 배포 형식은 onedir로 고정(onefile 미지원)
  - 사용자 PC에 Python/Git/터미널 사전 설치를 요구하지 않는다.
- 성공 기준:
  - `phase1-windows-runtime-smoke` Integration Test (Pre)에서 자동 테스트가 통과한다.
  - pre-deploy pass 직후 git_release/push가 가능하다.
  - 실기기 증적은 권장 항목으로 누적 기록한다.

### Task Candidate Backlog (task-decomposer)
1. `phase1-windows-frozen-path-compat`
- 한 줄 목표:
  - onedir frozen 런타임 경로(`sys._MEIPASS`/exe dir/`_internal`)를 일관되게 해석해 import 실패를 제거한다.
- 근거 문서:
  - `./phases/Phase-1.md`
  - `./overview/Service-Overview.md`
  - `./overview/modules/04-test-strategy.md`
  - `./overview/modules/05-windows-runtime-validation.md`
- 핵심 AC/DoD:
  - `ModuleNotFoundError` 없이 앱 기동
  - frozen 경로 해석 단위 테스트 추가/통과
  - 빌드 산출물 구조와 코드 경로 전략 정합성 문서화

2. `phase1-windows-noinstall-smoke-evidence`
- 한 줄 목표:
  - Win10/Win11 실기기에서 onedir 무설치 실행 증적(체크리스트/아티팩트)을 확보한다.
- 근거 문서:
  - `./phases/Phase-1.md`
  - `./overview/modules/04-test-strategy.md`
  - `./overview/modules/05-windows-runtime-validation.md`
- 핵심 AC/DoD:
  - Win10/Win11 각 1회 onedir 실행 증적 첨부
  - 번들 구조(flat/`_internal`) 기록

3. `phase1-windows-runtime-smoke`
- 한 줄 목표:
  - `ui_optional` Integration Test (Pre) 게이트를 자동 테스트 통과 기준으로 운영한다.
- 근거 문서:
  - `./phases/Phase-1.md`
  - `./overview/modules/04-test-strategy.md`
  - `./overview/modules/05-windows-runtime-validation.md`
- 핵심 AC/DoD:
  - Gate A(자동 테스트) 충족 시 pre-deploy pass
  - Integration Test (Pre) fail 사유(실기기 증적 미첨부 차단) 해소

4. `phase1-test-harness-expansion`
- 한 줄 목표:
  - 현재 단위 테스트 중심 체계를 서비스 통합 검증 중심으로 확장한다.
- 근거 문서:
  - `./overview/modules/04-test-strategy.md`
  - `./overview/Service-Overview.md`
- 핵심 AC/DoD:
  - 자동 테스트로 Gate A를 반복 실행 가능
  - 실패 케이스(DB 경로/OAuth 설정/갱신 주기) 재현 테스트 추가

5. `phase1-oauth-live-provider-smoke`
- 한 줄 목표:
  - 실 OAuth 공급자(staging 또는 운영 테스트 계정) 기준 로그인 성공/실패 경로를 검증한다.
- 근거 문서:
  - `./overview/modules/05-windows-runtime-validation.md`
  - `./overview/modules/03-privacy-security.md`
- 핵심 AC/DoD:
  - 콜백/토큰 저장/재시작 지속성 검증
  - 실패 시 민감정보가 로그에 남지 않음을 확인

6. `phase1-release-readiness-windows`
- 한 줄 목표:
  - 새 Windows 머신에서 문서만으로 무설치 실행을 재현 가능한 배포 준비 상태를 확보한다.
- 근거 문서:
  - `./phases/Phase-1.md`
  - `./overview/modules/04-test-strategy.md`
- 핵심 AC/DoD:
  - `desktop_win/WINDOWS_USAGE.md` 절차대로 무설치 실행 재현
  - 체크리스트 증적 1회 이상 기록

### 정렬 기준 (의존성/리스크)
- 우선순위:
  - `phase1-windows-frozen-path-compat` -> `phase1-windows-noinstall-smoke-evidence` -> `phase1-windows-runtime-smoke` -> `phase1-test-harness-expansion` -> `phase1-oauth-live-provider-smoke` -> `phase1-release-readiness-windows`
- 정렬 이유:
  - frozen 경로 결함을 먼저 해결해야 실기기 증적과 통합게이트 재실행이 유효해진다.

- Planning/Cycle 입력 하위 문서:
  - `./phases/Phase-1.md`
  - `./overview/Service-Overview.md`
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

### Cycle 4 (2026-02-18 23:33)
- 이번 변경:
  - 사용자 요청(Windows 별도 설치 없이 실행)에 따라 Phase 1 요구사항에 무설치 실행 경로를 추가했다.
  - Planning Input Snapshot과 Task Candidate Backlog를 무설치 실행 우선 순서로 재정렬했다.
- 방향 변경:
  - 검증 중심 우선순위는 유지하되, "개발자 설치 경로 기준"에서 "일반 사용자 무설치 실행 기준"으로 기준점을 이동한다.
- 새 리스크:
  - 번들 파일 크기 증가, 백신 오탐, 코드 서명 부재가 초기 배포 경험을 저하시킬 수 있음
- 다음 Cycle 전달사항:
  - `phase1-windows-noinstall-bundle`을 planning으로 승격해 번들 방식(onefile/onedir) 결정을 먼저 확정한다.

### Cycle 5 (2026-02-18 23:58)
- 이번 변경:
  - onedir 무설치 번들 Coding 이후 Review에서 frozen 런타임 경로 불일치 가능성을 확인했다.
  - `phase1-windows-noinstall-bundle`을 review에서 planning으로 되돌려 재계획 항목을 확정했다.
- 방향 변경:
  - "무설치 번들 생성" 완료 기준에서 "frozen 경로 호환 + 실기기 재현" 완료 기준으로 강화했다.
- 새 리스크:
  - 경로 전략 미고정 상태로 재코딩 시 동일 결함이 반복될 수 있음
- 다음 Cycle 전달사항:
  - 런타임 경로 탐색 우선순위와 빌드 산출물 구조를 먼저 고정하고 Coding을 재진입한다.

### Cycle 6 (2026-02-19 16:49)
- 이번 변경:
  - Notion 원문 동기화를 시도했으나 인증 이슈(`Auth required`)로 직접 fetch에 실패했다.
  - 로컬 파이프라인 문서를 기준으로 Big Picture 스냅샷과 태스크 후보를 재동기화했다.
  - `phase1-windows-noinstall-bundle`을 독립 검증 단위 3개로 재분해했다.
    - `phase1-windows-frozen-path-compat`
    - `phase1-windows-noinstall-smoke-evidence`
    - `phase1-windows-runtime-smoke`(게이트 재실행)
- 방향 변경:
  - 단일 대형 태스크에서 "결함 제거 -> 실증 수집 -> 게이트 재실행" 3단 구조로 사이클을 재정렬했다.
- 새 리스크:
  - Notion 원문과 로컬 문서가 잠시 어긋날 수 있으며, 인증 복구 전까지는 로컬 문서를 기준으로 운영해야 함
- 다음 Cycle 전달사항:
  - `phase1-windows-frozen-path-compat`을 planning으로 즉시 승격해 코딩 재진입 전 결함 수정 범위를 확정한다.

### Cycle 7 (2026-02-19 17:25)
- 이번 변경:
  - Notion 인증 복구 후 원문 페이지와 하위 문서(`테스트 전략`, `Windows 실기기 검증`) fetch를 성공했다.
  - Big Picture/하위 문서/사이클 상태를 원문과 대조해 현재 태스크 분배 우선순위를 유지하기로 확정했다.
- 방향 변경:
  - "로컬 임시 기준"에서 "Notion + 로컬 파이프라인 정합 운영"으로 복귀한다.
- 새 리스크:
  - Notion 본문이 2026-02-18 기준 스냅샷이라, 최신 운영 수치(예: `12 passed`)는 로컬 문서가 더 상세하다.
- 다음 Cycle 전달사항:
  - `phase1-windows-frozen-path-compat` Coding 진입을 위해 cycle/planning 인덱스를 최신화한다.
