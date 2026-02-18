# 주제
AI Usage Watcher for Windows (윈도우 AI 사용량 워처)

## 검토 범위
- 대상 태스크: `phase1-win-agent-usage-collector`
- 비교 문서:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/docs/podonote-history/podonote-planning/tasks/phase1-win-agent-usage-collector.md`
  - `/Users/mirador/Documents/ai-usage-windows-watcher/docs/podonote-history/podonote-coding/Coding.md`
- 핵심 코드:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py`
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/oauth_client.py`
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py`
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/src/collector.py`
- 검증 실행:
  - `agent/.venv/bin/pytest -q` -> `6 passed`
  - `python3 -m py_compile desktop_win/src/*.py agent/src/*.py` -> 통과
  - 재현 스니펫(토큰 파일 손상/자동갱신 오류)으로 실패 시나리오 확인

## 문서 비교 결과
- Planning -> Coding 누락 항목:
  - 작업 A의 핵심인 "Windows 실프로세스 감지 규칙"은 아직 샘플 이벤트 주입 중심이며 실감지 루프 구현은 후속 과제로 남아 있다.
- Coding -> Planning 역추적 불가 항목:
  - 없음 (UI/OAuth/.env 자동 로드/1시간 자동 갱신 요구는 문서-코드 정합)

## 보수 검토 체크리스트
- AC 충족 여부: 부분 충족 (샘플 기반 흐름은 충족, 실프로세스 감지는 미완)
- 성능/리소스 병목 가능성: 보통 (주기성 조회 구조 단순, 실패 복원 로직 부족)
- 오류 처리/예외 케이스 누락: 있음 (토큰 파일 손상, 주기 갱신 오류)
- 테스트 전략의 빈틈: 있음 (실패 시나리오 테스트 부족)
- 기술 부채 또는 과설계 위험: 보통 (MVP 단순화는 적절하나 운영 안정성 보강 필요)
- 배포 준비 상태(Docker/환경 변수/롤백): 미흡 (Deploy 단계 산출물 미작성)

## 발견 사항
1. [중요] 토큰 파일이 손상되면 앱 시작 단계에서 바로 예외로 종료된다.
   - 근거:
     - `load_token()`이 JSON 파싱 예외를 처리하지 않음: `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/oauth_client.py:140`
     - 앱 시작 중 즉시 호출됨: `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py:47`, `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py:180`
   - 영향:
     - `%APPDATA%\\AIUsageWatcher\\oauth_token.json` 파일이 깨진 경우 UI 진입 자체가 불가능하다.
   - 재현:
     - 손상된 JSON 파일 생성 후 `load_token()` 호출 시 `JSONDecodeError` 확인.

2. [중요] 자동 갱신 콜백에서 1회 예외가 발생하면 이후 주기 갱신이 중단된다.
   - 근거:
     - `_run_periodic_refresh()`가 예외 보호 없이 다음 스케줄 등록: `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py:260`
   - 영향:
     - DB 잠금/일시 오류 발생 시 "1시간 자동 갱신" 요구가 깨지고 수동 갱신에 의존하게 된다.
   - 재현:
     - `refresh_usage_table()` 예외를 강제로 발생시키면 `_schedule_next_refresh()`가 호출되지 않음(`scheduled=False`) 확인.

3. [보통] 실프로세스 감지 목표가 아직 샘플 데이터 기록 방식에 머물러 있다.
   - 근거:
     - 수집기는 이벤트 조합기 중심: `/Users/mirador/Documents/ai-usage-windows-watcher/agent/src/collector.py:31`
     - CLI/서비스도 샘플 삽입 위주: `/Users/mirador/Documents/ai-usage-windows-watcher/agent/src/cli.py:20`, `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py:42`
   - 영향:
     - Phase 1 범위의 "Windows 사용 세션 감지" 검증은 아직 제한적이다.

## 리스크/우려
- 운영 환경에서 토큰 파일/DB 상태 이상이 발생하면 앱 안정성이 급격히 저하될 수 있다.
- 자동 갱신 중단은 비용/사용량 모니터링의 신뢰도를 낮춘다.
- 실감지 미구현 상태가 길어지면 Phase 1 완료 기준과 실제 산출물 간 괴리가 커질 수 있다.

## 되돌림 가이드
- Planning으로 되돌릴 항목:
  - 없음 (요구 자체는 명확함)
- Coding으로 되돌릴 항목:
  - `load_token()` 파손 파일 복구 전략(예: 예외 시 None 처리 + 안내 메시지)
  - `_run_periodic_refresh()`의 예외 보호/재스케줄 보장(`try/finally` 또는 실패 재시도)
  - 실패 시나리오 단위 테스트 추가(토큰 파손, 갱신 중 예외)

## 배포 게이트 판정
- Deploy 진행 가능: 아니오
- 선행 보완 필요 항목:
  - 운영 안정성 결함 2건 수정 후 Review 재검증
  - 실프로세스 감지 범위(이번 사이클 포함 여부) 결정 및 문서 정합성 반영

## Integration Test Handoff
- 통합테스트 대상 범위:
  - 보류 (Review 게이트 미통과)
- 브라우저 기반 검증 포인트:
  - OAuth 로그인 후 상태 반영, 자동 갱신 주기 유지
- 선행 보완 필요 항목:
  - Coding 보완 완료 + 회귀 테스트 증적 첨부

## 원격 반영
- push 수행 여부: 미수행
- 대상 브랜치: `main`
- 원격 저장소: `git@github.com:HeeyongPark/ai-usage-windows-watcher.git`
- push 결과: 해당 없음

## 결정/후속 조치
- 결론: `phase1-win-agent-usage-collector`는 Coding 보완 후 Review 재진입
- 즉시 액션:
  - 토큰 파손/자동갱신 오류 복원 로직 구현
  - 실패 시나리오 테스트 추가
  - 수정 후 Review 문서 업데이트 및 Integration Test (Pre) 진입 재판정
