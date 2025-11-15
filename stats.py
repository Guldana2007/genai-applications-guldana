"""
stats.py

This script analyzes the research text and vocabulary list to automatically:

1. Extract vocabulary terms from `vocabulary.md`
2. Count how many times each term appears in `research.md`
3. Save the results into `usage_stats.json`
4. Generate a graph visualization (`vocab_graph.png`) that shows
   relationships between the central theme ("Generative AI Applications")
   and all vocabulary terms that appear at least once.

Visual style (updated, neon radial style):

- Dark, almost black background, cyan / magenta neon palette
- Central "AI" node in the middle, large and bright
- All terms placed on a circle around the center (radial layout)
- Top-3 most frequent terms: bigger, warm neon color
- Soft glow effect around nodes (drawn as transparent halos)
- Edge width encodes frequency, edges use bright cyan
- Frequency number is shown next to every term node

This script is intended to be executed both locally and via GitHub Actions.
It was designed with the help of an AI assistant (GenAI Repository Automator).
"""

import json
import re
from pathlib import Path
from typing import List, Dict

import networkx as nx
import matplotlib

# Non-interactive backend for CI / GitHub Actions
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Paths to all relevant project files
RESEARCH_FILE = Path("research.md")
VOCAB_FILE = Path("vocabulary.md")
OUTPUT_JSON = Path("usage_stats.json")
OUTPUT_PNG = Path("vocab_graph.png")


def load_text(path: Path) -> str:
    """
    Read the content of a text file and return it as a string.
    """
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
            # Remove everything before the first dot ("1. Term" -> "Term")
            term = line.split(".", 1)[-1].strip()
            if term:
                terms.append(term.lower())
    return terms


def count_frequencies(text: str, terms: List[str]) -> Dict[str, int]:
    """
    Count how many times each vocabulary term appears in the research text.

    Matching is case-insensitive and uses word boundaries where possible.
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
    """
    Return the top_k terms by frequency (descending).
    If there are ties, the ordering is resolved alphabetically.
    """
    non_zero_terms = [(t, c) for t, c in freq.items() if c > 0]
    if not non_zero_terms:
        return []

    non_zero_terms.sort(key=lambda x: (-x[1], x[0]))
    return [t for t, _ in non_zero_terms[:top_k]]


def build_graph(freq: Dict[str, int]) -> None:
    """
    Build and save a relationship graph (neon radial style).

    Nodes:
        - Center node: "AI" / "Generative AI Applications"
        - All vocabulary terms with frequency > 0

    Layout:
        - Center node at (0, 0)
        - All terms arranged on a circle around the center

    Styling:
        - Dark background
        - Cyan / magenta neon colours
        - Soft "glow" around nodes (drawn as transparent halos)
        - Top-3 terms highlighted
        - Edge width encodes frequency
    """
    used_terms = {term: count for term, count in freq.items() if count > 0}

    # If no terms were used in the research, generate a minimal placeholder graph
    if not used_terms:
        plt.figure(figsize=(10, 7))
        ax = plt.gca()
        ax.set_facecolor("#050816")
        plt.text(
            0.5,
            0.5,
            "No vocabulary terms found in research.md",
            ha="center",
            va="center",
            fontsize=13,
            color="#f5f5f5",
        )
        plt.axis("off")
        plt.title("Vocabulary Relationship Graph", color="#ffffff", fontsize=16, pad=20)
        plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
        plt.close()
        return

    top_terms = set(_get_top_terms(freq, top_k=3))

    G = nx.Graph()
    center_label = "Generative AI Applications"
    center_short = "AI"

    # Add center node
    G.add_node(center_label, size=2500, role="center", label=center_short)

    # Add terms
    for term, count in used_terms.items():
        base_size = 600
        size = base_size + count * 180
        role = "top" if term in top_terms else "normal"
        G.add_node(term, size=size, role=role, freq=count, label=term)
        G.add_edge(center_label, term, weight=count)

    # --- Layout: radial circle around the center ---
    num_terms = len(used_terms)
    radius = 3.0

    pos = {center_label: (0.0, 0.0)}
    # Place terms evenly on the circle
    for i, term in enumerate(used_terms.keys()):
        angle = 2.0 * 3.14159265 * i / max(1, num_terms)
        x = radius * float(matplotlib.np.cos(angle))
        y = radius * float(matplotlib.np.sin(angle))
        pos[term] = (x, y)

    # --- Drawing ---
    plt.figure(figsize=(14, 9))
    ax = plt.gca()
    ax.set_facecolor("#050816")
    plt.axis("off")

    # Collect drawing parameters
    node_sizes = []
    node_colors = []
    halo_sizes = []
    halo_colors = []

    for node in G.nodes:
        data = G.nodes[node]
        size = data.get("size", 600)
        role = data.get("role", "normal")

        node_sizes.append(size)

        if role == "center":
            node_colors.append("#ffd447")  # warm yellow
            halo_colors.append("#ffd447")
            halo_sizes.append(size * 1.8)
        elif role == "top":
            node_colors.append("#ff6bb5")  # magenta/pink
            halo_colors.append("#ff6bb5")
            halo_sizes.append(size * 1.6)
        else:
            node_colors.append("#3fd0ff")  # cyan
            halo_colors.append("#3fd0ff")
            halo_sizes.append(size * 1.4)

    # Map halos to positions in same order as nodes()
    node_list = list(G.nodes)

    # Draw "glow" halos first (big transparent circles)
    for idx, node in enumerate(node_list):
        x, y = pos[node]
        plt.scatter(
            [x],
            [y],
            s=halo_sizes[idx],
            color=halo_colors[idx],
            alpha=0.16,
            linewidths=0,
        )

    # Edge widths based on frequency
    edge_widths = []
    for u, v, data in G.edges(data=True):
        w = data.get("weight", 1)
        edge_widths.append(1.0 + 0.8 * w)

    # Draw edges
    nx.draw_networkx_edges(
        G,
        pos,
        width=edge_widths,
        alpha=0.7,
        edge_color="#4ee9ff",
        style="solid",
    )

    # Draw nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors="#ffffff",
        linewidths=1.2,
        alpha=0.98,
    )

    # Labels: use "AI" for center, full term for others
    labels = {}
    for node in G.nodes:
        data = G.nodes[node]
        labels[node] = data.get("label", node)

    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels,
        font_size=9,
        font_color="#ffffff",
    )

    # Frequency labels near term nodes (not for center)
    for node in G.nodes:
        if node == center_label:
            continue
        data = G.nodes[node]
        freq_value = data.get("freq", 0)
        x, y = pos[node]
        plt.text(
            x,
            y - 0.35,
            f"{freq_value}",
            fontsize=8,
            ha="center",
            va="center",
            color="#fff6a1",
        )

    # Title and legend text
    plt.title(
        "Generative AI Vocabulary — Neon Radial Graph\n"
        "Node size & edge width reflect frequency. Top-3 terms highlighted.",
        fontsize=15,
        color="#ffffff",
        pad=22,
    )

    plt.text(
        0.01,
        0.02,
        "Center: Generative AI Applications (AI)\n"
        "Pink nodes: Top-3 most frequent terms\n"
        "Cyan nodes: Other used terms\n"
        "Number under each node = frequency in research.md",
        transform=plt.gcf().transFigure,
        fontsize=8,
        color="#d0d0d0",
        va="bottom",
    )

    plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
    plt.close()


def main() -> None:
    """
    Main execution function:
    - Load input files
    - Extract vocabulary terms
    - Count frequencies
    - Generate JSON statistics
    - Build and save the visual graph
    """
    research_text = load_text(RESEARCH_FILE)
    vocab_text = load_text(VOCAB_FILE)

    terms = extract_terms(vocab_text)
    freq = count_frequencies(research_text, terms)

    # Save frequency statistics as JSON
    OUTPUT_JSON.write_text(
        json.dumps(freq, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    # Build the vocabulary graph
    build_graph(freq)


if __name__ == "__main__":
    main()
