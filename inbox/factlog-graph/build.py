#!/usr/bin/env python3
"""factlog KB → Understand-Anything 지식그래프 (결정적 변환, LLM 없음).

사실 2,330건이 이미 그래프다 — subject·relation·object. 관계 이름을 엣지 타입으로 **보존**해
옮긴다. 문서에서 재추론하는 경로(UA 파서를 pages/ 에 겨누는 것)는 위키링크가 전부 `related` 로
뭉개져 maps_to_hls 인지 belongs_to_annex 인지가 사라지므로 쓰지 않는다.

    python3 inbox/factlog-graph/build.py             # .factlog/.ua/ 에 단독 그래프
    python3 inbox/factlog-graph/build.py --inject   # 위키 그래프에 사실 노드를 주입
    python3 inbox/factlog-graph/build.py --verify   # 주입이 살아 있는지 확인(없으면 exit 1)

--inject 는 루트 `.understand-anything/knowledge-graph.json` 에 사실 노드/엣지를 더한다.
표준·구조문서는 `topic` 으로, 나머지는 `entity` 로 넣고 원문 노드는 **새로 만들지 않고 위키
그래프의 것을 재사용**한다 — 그래야 cites 엣지가 두 그래프를 잇는 실제 엣지가 된다.
Gate C 는 `type == "article"` / `"source"` 만 기대집합과 대조하므로 이 주입은 게이트를 통과한다.

주의: 위키 그래프를 재생성하면 주입분이 통째로 사라지고 **어떤 게이트도 잡지 못한다**
(Gate C 는 article/source 만 본다). 그래서 재생성 절차의 마지막에 --inject 를, 그다음 --verify 를
두는 것이 이 스크립트를 쓰는 조건이다. SKILL.md 의 "Generate the graph from a git-visible copy"
참조.
"""
import csv, json, re, subprocess, datetime, pathlib, sys
from collections import defaultdict

KB = pathlib.Path(".factlog")
OUT = KB / ".ua"
WIKI_GRAPH = pathlib.Path(".understand-anything") / "knowledge-graph.json"
# 주입된 사실 노드를 식별하는 표식. --verify 가 이걸 센다.
MARK = "factlog"

# 리터럴을 목적어로 갖는 관계 — 노드가 아니라 노드의 속성으로 접는다.
ATTRIBUTE = {
    "clause_title", "obligation", "annex_status", "edition_year", "structure_family",
    "iso_edition_ordinal", "control_objective", "introduced_in_structure",
    "requires_documented_information",
}
# 온톨로지 타입 → UA 타입. 지식 뷰는 5종에만 색·범례·필터를 붙이므로 그 안에서 고른다.
UA_TYPE = {
    "standard": "article", "structure_document": "article",
    "structure_slot": "topic",
    "clause": "entity", "annex": "entity", "annex_item": "entity",
}
TYPE_RANK = ["standard", "structure_document", "annex", "structure_slot", "annex_item", "clause"]


def accepted_rows():
    with open(KB / "facts" / "candidates.csv", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r["status"] in ("accepted", "confirmed")]


def ontology_types():
    """logic_report.txt 의 instance_of 도출 결과. 엔진이 내린 타입을 그대로 쓴다."""
    types = defaultdict(set)
    report = KB / "facts" / "logic_report.txt"
    if not report.exists():
        sys.exit("logic_report.txt 가 없다 — 먼저 /factlog check 를 돌릴 것")
    for line in report.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- instance_of: (.*) \((\w+)\)$", line.strip())
        if m:
            types[m.group(1)].add(m.group(2))
    if not types:
        sys.exit("instance_of 결과가 없다 — extra.dl 의 타입 규칙을 확인할 것")
    return types


def source_id(ref):
    """위키 그래프와 같은 id 형식으로 맞춘다 — 두 그래프를 source 경로로 조인하기 위해."""
    path = ref.split("#", 1)[0]
    path = re.sub(r"^sources/", "", path)
    return "source:" + re.sub(r"\.md$", "", path)


def build():
    rows = accepted_rows()
    types = ontology_types()

    attrs = defaultdict(lambda: defaultdict(list))   # entity → relation → [objects]
    links, cites = [], defaultdict(set)
    entities = set()
    for r in rows:
        s, rel, o = r["subject"], r["relation"], r["object"]
        entities.add(s)
        cites[s].add(r["source"])
        if rel in ATTRIBUTE:
            attrs[s][rel].append(o)
        else:
            entities.add(o)
            cites[o].add(r["source"])
            links.append((s, rel, o, r["confidence"], r["note"]))

    nodes, edges = [], []
    for e in sorted(entities):
        kinds = types.get(e, set())
        primary = next((t for t in TYPE_RANK if t in kinds), "clause")
        a = attrs.get(e, {})
        title = a.get("clause_title", [None])[0]
        bits = []
        if a.get("obligation"):
            bits.append("의무: " + "/".join(sorted(set(a["obligation"]))))
        if a.get("annex_status"):
            bits.append("부속서 지위: " + a["annex_status"][0])
        if a.get("requires_documented_information"):
            bits.append("문서화된 정보 요구")
        if a.get("control_objective"):
            bits.append("목적: " + a["control_objective"][0][:80])
        if a.get("structure_family"):
            bits.append("구조: " + a["structure_family"][0])
        if a.get("edition_year"):
            bits.append("판: " + a["edition_year"][0])
        nodes.append({
            "id": "fact:" + e,
            "type": UA_TYPE[primary],
            "name": f"{e} — {title}" if title else e,
            "summary": " · ".join(bits) if bits else f"{primary} (factlog 검증 사실)",
            "tags": sorted(kinds) or [primary],
            "complexity": "simple",
        })

    for ref in sorted({s for v in cites.values() for s in v}):
        nodes.append({
            "id": source_id(ref), "type": "source",
            "name": ref.split("/")[-1],
            "summary": f"원문 캡처: {ref}",
            "tags": ["source"], "complexity": "simple",
        })

    for s, rel, o, conf, note in links:
        edges.append({
            "source": "fact:" + s, "target": "fact:" + o, "type": rel,
            "direction": "forward", "weight": float(conf or 0.9),
            "description": (note or rel)[:200],
        })
    for e in sorted(cites):
        for ref in sorted(cites[e]):
            edges.append({
                "source": "fact:" + e, "target": source_id(ref), "type": "cites",
                "direction": "forward", "weight": 0.7,
                "description": "이 엔터티의 사실이 인용한 원문",
            })

    ids = {n["id"] for n in nodes}
    dangling = [e for e in edges if e["source"] not in ids or e["target"] not in ids]
    assert not dangling, f"dangling edge {len(dangling)}건"
    assert len(ids) == len(nodes), "중복 노드 id"

    layers = [{"id": t, "name": t, "nodeIds": sorted(
        n["id"] for n in nodes if t in n["tags"])} for t in TYPE_RANK]
    layers = [l for l in layers if l["nodeIds"]]
    tour = [{"step": i + 1, "nodeId": l["nodeIds"][0], "title": l["name"],
             "description": f"{l['name']} 계층의 시작점"} for i, l in enumerate(layers)]

    head = subprocess.run(["git", "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    graph = {
        "version": "1.0.0", "kind": "knowledge",
        "project": {
            "name": "factlog KB", "languages": ["datalog"], "frameworks": ["factlog"],
            "description": "factlog 가 검증한 사실에서 결정적으로 변환한 그래프 (LLM 추론 없음)",
            "analyzedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "gitCommitHash": head,
        },
        "nodes": nodes, "edges": edges, "layers": layers, "tour": tour,
    }
    from collections import Counter
    print(f"facts {len(rows)} → nodes {len(nodes)} {dict(Counter(n['type'] for n in nodes))}")
    print(f"edges {len(edges)} {dict(Counter(e['type'] for e in edges))}")
    print(f"layers {len(layers)} · tour {len(tour)} · dangling 0")
    return graph


def write_standalone(graph):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "knowledge-graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "meta.json").write_text(json.dumps({
        "lastAnalyzedAt": graph["project"]["analyzedAt"],
        "gitCommitHash": graph["project"]["gitCommitHash"],
        "version": "1.0.0", "analyzedFiles": len(graph["nodes"]),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"written: {OUT}/knowledge-graph.json")


def inject(graph):
    """위키 그래프에 사실 노드/엣지를 더한다. 멱등 — 이미 있는 id 는 건너뛴다."""
    if not WIKI_GRAPH.exists():
        sys.exit(f"{WIKI_GRAPH} 가 없다 — 먼저 위키 그래프를 생성할 것")
    wiki = json.loads(WIKI_GRAPH.read_text(encoding="utf-8"))
    ids = {n["id"] for n in wiki["nodes"]}
    added = 0
    for n in graph["nodes"]:
        if n["type"] == "source":          # 위키 그래프의 원문 노드를 재사용한다
            continue
        if n["id"] in ids:
            continue
        m = dict(n)
        m["type"] = "topic" if n["type"] == "article" else n["type"]
        m["tags"] = sorted(set(m["tags"]) | {MARK, "verified"})
        wiki["nodes"].append(m); ids.add(m["id"]); added += 1
    have = {(e["source"], e["target"], e["type"]) for e in wiki["edges"]}
    kept = [e for e in graph["edges"]
            if e["source"] in ids and e["target"] in ids
            and (e["source"], e["target"], e["type"]) not in have]
    wiki["edges"].extend(kept)
    WIKI_GRAPH.write_text(json.dumps(wiki, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
    from collections import Counter
    print(f"injected: nodes +{added}, edges +{len(kept)}")
    print(f"  wiki graph now {len(wiki['nodes'])} nodes "
          f"{dict(Counter(n['type'] for n in wiki['nodes']))}, {len(wiki['edges'])} edges")


def verify():
    """재생성이 주입분을 지웠는지 본다. Gate C 는 article/source 만 보므로 이걸 잡지 못한다."""
    if not WIKI_GRAPH.exists():
        sys.exit(f"{WIKI_GRAPH} 가 없다")
    wiki = json.loads(WIKI_GRAPH.read_text(encoding="utf-8"))
    n = sum(1 for x in wiki["nodes"] if MARK in x.get("tags", []))
    print(f"wiki graph 안의 factlog 사실 노드: {n}")
    if n == 0:
        sys.exit("사실 노드가 없다 — 그래프 재생성이 주입분을 지웠다. "
                 "`build.py --inject` 를 다시 돌릴 것")
    return 0


if __name__ == "__main__":
    if "--verify" in sys.argv:
        raise SystemExit(verify())
    g = build()
    if "--inject" in sys.argv:
        inject(g)
    else:
        write_standalone(g)
