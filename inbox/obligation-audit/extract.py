"""조항별 '자체 본문'을 뽑고 조동사를 판정한다.
자체 본문 = 표제 줄 다음부터, 다음 조항 표제 또는 (부속서 그룹의 경우) 표 시작 직전까지.
부속서 개별 항목은 표 행에서 뽑는다."""
import re, io
NUM = r'(?:[A-Z]\.)?\d+(?:\.\d+)*'
SHALL = [r'[아어여]야\s*한다', r'[아어여]야\s*하며', r'[아어여]야\s*함', r'해야\s*한다']
SHOULD = [r'것이\s*좋다', r'좋을\s*것이다', r'하여야\s*할\s*것이다', r'것이\s*좋을']

def clean(text):
    out=[]
    for l in text.split('\n'):
        s=l.strip()
        if re.match(r'^<!-- PDF page \d+ -->$', s): continue
        if s.startswith('[Diagonal watermark'): continue
        if re.match(r'^(KS [A-Z] ISO[^\n]{0,40}|－?\s*[ivxlc]+\s*－?|\d{1,3})$', s): continue  # 러닝헤더·쪽번호
        out.append(l)
    t='\n'.join(out)
    m=re.search(r'^해\s*설\s*$', t, re.M)      # 문서 말미 '해 설'은 표준 본문이 아니다
    return t[:m.start()] if m else t

def modals(body):
    return (any(re.search(p, body) for p in SHALL),
            any(re.search(p, body) for p in SHOULD))

def clause_bodies(path):
    """{번호: 자체본문}"""
    t = clean(io.open(path, encoding='utf-8').read())
    lines = t.split('\n')
    heads=[]                      # (idx, num)
    for i,l in enumerate(lines):
        s=l.strip()
        if re.search(r'\.{3,}|…', s): continue            # 목차
        m = re.match(r'^('+NUM+r')(?:\s{1,}|\s*$)(?!\|)', s)
        if not m: continue
        if s.startswith('|'): continue
        heads.append((i, m.group(1)))
    bodies={}
    for k,(i,num) in enumerate(heads):
        end = heads[k+1][0] if k+1 < len(heads) else len(lines)
        rest = lines[i].strip()[len(num):].strip()   # '10.2.2  조직은 …' 처럼 번호와 본문이 한 줄인 경우
        seg = [rest] + lines[i+1:end]
        # 부속서 그룹: 표가 시작되면 거기서 자체 본문 종료(표 행은 자식 항목)
        for j,l in enumerate(seg):
            if l.strip().startswith('|'):
                seg = seg[:j]; break
        bodies[num] = '\n'.join(seg).strip()   # 같은 번호가 여러 번이면 마지막(본문)이 남는다
    # 부속서 표 행 = 개별 항목
    for l in lines:
        m = re.match(r'^\|\s*('+NUM+r')\s*\|([^|]*)\|(.*)\|\s*$', l.strip())
        if m: bodies[m.group(1)] = m.group(3).strip()
    return bodies
