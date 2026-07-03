def find_contradictions(graph):
    result = []
    for u, v, key, d in graph.g.edges(keys=True, data=True):
        if d.get("rel") == "contradicts":
            result.append({"about": graph.g.nodes[u].get("name", u), "sources": [u, v]})
    return result


def find_gaps(graph):
    return []
