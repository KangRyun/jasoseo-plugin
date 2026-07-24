# jasoseo — 한국 자기소개서 작성 파이프라인 (Claude Code 플러그인)

기업 조사 → 채용 공고/문항 분석 → 초안 → 글자 수 조정 → 전문가 리뷰 → 반영 → 윤문 → 최종 검증까지 8단계로 자기소개서를 완성하는 Claude Code 플러그인입니다. 신입·인턴 지원자가 여러 회사에 반복 지원할 때 생기는 문제(소재 중복, 경험 과장, 글자 수 미달, 회사별 폴더 정리)를 자동화합니다.

## 설치

로컬에서 바로 써보려면:

```
/plugin marketplace add /home/kr9370/jasoseo-plugin
/plugin install jasoseo@jasoseo-marketplace
```

GitHub에 올린 뒤라면:

```
/plugin marketplace add <github-user>/jasoseo-plugin
/plugin install jasoseo@jasoseo-marketplace
```

## 사용법

지원자 워크스페이스(작업 폴더)에 `이력서.md`를 두고, `PROFILE.md`(선택, 템플릿은 `skills/jasoseo/references/profile-template.md`)를 채운 뒤:

```
/jasoseo <회사명>
```

특정 단계부터 이어가려면:

```
/jasoseo <회사명> 리뷰
```

## 권장 companion 플러그인

7단계(윤문)에서 자연스러운 한국어 다듬기를 위해 [`humanize-korean`](https://github.com/epoko77-ai/im-not-ai) 플러그인이 설치되어 있으면 자동으로 활용합니다. 없어도 동작하지만(자체 윤문으로 대체), 설치를 권장합니다.

## 구성

- `skills/jasoseo/` — 8단계 파이프라인 오케스트레이션 스킬
- `agents/jasoseo-researcher.md` — 1단계(기업 조사) 전용 에이전트
- `agents/jasoseo-reviewer.md` — 5단계(전문가 리뷰) 전용 에이전트

## 라이선스

MIT
