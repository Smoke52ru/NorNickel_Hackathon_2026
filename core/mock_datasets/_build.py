"""Helper to validate mock graph node/edge consistency."""
from __future__ import annotations


def validate_graph(graph: dict, name: str) -> None:
    node_ids = {n["id"] for n in graph["nodes"]}
    types = {n["type"] for n in graph["nodes"]}
    required = {
        "Material", "Process", "Equipment", "Property",
        "Experiment", "Publication", "Expert", "Facility",
    }
    missing = required - types
    if missing:
        raise ValueError(f"{name}: missing entity types {missing}")
    for e in graph["edges"]:
        if e["from"] not in node_ids:
            raise ValueError(f"{name}: unknown from {e['from']}")
        if e["to"] not in node_ids:
            raise ValueError(f"{name}: unknown to {e['to']}")
