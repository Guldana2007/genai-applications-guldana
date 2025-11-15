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

This script is executed both locally and automatically using GitHub Actions.
It forms the core of the project's analytical pipeline.
"""

import json
import re
from pathlib import Path

import networkx as nx
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend for GitHub Actions
import matplotlib.pyplot as plt

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

    Matching is case-insensitive, and we use word-boundary regex
    to ensure exact term matches (no partial matches inside other words).

    Parameters:
        text (str): The research document.
        terms (list[str]): Vocabulary terms to search for.

    Returns:
        dict: A dictionary mapping each term to its frequency.
    """
    freq = {}
    text = text.lower()  # Normalize text

    for term in terms:
        # Use regex to count exact whole-word occurrences
        freq[term] = len(re.findall(r"\b" + re.escape(term) + r"\b", text))

    return freq


def build_graph(freq: dict):
    """
    Build and save a relationship graph using NetworkX.

    Nodes:
        - A central node: "Generative AI Applications"
        - All vocabulary terms with a frequency > 0
          (their node size increases with frequency)

    Edges:
        - Each term node is connected to the central node.

    Output:
        vocab_graph.png (saved in project root)
    """
    G = nx.Graph()
    center = "Generative AI Applications"
    G.add_node(center, size=500)  # Central node

    # Add all terms that appear at least once
    for term, count in freq.items():
        if count > 0:
            G.add_node(term, size=200 + count * 100)  # Scale node size
            G.add_edge(center, term)

    # Draw the graph
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, seed=42)  # Stable layout
    sizes = [G.nodes[n]["size"] for n in G.nodes]

    nx.draw(G, pos, with_labels=True, node_size=sizes, font_size=8)
    plt.title("Vocabulary Relationship Graph")

    # Save the output image file
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
        encoding="utf-8"
    )

    # Build the vocabulary graph
    build_graph(freq)


if __name__ == "__main__":
    # Run the script only when executed directly
    main()
