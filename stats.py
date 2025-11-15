"""
stats.py

This script analyzes the research text and vocabulary list to automatically:

1. Extract vocabulary terms from `vocabulary.md`
2. Count how many times each term appears in `research.md`
3. Save the results into `usage_stats.json`
4. Generate a graph visualization (`vocab_graph.png`) that shows
   relationships between the central theme ("Generative AI Applications")
   and all vocabulary terms that appear at least once.

The visual style of the graph is enhanced:
- Top-3 most frequent terms are highlighted with a special color and larger size
- All nodes use a force-directed (spring) layout
- Frequency values are displayed near each node
- Dark background and bright colors provide a modern “data science” look

This script is intended to be executed both locally and via GitHub Actions.
It was designed with the help of an AI assistant (GenAI Repository Automator).
"""

import json
import re
from pathlib import Path
from typing import List, Dict

import networkx as nx
import matplotlib

# Use non-interactive backend for CI / GitHub Actions
matplotlib.use("Agg")

import matplotlib.pyplot as plt


# Paths to all relevant project files
RESEARCH_FILE = Path("research.md")
VOCAB_FILE = Path("vocabulary.md")
OUTPUT_JSON = Path("usage_stats.json")
OUTPUT_PNG = Path("vocab_graph.png")


def load_text(path: Path) -> str:
    """Read the content of a text file and return it as a string."""
    return path.read_text(encoding="utf-8")


def extract_terms(vocab_md: str) -> List[str]:
    """
    Extract vocabulary terms from the markdown file.

    It finds lines starting with '##', removes numbering (e.g., '1.'),
    and converts terms to lowercase for consistent matching.

    Expected format for each term line: '## 1. Term'.
    """
    terms: List[str] = []
    for line in vocab_md.splitlines():
        line = line.strip()
        if line.startswith("##"):
            term = line.split(".", 1)[-1].strip()
            if term:
                terms.append(term.lower())
    return terms


def count_frequencies(text: str, terms: List[str]) -> Dict[str, int]:
    """
    Count how many times each vocabulary term appears in the research text.

    Matching is case-insensitive, and we use a regex with word boundaries
    to reduce the chance of partial matches.
    """
    freq: Dict[str, int] = {}
    text_lower = text.lower()

    for term in terms:
        if not term:
            freq[term] = 0
            continue

        pattern = r"\b" + re.escape(term) + r"\b"
        matches = re.findall(pattern, text_lower)
        freq[term] = len(matches)

    return freq


def _get_top_terms(freq: Dict[str, int], top_k: int = 3) -> List[str]:
    """Return the top_k terms by frequency (descending)."""
    non_zero_terms = [(t, c) for t, c in freq.items() if c > 0]
    if not non_zero_terms:
        return []

    non_zero_terms.sort(key=lambda x: (-x[1], x[0]))
    return [t for t, _ in non_zero_terms[:top_k]]


def build_graph(freq: Dict[str, int]) -> None:
    """
    Build and save a relationship graph using NetworkX and Matplotlib.

    Nodes:
        - A central node: "Generative AI Applications"
        - All vocabulary terms with a frequency > 0

    Styling:
        - Dark background
        - Top-3 most frequent terms are highlighted
        - Node sizes scale with term frequency
        - Frequency labels are drawn next to each node

    Output:
        vocab_graph.png
    """
    used_terms = {term: count for term, count in freq.items() if count > 0}

    if not used_terms:
        plt.figure(figsize=(8, 6))
        plt.text(
            0.5,
            0.5,
            "No vocabulary terms found in research.md",
            ha="center",
            va="center",
            fontsize=12,
        )
        plt.axis("off")
        plt.title("Vocabulary Relationship Graph")
        plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
        plt.close()
        return

    top_terms = set(_get_top_terms(freq, top_k=3))

    G = nx.Graph()
    center_label = "Generative AI Applications"
    G.add_node(center_label, size=1600, role="center")

    for term, count in used_terms.items():
        base_size = 400
        size = base_size + count * 150
        role = "top" if term in top_terms else "normal"
        G.add_node(term, size=size, role=role, freq=count)
        G.add_edge(center_label, term, weight=count)

    plt.figure(figsize=(14, 10))
    ax = plt.gca()
    ax.set_facecolor("#0b1020")
    plt.axis("off")

    # Spring layout (force-directed) for modern look
    pos = nx.spring_layout(G, seed=42, k=0.8)

    node_sizes = []
    node_colors = []
    for node in G.nodes:
        data = G.nodes[node]
        size = data.get("size", 400)
        role = data.get("role", "normal")

        node_sizes.append(size)

        if role == "center":
            node_colors.append("#ffcc00")  # center
        elif role == "top":
            node_colors.append("#ff6b6b")  # top terms
        else:
            node_colors.append("#4db8ff")  # others

    edge_widths = []
    for _, _, data in G.edges(data=True):
        w = data.get("weight", 1)
        edge_widths.append(0.8 + 0.6 * w)

    nx.draw_networkx_edges(
        G,
        pos,
        width=edge_widths,
        alpha=0.6,
        edge_color="#cccccc",
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        linewidths=1.0,
        edgecolors="#ffffff",
        alpha=0.95,
    )

    labels = {n: n for n in G.nodes}
    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels,
        font_size=9,
        font_color="#ffffff",
    )

    for node in G.nodes:
        if node == center_label:
            continue
        data = G.nodes[node]
        freq_value = data.get("freq", 0)
        x, y = pos[node]
        plt.text(
            x,
            y - 0.06,
            f"{freq_value}",
            fontsize=8,
            ha="center",
            va="center",
            color="#fffb99",
        )

    plt.title(
        "Vocabulary Relationship Graph\n"
        "Node size and color reflect term frequency. Top-3 terms highlighted.",
        fontsize=14,
        color="#ffffff",
        pad=20,
    )

    plt.text(
        0.01,
        0.02,
        "Center: Generative AI Applications\n"
        "Red nodes: Top-3 most frequent terms\n"
        "Blue nodes: Other used terms\n"
        "Number under each node = frequency in research.md",
        transform=plt.gcf().transFigure,
        fontsize=8,
        color="#dddddd",
        va="bottom",
    )

    plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
    plt.close()


def main() -> None:
    """Main execution function."""
    research_text = load_text(RESEARCH_FILE)
    vocab_text = load_text(VOCAB_FILE)

    terms = extract_terms(vocab_text)
    freq = count_frequencies(research_text, terms)

    OUTPUT_JSON.write_text(
        json.dumps(freq, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    build_graph(freq)


if __name__ == "__main__":
    main()
