"""
stats.py
--------

This script analyzes the research text and vocabulary list to automatically:

1. Extract vocabulary terms from `vocabulary.md`
2. Count how many times each term appears in `research.md`
3. Save the results into `usage_stats.json`
4. Generate a graph visualization (`vocab_graph.png`) that shows
   relationships between the central theme ("Generative AI Applications")
   and all vocabulary terms that appear at least once.

The graph uses a circular layout, highlights the top-3 most frequent
terms in a different color, and displays the frequency next to each node.

This script is executed both locally and automatically using GitHub Actions.
It forms the core of the project's analytical pipeline.
"""

import json
import math
import re
from pathlib import Path

import networkx as nx
import matplotlib

# Use non-interactive backend for GitHub Actions / headless environments
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Paths to all relevant project files
RESEARCH_FILE = Path("research.md")
VOCAB_FILE = Path("vocabulary.md")
OUTPUT_JSON = Path("usage_stats.json")
OUTPUT_PNG = Path("vocab_graph.png")


def load_text(path: Path) -> str:
    """
    Read the content of a text file and return it as a string.

    Parameters:
        path (Path): Path to the file that should be loaded.

    Returns:
        str: Content of the file.
    """
    return path.read_text(encoding="utf-8")


def extract_terms(vocab_md: str) -> list:
    """
    Extract vocabulary terms from the markdown file.
    It finds lines starting with '##', removes numbering (e.g., '1.'),
    and converts terms to lowercase for consistent matching.

    Parameters:
        vocab_md (str): Content of vocabulary.md as a string.

    Returns:
        list: A list of extracted vocabulary terms in lowercase.
    """
    terms = []
    for line in vocab_md.splitlines():
        line = line.strip()
        # Vocabulary terms follow the format '## 1. Term'
        if line.startswith("##"):
            # Remove numbering before the first dot
            term = line.split(".", 1)[-1].strip()
            terms.append(term.lower())
    return terms


def count_frequencies(text: str, terms: list[str]) -> dict:
    """
    Count how many times each vocabulary term appears in the research text.

    Matching is case-insensitive, and we use a word-boundary regex
    to ensure exact term matches (no partial matches inside other words).

    Parameters:
        text (str): The research document.
        terms (list[str]): Vocabulary terms to search for.

    Returns:
        dict: A dictionary mapping each term to its frequency.
    """
    freq: dict[str, int] = {}
    text = text.lower()  # Normalize text

    for term in terms:
        # Use regex to count exact whole-word occurrences
        freq[term] = len(re.findall(r"\b" + re.escape(term) + r"\b", text))

    return freq


def build_graph(freq: dict):
    """
    Build and save a styled relationship graph using NetworkX and matplotlib.

    Nodes:
        - Central node: "Generative AI Applications"
        - All vocabulary terms with frequency > 0
          (their node size increases with frequency)

    Layout:
        - Circular layout: all terms are positioned on a circle
          around the central node.

    Styling:
        - Node size and edge width reflect term frequency
        - Top-3 most frequent terms highlighted in a different color
        - Labels show both the term and its frequency, e.g. "term (3)"

    Output:
        vocab_graph.png (saved in the project root).
    """
    G = nx.Graph()
    center = "Generative AI Applications"
    G.add_node(center, size=1400, kind="center", count=0)

    # Keep only terms that actually appear at least once
    nonzero_terms: list[tuple[str, int]] = [
        (term, c) for term, c in freq.items() if c > 0
    ]
    if not nonzero_terms:
        # Nothing to draw if no vocabulary terms appear in the research text
        return

    # Sort by frequency (descending) to find top-3 terms
    nonzero_terms.sort(key=lambda x: x[1], reverse=True)
    top_terms = {t for t, _ in nonzero_terms[:3]}  # names of top-3 terms
    max_count = max(c for _, c in nonzero_terms)

    # Add term nodes and edges connecting them to the central node
    for term, count in nonzero_terms:
        node_size = 450 + count * 220  # grow node size with frequency
        G.add_node(term, size=node_size, kind="term", count=count)
        G.add_edge(center, term, weight=1.0 + 0.6 * count)

    plt.figure(figsize=(14, 9))
    plt.axis("off")

    # ---- Circular layout: center at (0, 0), terms arranged on a circle ----
    pos: dict[str, tuple[float, float]] = {}
    pos[center] = (0.0, 0.0)

    n = len(nonzero_terms)
    radius = 1.8
    for i, (term, _) in enumerate(nonzero_terms):
        angle = 2 * math.pi * i / n
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        pos[term] = (x, y)

    # ---- Draw edges between center and term nodes ----
    edge_weights = [G[u][v].get("weight", 1.0) for u, v in G.edges()]
    nx.draw_networkx_edges(
        G,
        pos,
        width=edge_weights,
        alpha=0.4,
        edge_color="#555555",
    )

    # ---- Draw central node (highlighted) ----
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[center],
        node_size=G.nodes[center]["size"],
        node_color="#0052CC",  # deep blue
        edgecolors="white",
        linewidths=2.4,
    )

    # ---- Draw term nodes, using separate color for top-3 terms ----
    term_nodes = [t for t, _ in nonzero_terms]
    term_sizes = [G.nodes[n]["size"] for n in term_nodes]

    cmap = plt.cm.Blues
    node_colors = []
    for term, count in nonzero_terms:
        if term in top_terms:
            # Top-3 terms: highlight with teal color
            node_colors.append("#00B8A9")
        else:
            # Other terms: blue gradient depending on frequency
            norm = 0.3 + 0.7 * (count / max_count)
            node_colors.append(cmap(norm))

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=term_nodes,
        node_size=term_sizes,
        node_color=node_colors,
        edgecolors="white",
        linewidths=1.8,
    )

    # ---- Labels: term + frequency ----
    labels: dict[str, str] = {}
    for term in term_nodes:
        c = G.nodes[term]["count"]
        # Example label: "semantic search\n(1)" → term + frequency in brackets
        labels[term] = f"{term}\n({c})"
    labels[center] = center

    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels,
        font_size=9,
        font_family="sans-serif",
        font_color="#222222",
    )

    # ---- Title ----
    plt.title(
        "Generative AI Vocabulary Graph (Frequency & Top Terms)",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300)
    plt.close()


def main():
    """
    Main execution function:
    - Load input files
    - Extract vocabulary terms
    - Count frequencies
    - Generate JSON statistics
    - Build and save the graph
    """
    research = load_text(RESEARCH_FILE)
    vocab = load_text(VOCAB_FILE)

    terms = extract_terms(vocab)
    freq = count_frequencies(research, terms)

    # Save frequency statistics as JSON
    OUTPUT_JSON.write_text(
        json.dumps(freq, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    # Build the vocabulary graph
    build_graph(freq)


if __name__ == "__main__":
    # Run the script only when executed directly
    main()
