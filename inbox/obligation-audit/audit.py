#!/usr/bin/env python3
"""`obligation` 사실을 raw 캡처와 대조한다.

자체검증 규칙: 이미 수락된 obligation 행을 추출기가 전부 재현해야 한다.
'재현 실패'가 0이 아니면 추출기가 틀린 것이므로, 그 상태로 나온 '결손 후보'는 믿지 말 것.

    python3 inbox/obligation-audit/audit.py          # 위키 루트에서
"""
import csv, sys, pathlib
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from extract import clause_bodies, modals

FILES = {
    'KS X ISO/IEC 27001:2013': 'raw/papers/ks-x-iso-iec-27001-20241030-ko-llmvision.md',
    'KS Q ISO 9001:2015':      'raw/papers/ks-q-iso-9001-20241213-ko-llmvision.md',
    'KS X ISO/IEC 42001:2023': 'raw/papers/ks-x-iso-iec-42001-20251030-ko-llmvision.md',
    'KS I ISO 14001:2015':     'raw/papers/ks-i-iso-14001-20210928-ko-llmvision.md',
}
# 본문의 종결 술어가 '좋다' 라서 shall 로 볼 수 없는 문장 (2026-09-11 판단)
EXCLUDED = {('KS X ISO/IEC 42001:2023 B.6.2.2', 'shall')}


def main():
    acc = [r for r in csv.DictReader(open('.factlog/facts/candidates.csv'))
           if r['status'] in ('accepted', 'confirmed')]
    has, ob = defaultdict(set), defaultdict(set)
    for r in acc:
        if r['relation'] == 'has_clause': has[r['subject']].add(r['object'])
        if r['relation'] == 'obligation': ob[r['subject']].add(r['object'])

    unreproduced, gaps = [], []
    for std, path in FILES.items():
        bodies = clause_bodies(path)
        for clause in sorted(has[std]):
            body = bodies.get(clause[len(std) + 1:])
            if body is None:
                continue
            found = dict(zip(('shall', 'should'), modals(body)))
            for mod, present in found.items():
                if mod in ob[clause] and not present:
                    unreproduced.append((clause, mod))
                elif present and mod not in ob[clause] and (clause, mod) not in EXCLUDED:
                    gaps.append((clause, mod, body[:90]))

    print(f'재현 실패: {len(unreproduced)}')
    for c, m in unreproduced:
        print(f'  {c} [{m}]')
    print(f'결손 후보: {len(gaps)}')
    for c, m, snip in gaps:
        print(f'  {c} [{m}] {snip}')
    assert not unreproduced, '추출기가 수락된 행을 재현하지 못한다 — 결손 후보를 신뢰하지 말 것'
    return 1 if gaps else 0


if __name__ == '__main__':
    raise SystemExit(main())
