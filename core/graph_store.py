import pickle
from abc import ABC, abstractmethod

import networkx as nx


class GraphStore(ABC):
    @abstractmethod
    def add_entity(self, eid, etype, name, **attrs): ...
    @abstractmethod
    def add_relation(self, src, dst, rel, **attrs): ...
    @abstractmethod
    def neighbors(self, eid): ...
    @abstractmethod
    def find_path(self, src, dst): ...
    @abstractmethod
    def to_dict(self, nodes=None): ...


class NetworkxGraphStore(GraphStore):
    def __init__(self):
        self.g = nx.MultiDiGraph()

    def add_entity(self, eid, etype, name, **attrs):
        self.g.add_node(eid, type=etype, name=name, **attrs)

    def add_relation(self, src, dst, rel, **attrs):
        self.g.add_edge(src, dst, key=rel, rel=rel, **attrs)

    def neighbors(self, eid):
        return list(set(self.g.successors(eid)) | set(self.g.predecessors(eid)))

    def find_path(self, src, dst):
        try:
            return nx.shortest_path(self.g, src, dst)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def to_dict(self, nodes=None):
        g = self.g if nodes is None else self.g.subgraph(nodes)
        out_nodes = [{"id": n, "label": d.get("name", n), "type": d.get("type", "")}
                     for n, d in g.nodes(data=True)]
        out_edges = [{"from": u, "to": v, "label": d.get("rel", key),
                      "flag": "contradiction" if d.get("rel") == "contradicts" else "normal"}
                     for u, v, key, d in g.edges(keys=True, data=True)]
        return {"nodes": out_nodes, "edges": out_edges}

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump(self.g, f)

    def load(self, path):
        with open(path, "rb") as f:
            self.g = pickle.load(f)
        return self

    def stats(self):
        return {"nodes": self.g.number_of_nodes(), "edges": self.g.number_of_edges()}
