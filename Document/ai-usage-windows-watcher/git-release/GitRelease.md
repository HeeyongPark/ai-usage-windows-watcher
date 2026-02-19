# Git Release

## Subject
- ai-usage-windows-watcher

## Latest Release
- status:
  - released

## Release Run (2026-02-18 22:37 KST)

## 입력 요약
- Integration Test 게이트:
  - pass (`9 passed in 0.09s`)
- 대상 브랜치:
  - `main`

## 변경 파일
- staged files:
  - /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/storage.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/budget_rules.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_usage_service.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_budget_rules.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-desktop-dashboard.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-budget-alert-rule.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md

## Commit
- commit message:
  - `phase1: complete pre-deploy gate for dashboard and budget alerts`
- commit sha:
  - `88fd6e92bc70a84dff73f661f7de8f0312f57d5a`

## Tag
- tag name:
  - `v0.1.1-phase1`
- tag message:
  - `Phase1 git release after pre-deploy pass`
- note:
  - `v0.1.0-phase1` 태그는 이전 커밋(`79f8edf...`)에 남아 있고, 이번 릴리즈 기준 태그는 `v0.1.1-phase1`으로 확정함

## Push 결과
- branch push:
  - `79f8edf..88fd6e9  main -> main`
- tag push:
  - `[new tag] v0.1.1-phase1 -> v0.1.1-phase1`
- remote 확인:
  - `origin git@github.com:HeeyongPark/ai-usage-windows-watcher.git`

## 실패/재시도
- 실패 원인:
  - 없음
- 재시도 조건:
  - 없음

## Handoff
- pipeline 다음 단계:
  - Git Release 완료
- project override:
  - 본 프로젝트는 `git_release`를 terminal stage로 사용(Deploy/Post 단계 미진행)
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/git-release/GitRelease.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md

## Release Run (2026-02-19 22:11 KST)

## 입력 요약
- Integration Test 게이트:
  - pass (`project override ui_optional`, `15 passed in 0.09s`, py_compile 오류 없음)
- 대상 브랜치:
  - `main`

## 변경 파일
- staged files:
  - /Users/mirador/Documents/ai-usage-windows-watcher/.gitignore
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/BigPicture.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/overview/Service-Overview.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/overview/modules/04-test-strategy.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/overview/modules/05-windows-runtime-validation.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/big-picture/phases/Phase-1.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/coding/Coding.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/cycle-manager/Cycle.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/Planning.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-frozen-path-compat.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-noinstall-bundle.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/planning/tasks/phase1-windows-noinstall-smoke-evidence.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/review/Review.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/README.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/collect_windows_smoke_evidence.bat
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/run_ai_usage_watcher.bat
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/env_loader.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_env_loader.py
  - /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/test_usage_service.py

## Commit
- commit message:
  - `phase1: switch pre-deploy gate to auto-test and bundle no-install evidence flow`
- commit sha:
  - `af8af973c75365531396f7077b9fd6b246fd149b`

## Tag
- tag name:
  - `v0.1.2-phase1`
- tag message:
  - `Phase1 auto-test pre-deploy gate passed`

## Push 결과
- branch push:
  - `70551a3..af8af97  main -> main`
- tag push:
  - `[new tag] v0.1.2-phase1 -> v0.1.2-phase1`
- remote 확인:
  - `origin git@github.com:HeeyongPark/ai-usage-windows-watcher.git`

## 실패/재시도
- 실패 원인:
  - 없음
- 재시도 조건:
  - 없음

## Handoff
- pipeline 다음 단계:
  - Git Release 완료 (project terminal stage)
- project override:
  - 본 프로젝트는 `git_release`를 terminal stage로 사용(Deploy/Post 단계 미진행)
- 입력 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/git-release/GitRelease.md
- 참고 문서 위치:
  - /Users/mirador/Documents/ai-usage-windows-watcher/Document/ai-usage-windows-watcher/integration-test/IntegrationTest.md
