def _sources(node):
    return set(node.get("sources") or [])


def find_contradictions(graph):
    g = graph.g
    result = []

    for u, v, key, d in g.edges(keys=True, data=True):
        if d.get("rel") == "contradicts":
            result.append({
                "about": g.nodes[u].get("name", u),
                "between": [g.nodes[u].get("name", u), g.nodes[v].get("name", v)],
                "sources": [d.get("source")],
            })

    for n, d in g.nodes(data=True):
        measurements = [m for m in (d.get("measurements") or []) if m.get("value") is not None]
        distinct = {(str(m.get("value")), m.get("unit")) for m in measurements}
        sources = {m.get("source") for m in measurements}
        if len(distinct) > 1 and len(sources) > 1:
            result.append({
                "about": d.get("name", n),
                "values": measurements,
                "sources": sorted(sources),
            })

    return result


def find_gaps(graph, limit=20):
    g = graph.g
    materials = {n: d for n, d in g.nodes(data=True) if d.get("type") == "Material"}
    processes = {n: d for n, d in g.nodes(data=True) if d.get("type") == "Process"}

    observed = {(m, p) for m, md in materials.items() for p, pd in processes.items()
                if _sources(md) & _sources(pd)}
    mat_procs = {m: {p for (mm, p) in observed if mm == m} for m in materials}
    proc_mats = {p: {m for (m, pp) in observed if pp == p} for p in processes}

    gaps = []
    for m, md in materials.items():
        for p, pd in processes.items():
            if (m, p) in observed or not mat_procs[m] or not proc_mats[p]:
                continue
            gaps.append({
                "material": md.get("name", m),
                "process": pd.get("name", p),
                "reason": f"{pd.get('name', p)} изучали с другими материалами "
                          f"({len(proc_mats[p])}), а с «{md.get('name', m)}» — нет",
                "score": len(mat_procs[m]) * len(proc_mats[p]),
            })

    gaps.sort(key=lambda x: -x["score"])
    return gaps[:limit]
