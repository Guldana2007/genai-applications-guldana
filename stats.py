import json
import re
from pathlib import Path

import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESEARCH_FILE = Path("research.md")
VOCAB_FILE = Path("vocabulary.md")
OUTPUT_JSON = Path("usage_stats.json")
OUTPUT_PNG = Path("vocab_graph.png")


def load_text(path):
    return path.read_text(encoding="utf-8")


def extract_terms(vocab_md: str):
    terms = []
    for line in vocab_md.splitlines():
        line = line.strip()
        if line.startswith("##"):
            term = line.split(".", 1)[-1].strip()
            terms.append(term.lower())
    return terms


def count_frequencies(text: str, terms: list[str]):
    freq = {}
    text = text.lower()
    for term in terms:
        freq[term] = len(re.findall(r"\b" + re.escape(term) + r"\b", text))
    return freq


def build_graph(freq: dict):
    G = nx.Graph()
    center = "Generative AI Applications"
    G.add_node(center, size=500)

    for term, count in freq.items():
        if count > 0:
            G.add_node(term, size=200 + count * 100)
            G.add_edge(center, term)

    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42)
    sizes = [G.nodes[n]["size"] for n in G.nodes]

    nx.draw(G, pos, with_labels=True, node_size=sizes, font_size=8)
    plt.title("Vocabulary Relationship Graph")
    plt.savefig(OUTPUT_PNG, dpi=300)
    plt.close()


def main():
    research = load_text(RESEARCH_FILE)
    vocab = load_text(VOCAB_FILE)

    terms = extract_terms(vocab)
    freq = count_frequencies(research, terms)

    OUTPUT_JSON.write_text(json.dumps(freq, indent=4, ensure_ascii=False), encoding="utf-8")
    build_graph(freq)


if __name__ == "__main__":
    main()
