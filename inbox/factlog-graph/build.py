#!/usr/bin/env python3
"""factlog KB → Understand-Anything 지식그래프 (결정적 변환, LLM 없음).

사실 2,330건이 이미 그래프다 — subject·relation·object. 관계 이름을 엣지 타입으로 **보존**해
옮긴다. 문서에서 재추론하는 경로(UA 파서를 pages/ 에 겨누는 것)는 위키링크가 전부 `related` 로
뭉개져 maps_to_hls 인지 belongs_to_annex 인지가 사라지므로 쓰지 않는다.

    python3 inbox/factlog-graph/build.py          # 위키 루트에서

출력: .factlog/.ua/{knowledge-graph.json,meta.json}
루트의 .understand-anything/ 은 **건드리지 않는다** — 그쪽은 위키 문서 그래프이고 Gate C 가
article 95 / source 57 로 검증한다. 구성이 다른 그래프를 덮으면 즉시 깨진다.
"""
import csv, json, re, subprocess, datetime, pathlib, sys
from collections import defaultdict

KB = pathlib.Path(".factlog")
OUT = KB / ".ua"

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
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "knowledge-graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "meta.json").write_text(json.dumps({
        "lastAnalyzedAt": graph["project"]["analyzedAt"], "gitCommitHash": head,
        "version": "1.0.0", "analyzedFiles": len(rows),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    from collections import Counter
    print(f"facts {len(rows)} → nodes {len(nodes)} {dict(Counter(n['type'] for n in nodes))}")
    print(f"edges {len(edges)} {dict(Counter(e['type'] for e in edges))}")
    print(f"layers {len(layers)} · tour {len(tour)} · dangling 0")
    print(f"written: {OUT}/knowledge-graph.json")


if __name__ == "__main__":
    build()
