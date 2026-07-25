# 기여 가이드 (Contributing)

jasoseo에 관심 가져주셔서 감사합니다. 버그 제보, 개선 제안, 자기 상황에 맞춘 수정 모두 환영합니다.

## 먼저 이해하면 좋은 설계 원칙

이 플러그인은 몇 가지 원칙 위에 서 있습니다. 기여 시 이 원칙을 깨지 않는 방향으로 제안해 주세요.

1. **사실만 쓴다.** 자소서 소재는 사용자의 이력서에 있는 실제 경험만 사용합니다. "더 그럴듯하게 지어내는" 기능은 이 프로젝트의 방향과 반대입니다.
2. **경험 귀속을 지킨다.** 팀 프로젝트에서 본인이 안 한 일을 본인 성과로 쓰지 않도록 돕는 게 핵심 가치입니다.
3. **개인 데이터는 코드에 넣지 않는다.** 특정 사용자의 이력·회사·수치는 스킬/에이전트/README에 하드코딩하지 않습니다. 그런 맥락은 사용자별 `PROFILE.md`로 분리합니다.
4. **컨텍스트는 공공재다.** `SKILL.md` 본문은 간결하게(가급적 500줄 이내) 유지하고, 상세한 내용은 `references/`로 분리합니다.

## 리포지터리 구조

```
jasoseo-plugin/
├── .claude-plugin/
│   ├── plugin.json          # 플러그인 매니페스트
│   └── marketplace.json     # 로컬/원격 설치용 마켓플레이스 정의
├── skills/jasoseo/
│   ├── SKILL.md             # 8단계 파이프라인 (핵심)
│   └── references/
│       └── profile-template.md
├── agents/
│   ├── jasoseo-researcher.md
│   └── jasoseo-reviewer.md
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## 로컬에서 개발·테스트하기

1. 이 저장소를 클론합니다.
2. 로컬 마켓플레이스로 등록하고 설치합니다.
   ```
   /plugin marketplace add /경로/jasoseo-plugin
   /plugin install jasoseo@jasoseo-marketplace
   ```
3. **중요 — 설치본은 소스의 복사본입니다.** 설치 시 소스가 `~/.claude/plugins/cache/...`로 복사되므로, 소스 파일을 수정한 뒤에는 재설치해야 반영됩니다.
   ```
   claude plugin uninstall jasoseo
   claude plugin marketplace remove jasoseo-marketplace
   claude plugin marketplace add /경로/jasoseo-plugin
   claude plugin install jasoseo@jasoseo-marketplace
   ```
   반영 여부는 `diff -rq` 로 소스와 캐시를 비교해 확인할 수 있습니다.

## 변경 전 검증

매니페스트가 유효한지 확인합니다.

```
claude plugin validate /경로/jasoseo-plugin
```

에이전트 정의를 수정했다면 frontmatter에 `name` / `description` / `model` / `tools`가 모두 있는지 확인하세요 — 이 네 필드가 실제 작동하는 플러그인 에이전트의 표준 형식입니다.

## 커밋과 PR

- 커밋 메시지는 **무엇을, 왜** 바꿨는지 한 줄 요약 + 필요 시 본문으로 설명합니다.
- 사용자에게 보이는 변경(스킬 동작, 인자 규칙, 파일 산출물 등)은 `CHANGELOG.md`의 `[Unreleased]` 섹션에 기록합니다.
- 하나의 PR은 하나의 주제만 다루는 것이 리뷰에 좋습니다.

## 버그 제보 / 제안

이슈를 열 때 다음이 있으면 도움이 됩니다.
- 무엇을 하려 했고, 무엇이 일어났는지
- 재현 방법 (입력한 명령, 공고 유형 등)
- 기대한 결과와 실제 결과의 차이

감사합니다. 여러분의 자소서가 잘 되길 바랍니다.
