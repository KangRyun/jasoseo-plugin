#!/usr/bin/env python3
"""자소서 글자 수·핵심 토큰 검증 (jasoseo 스킬 4·8단계 표준 계산식)

계산식: 문항별 `## 문항 N` 헤더 다음 줄부터 다음 `## `/`---`/HUMANIZE 주석 전까지,
        마크다운 `**` 제거, 개행 제외, 공백 포함 = 폼 기준값. 공백 제외도 병기.
사용:  python3 verify.py <파일.md> [필수토큰 ...] [--forbid 금지토큰 ...]
"""
import re, sys

def sections(path):
    txt = open(path, encoding='utf-8').read().split('<!-- HUMANIZE')[0]
    parts = re.split(r'^## 문항 (\d+)[^\n]*\n', txt, flags=re.M)
    for i in range(1, len(parts), 2):
        sec = parts[i + 1].split('\n## ')[0].split('\n---')[0].replace('**', '').strip()
        yield parts[i], sec

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    path = args[0]
    forbid = args[args.index('--forbid') + 1:] if '--forbid' in args else []
    keys = args[1:args.index('--forbid')] if '--forbid' in args else args[1:]
    body = ''
    for n, sec in sections(path):  # 토큰 검사는 문항 본문에서만(헤더의 변경 이력 메모 제외)
        body += sec + '\n'
        flat = sec.replace('\n', '')
        print(f"문항{n}: 제목포함·공백포함 {len(flat)} | 공백제외 {len(flat.replace(' ', ''))}")
    if keys:
        miss = [k for k in keys if k not in body]
        print("필수 토큰:", "✅ 전부 보존" if not miss else f"❌ 누락 {miss}")
    if forbid:
        hit = [k for k in forbid if k in body]
        print("금지 토큰:", "✅ 없음" if not hit else f"❌ 발견 {hit}")

if __name__ == '__main__':
    main()
