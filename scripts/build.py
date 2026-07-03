import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import extract
from core.graph_store import NetworkxGraphStore
from core.llm import get_llm


def load_documents(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/processed/documents.jsonl")
    ap.add_argument("--output", default="data/processed")
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()

    llm = get_llm()
    graph = NetworkxGraphStore()

    for i, doc in enumerate(load_documents(args.input)):
        if args.limit and i >= args.limit:
            break
        data = extract.extract(doc["text"], llm)
        print(f"[{i}] {doc['doc_id']}: {len(data['entities'])} entities, {len(data['relations'])} relations")

    os.makedirs(args.output, exist_ok=True)
    graph.save(os.path.join(args.output, "graph.pkl"))
    print("graph:", graph.stats())


if __name__ == "__main__":
    main()
