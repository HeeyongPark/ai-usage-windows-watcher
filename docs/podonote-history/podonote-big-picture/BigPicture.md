# 주제
AI Usage Watcher for Windows (윈도우 AI 사용량 워처)

## 문서 구조 원칙
- Track A (Phase 실행 트랙):
  - 경로: `./phases/`
  - 역할: 단계별 구현 범위와 릴리즈 기준 정의
- Track B (기능/운영 모듈 트랙):
  - 경로: `./overview/modules/`
  - 역할: 수집 대상, 개인정보 보호, 지표/리포트 기준 정의
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
- Phase 1: Windows 에이전트 + 로컬 저장 + 기본 대시보드 MVP
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

## Notion 구조 동기화 상태
- 소스 페이지:
  - https://www.notion.so/mirador/30be497bcfdf807a877bdccfbdcbd8c4?source=copy_link
- 동기화 결과:
  - 2026-02-18 16:06 KST 기준 프로젝트 본문(비전/로드맵/첫 사이클 태스크) 반영 완료
  - 로컬 Big Picture와 Notion 초기 스코프 정합성 확보

## Planning Input Snapshot (Latest)
- 이번 루프 핵심 내용:
  - 프로젝트 초기화 후 Phase 1 첫 태스크(사용량 수집기 MVP) Planning 문서를 확정한다.
- 이번 사이클 방향:
  - 로컬 우선 수집, 최소 권한, 재현 가능한 설치/실행 절차를 우선한다.
- 고민거리:
  - 수집 가능한 신뢰 지표(세션 시간/요청 수/토큰 추정치) 범위 확정
- 고정 제약:
  - Windows 우선, 개인정보 최소 수집, 오프라인 우선 동작
- 성공 기준:
  - Cycle/Planning 문서가 생성되고 첫 실행 태스크가 `planning` 상태로 진입한다.
- Planning/Cycle 입력 하위 문서:
  - ./phases/Phase-1.md
  - ./overview/modules/01-collection-policy.md
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
