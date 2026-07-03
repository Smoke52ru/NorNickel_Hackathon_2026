import re

from .graph_store import NetworkxGraphStore


def _norm(name):
    return re.sub(r"\s+", " ", name.strip().lower())


def _nid(name):
    return re.sub(r"\W+", "_", _norm(name)).strip("_")[:60]


def _add_source(node, doc_id):
    srcs = node.setdefault("sources", [])
    if doc_id not in srcs:
        srcs.append(doc_id)


def add_extraction(graph, extraction, doc_id, meta=None):
    g = graph.g

    for e in extraction.get("entities", []):
        name = e.get("name")
        if not name:
            continue
        eid = _nid(name)
        if eid in g:
            _add_source(g.nodes[eid], doc_id)
        else:
            graph.add_entity(eid, e.get("type", "Unknown"), name,
                             geo=e.get("geo", "unknown"), sources=[doc_id])

    for r in extraction.get("relations", []):
        s, t = r.get("source"), r.get("target")
        if not s or not t:
            continue
        sid, tid = _nid(s), _nid(t)
        for nid, nm in ((sid, s), (tid, t)):
            if nid not in g:
                graph.add_entity(nid, "Unknown", nm, sources=[doc_id])
        graph.add_relation(sid, tid, r.get("relation", "related"), source=doc_id)

    for num in extraction.get("numbers", []):
        prop = num.get("property")
        if not prop:
            continue
        pid = _nid(prop)
        if pid not in g:
            graph.add_entity(pid, "Property", prop, measurements=[], sources=[doc_id])
        else:
            _add_source(g.nodes[pid], doc_id)
        g.nodes[pid].setdefault("measurements", []).append(
            {"op": num.get("op"), "value": num.get("value"),
             "unit": num.get("unit"), "source": doc_id})


def build_graph(documents, extractor, llm):
    graph = NetworkxGraphStore()
    for doc in documents:
        add_extraction(graph, extractor(doc["text"], llm), doc["doc_id"], doc)
    return graph
