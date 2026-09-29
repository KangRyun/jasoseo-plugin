#!/usr/bin/env python3
"""
문체 검사 (references/문체_금지규칙.md, 2026-09-29 개정판)
  1) 금지 — 2절 목록. 0건이어야 한다(히트가 있으면 종료 코드 1)
  2) 범위 — 4절 빈도 기준. 합격작 1,080건 범위를 벗어나면 ⚠(고치거나 `## 참고`에 사유 기록)
사용:  python3 style_check.py <파일.md> [--all]
  기본: `## 문항 N` 섹션별 검사(verify.py와 같은 분할, `[...]` 소제목 줄은 범위 계산에서 뺌). --all: 파일 전체를 한 덩어리로.
정규식은 1차 필터다. 0건이어도 정의로 재독하고, 히트가 문맥상 정당하면 사람이 판단한다.
"""
import os, re, statistics, sys
sys.path.insert(0, os.path.dirname(__file__))
from verify import sections

# ── 1) 금지 (2절) ──
RULES = {
    '번역투': [
        r'되어졌', r'에 의해', r'에 있어서(?![가-힣])', r'함에 있어', r'에 대한 [가-힣]+을 (진행|수행)', r'을 가지게 되',
        r'(관심|열정|책임감)을 가지', r'를 통해 (성장|배웠|느꼈|깨달)', r'으?로부터', r'에게 있어', r'것으로 보여집니다',
        r'생각되어집니다', r'(저|제|나)의 경우', r'적인 측면에서', r'하는 것을 (진행|수행)', r'수행을 완료',
        r'[가-힣]+(은|는|이|가) (저|나)에게 [가-힣 ]*(가르쳐|알려|깨닫게|보여) ?주',
    ],
    '상투어': [
        r'끊임없이', r'최선을 다', r'밤낮', r'누구보다', r'항상 고민', r'열정을', r'책임감을 갖', r'적극적으로 소통',
        r'밑거름', r'발판', r'한 걸음 더', r'값진 경험', r'소중한 경험', r'많은 것을 배', r'성장할 수 있었', r'한층 성장',
        r'시야를 넓', r'시너지', r'든든한', r'하나 된', r'원활한 소통', r'팀워크를 발휘', r'뼈를 묻', r'평생 헌신',
        r'최고의 전문가', r'발전에 이바지', r'미래를 선도', r'심도 있는', r'폭넓은', r'체계적인', r'성공적으로',
    ],
    '일반명제': [  # 구 잠언체: 추상 개념이 주어인 진리 선언. "저는 ~을 배웠습니다"는 해당 없음(3-3)
        r'(신뢰|준비|의지|혁신|품질|책임|성장|본질|정답|원칙|열정|노력|성공|실패|기술|개발|운영|협업|소통|안정성|데이터|사람|일)(은|는|이란|란) [가-힣 ,]+(입니다|이다|됩니다|된다|나옵니다|나온다|갈립니다|갈린다)[\.,]',
        r'(은|는) 결국', r'에서 (나온다|나옵니다|갈린다|갈립니다|시작된다|시작됩니다)',
        r'(보다|아니라) [가-힣 ]+(가|이) 중요(합니다|하다)', r'만이 [가-힣 ]+수 있', r'없는 [가-힣]+(은|는) [가-힣 ]+(된다|됩니다)',
    ],
    '빈결의': [  # 구 코다체: 구체 업무 없는 결의, 신념 선언, 요약 반복, 대구 수사
        r'(라고|이라고|다고) (믿습니다|확신합니다)\.', r'(가|이) 제 (기준|원칙|신념)입니다\.', r'오래 하고 싶습니다',
        r'기여하겠습니다', r'보답하겠습니다', r'이바지하겠습니다', r'함께 성장하',
        r'(인재|전문가|개발자|엔지니어|사람|일원)(가|이|으로|로) (되겠습니다|거듭나겠습니다|성장하겠습니다)',
        r'역시 [가-힣 ]+(라고|이라고) (믿|생각)',
        r'(에서도|때도) [가-힣 ,]*(이 원칙|이 기준|이 자세|이 태도)[가-힣 ,]*(지키겠습니다|이어가겠습니다|잃지 않겠습니다)',
        r'이렇게 저는', r'(으로|로) 답하겠습니다', r'(으로|로) 증명하겠습니다',
    ],
    '중간점': [r'[·∙・‧]'],  # 2026-09-28
    '금지어휘': [r'세우|세운|세워|세웠', r'단독', r'(순서|구조|상황|갈래|층|설계|사례|몫|점|일|것)입니다\.'],  # 2026-09-29 오전
    '구어종결': [r'판이었습니다', r'해\s?봤습니다', r'들여다보니'],  # 2026-09-16
    '약점고백': [r'(한|해 본|다뤄 본) 적이 없', r'(배우|학습하)지 않은', r'부족한 (제가|저는|저)', r'경험이 없(어|습니다|는)'],  # 2026-09-21
}
LAST_SENTENCE = r'(라고|이라고|다고) (생각합니다|믿습니다|확신합니다)\.?$'  # 마지막 문장만 신념 선언 금지(3-5)

# ── 2) 범위 (4절) ──
NUM_UNIT = r'\d+(?:[.,]\d+)*\s*(?:%|초|ms|분|시간|일|주|개월|건|개|명|배|위|점|회|줄|커밋|MB|GB|rps|VU|곳|종|단계|차)'
PAIR = r'(?:' + NUM_UNIT + r')\s*(?:에서|→|->)\s*(?:' + NUM_UNIT + r')'  # 전후 비교 쌍은 1개로 센다
LATIN = r'[A-Za-z][A-Za-z0-9+#.\-/]*'
FIRST = r'(?:(?<=\s)|^)(?:저는|저도|저의|저를|저에게|저만|제가|제게|제\s|나는|내가|나의)'
CONNECT = r'(?:^|\s)(?:또한|특히|이를 통해|이를 바탕으로|이를 위해|따라서|그래서|그 결과|결과적으로|이처럼|이러한|하지만|그러나|그런데)'
TICS = {'먼저': r'먼저', '같은': r'(?:^|\s)같은', '직접': r'직접', '끝까지': r'끝까지', '~가 아니라': r'(?:이|가) 아니라',
        '~기 전에': r'기 전에', '~한 뒤': r'[한은] 뒤'}


def scan(text):
    hits = []
    for cat, pats in RULES.items():
        for p in pats:
            for m in re.finditer(p, text, flags=re.M):
                s, e = max(0, m.start() - 25), min(len(text), m.end() + 15)
                hits.append((cat, text[s:e].replace('\n', ' ')))
    return hits


def body_lines(sec):
    return [l.strip() for l in sec.split('\n') if l.strip() and not re.match(r'^\[.*\]$', l.strip())]


def sentences(lines):
    return [s.strip() for l in lines for s in re.split(r'(?<=[\.!?])\s+', l) if len(s.strip()) > 5]


def ranges(sec):
    lines = body_lines(sec)
    body = '\n'.join(lines)
    n = max(len(body.replace('\n', '')), 1)
    ss = sentences(lines)
    per = lambda pat: 1000 * len(re.findall(pat, body, re.M)) / n
    out = []  # (이름, 값 문자열, 통과 여부, 기준)
    v = 1000 * (len(re.findall(NUM_UNIT, body)) - len(re.findall(PAIR, body))) / n
    out.append(('측정 수치(전후 쌍=1)', f'{v:.1f}/1,000자', v <= 4.5, '≤4.5'))
    v = per(LATIN); out.append(('영문 용어', f'{v:.1f}/1,000자', v <= 14, '≤14'))
    d = len({w.lower() for w in re.findall(LATIN, body)}); out.append(('서로 다른 영문 용어', f'{d}개', d <= 7, '≤7'))
    if ss:
        dense = 100 * sum(len(re.findall(LATIN, s)) >= 2 or len(re.findall(r'\d+(?:[.,]\d+)*', s)) >= 2 for s in ss) / len(ss)
        out.append(('빽빽한 문장', f'{dense:.0f}%', dense <= 25, '≤25%'))
        med = statistics.median(len(s) for s in ss)
        out.append(('문장 길이 중앙값', f'{med:.0f}자', 50 <= med <= 75, '50~75자'))
    v = per(FIRST); out.append(('1인칭', f'{v:.1f}/1,000자', 1 <= v <= 5, '1~5'))
    c = len(re.findall(CONNECT, body, re.M)); out.append(('연결어', f'{c}회', c >= 1, '≥1'))
    tics = {k: len(re.findall(p, body, re.M)) for k, p in TICS.items()}
    over = {k: c for k, c in tics.items() if c > 1}
    out.append(('말버릇', ', '.join(f'{k} {c}회' for k, c in over.items()) or '없음', not over, '표현당 ≤1'))
    keys = [re.sub(r'[\.!?"”\'’)\]]+$', '', s)[-4:] for s in ss]
    run = next((ss[i + 2][-30:] for i in range(len(keys) - 2) if keys[i] == keys[i + 1] == keys[i + 2]), None)
    out.append(('같은 종결 3연속', run and f'…{run}' or '없음', run is None, '없음'))
    return out, ss


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    path = args[0]
    if '--all' in args:
        blocks = [('전체', open(path, encoding='utf-8').read())]
    else:
        blocks = list(sections(path)) or [('전체', open(path, encoding='utf-8').read())]
    hard = warn = 0
    for n, sec in blocks:
        hits = scan(sec)
        rs, ss = ranges(sec)
        if ss and re.search(LAST_SENTENCE, ss[-1]):
            hits.append(('빈결의', '마지막 문장이 신념 선언: …' + ss[-1][-40:]))
        bad = [r for r in rs if not r[2]]
        hard += len(hits); warn += len(bad)
        print(f"문항{n}: 금지 {'✅ 0건' if not hits else f'❌ {len(hits)}건'} | 범위 {'✅' if not bad else f'⚠ {len(bad)}건'}")
        for cat, ctx in hits:
            print(f"  [{cat}] …{ctx}…")
        for name, val, _, tgt in bad:
            print(f"  [범위] {name} {val} (기준 {tgt})")
    print(f"\n금지 {hard}건 · 범위 경고 {warn}건 — 금지는 0건이어야 한다. 범위 경고는 고치거나 `## 참고`에 사유를 적는다. 0건이어도 문체_금지규칙.md 정의로 재독할 것")
    sys.exit(1 if hard else 0)


if __name__ == '__main__':
    main()
