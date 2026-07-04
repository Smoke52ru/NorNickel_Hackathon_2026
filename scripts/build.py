import argparse
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import analysis, extract
from core.graph_build import add_extraction
from core.graph_store import NetworkxGraphStore
from core.llm import get_llm
from core.retrieval import load_chunks


def load_documents(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def build_vectors(docs_path, output):
    """Посчитать эмбеддинги всех кусков для векторного поиска. Не критично: если
    эмбеддер недоступен, поиск деградирует до BM25, поэтому падать не даём."""
    try:
        import faiss
        import numpy as np
        from core.embeddings import get_embedder
        chunks = load_chunks(docs_path)
        vecs = np.asarray(get_embedder()([c["text"] for c in chunks]), dtype="float32")
        faiss.normalize_L2(vecs)
        np.save(os.path.join(output, "vectors.npy"), vecs)
        print("vectors:", vecs.shape)
    except Exception as e:
        print("vectors skipped:", e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/processed/documents.jsonl")
    ap.add_argument("--output", default="data/processed")
    ap.add_argument("--limit", type=int, default=50, help="макс. документов (0 = все)")
    ap.add_argument("--no-vectors", action="store_true", help="пропустить эмбеддинги (только BM25)")
    args = ap.parse_args()

    llm = get_llm()
    graph = NetworkxGraphStore()

    for i, doc in enumerate(load_documents(args.input)):
        if args.limit and i >= args.limit:
            break
        # извлекаем ПО КУСКАМ: chunks покрывают весь документ, обрезанный text потерял бы всё, кроме начала
        n_ent = n_rel = 0
        for chunk in doc.get("chunks") or [doc["text"]]:
            data = extract.extract(chunk, llm)
            add_extraction(graph, data, doc["doc_id"], doc)
            n_ent += len(data["entities"])
            n_rel += len(data["relations"])
        print(f"[{i}] {doc['doc_id']}: +{n_ent} entities, +{n_rel} relations")

    os.makedirs(args.output, exist_ok=True)
    graph.save(os.path.join(args.output, "graph.pkl"))

    # документы кладём рядом с графом — API читает всё из одного места (DATA_PROCESSED)
    dst = os.path.join(args.output, "documents.jsonl")
    if os.path.abspath(args.input) != os.path.abspath(dst):
        shutil.copy(args.input, dst)

    if not args.no_vectors:
        build_vectors(dst, args.output)

    print("graph:", graph.stats())
    print("contradictions:", len(analysis.find_contradictions(graph)))
    print("gaps:", len(analysis.find_gaps(graph)))


if __name__ == "__main__":
    main()
