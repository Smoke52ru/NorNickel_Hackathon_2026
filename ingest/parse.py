# documents.jsonl: {doc_id, source_path, title, year, lang, text, chunks}
import argparse


def parse_pdf(path):
    raise NotImplementedError


def parse_docx(path):
    raise NotImplementedError


def make_record(path, root):
    raise NotImplementedError


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="data/raw")
    ap.add_argument("--output", default="data/processed/documents.jsonl")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    raise NotImplementedError


if __name__ == "__main__":
    main()
