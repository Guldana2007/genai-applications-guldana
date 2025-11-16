"""
stats.py

This script analyzes the research text and the vocabulary list in order to:

1. Extract vocabulary terms from `vocabulary.md`
2. Count how many times each term appears in `research.md`
3. Save the statistics into `usage_stats.json`
4. Build a vocabulary graph in `vocab_graph.png`

The graph uses:
- Dark background with a subtle grid
- Rectangular "cards" instead of circles
- Glow around nodes
- Soft, segmented edges
- Small light particles in the background

The goal is to make the visualization both informative and visually attractive.
"""

import json
import re
from pathlib import Path
from typing import List, Dict

import matplotlib
# Use a non-interactive backend so the script works in CI / GitHub Actions
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# Paths to all relevant project files
RESEARCH_FILE = Path("research.md")
VOCAB_FILE = Path("vocabulary.md")
OUTPUT_JSON = Path("usage_stats.json")
OUTPUT_PNG = Path("vocab_graph.png")


def load_text(path: Path) -> str:
    """
    Read the content of a text file and return it as a single string.
    """
    return path.read_text(encoding="utf-8")


def extract_terms(vocab_md: str) -> List[str]:
    """
    Extract vocabulary terms from the markdown document.

    Each term is expected to be on a line starting with "##",
    for example:

        ## 1. Generative AI

    Only the part after the first dot is used as a term,
    and everything is converted to lowercase for consistent matching.
    """
    terms: List[str] = []
    for line in vocab_md.splitlines():
        stripped = line.strip()
        if stripped.startswith("##"):
            # Take the part after the first dot, e.g. "1. Generative AI" -> "Generative AI"
            term = stripped.split(".", 1)[-1].strip().lower()
            if term:
                terms.append(term)
    return terms


def count_frequencies(text: str, terms: List[str]) -> Dict[str, int]:
    """
    Count how many times each vocabulary term appears in the research text.

    Matching is case-insensitive. Word boundaries are used to reduce the
    chance of partial matches (for example, "token" inside "tokenization").
    """
    frequencies: Dict[str, int] = {}
    text_lower = text.lower()

    for term in terms:
        if not term:
            frequencies[term] = 0
            continue

        pattern = r"\b" + re.escape(term) + r"\b"
        matches = re.findall(pattern, text_lower)
        frequencies[term] = len(matches)

    return frequencies


def _get_top_terms(freq: Dict[str, int], top_k: int = 3) -> List[str]:
    """
    Return a list with the names of the top_k most frequent terms.

    Only terms with a frequency > 0 are considered.
    """
    non_zero = [(term, count) for term, count in freq.items() if count > 0]
    if not non_zero:
        return []

    # Sort by frequency (descending), then alphabetically for stability
    non_zero.sort(key=lambda x: (-x[1], x[0]))
    return [term for term, _ in non_zero[:top_k]]


# ============================================================================
#   Futuristic vocabulary graph generator (rectangles, glow, particles)
# ============================================================================


def build_graph(freq: Dict[str, int]) -> None:
    """
    Build and save a vocabulary graph.

    Nodes:
        - Center node: "Generative AI Applications"
        - One node per vocabulary term that appears at least once in research.md

    Visual style:
        - Dark grid background
        - Rectangular nodes (cards) instead of circles
        - Glow around nodes
        - Segmented edges to imitate a soft gradient
        - Light particles scattered in the background
        - Top-3 most frequent terms are highlighted in a separate color

    Output is saved as `vocab_graph.png`.
    """
    # Keep only terms that actually appear in the research text
    used_terms = {term: count for term, count in freq.items() if count > 0}

    # If nothing is used, create a simple message image and stop
    if not used_terms:
        plt.figure(figsize=(10, 6))
        ax = plt.gca()
        ax.set_facecolor("#030510")
        plt.text(
            0.5,
            0.5,
            "No vocabulary terms found in research.md",
            ha="center",
            va="center",
            fontsize=12,
            color="white",
        )
        plt.axis("off")
        plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
        plt.close()
        return

    center_label = "Generative AI Applications"
    top_terms = set(_get_top_terms(freq, top_k=3))

    # --- Create the graph structure ---
    G = nx.Graph()
    G.add_node(center_label, role="center", freq=0, size=3200)

    for term, count in used_terms.items():
        G.add_node(
            term,
            role="top" if term in top_terms else "normal",
            freq=count,
            size=1800 + count * 400,
        )
        G.add_edge(center_label, term, weight=count)

    # --- Prepare the figure and background ---
    fig = plt.figure(figsize=(20, 16))
    ax = plt.gca()
    plt.axis("off")

    # Dark background color
    ax.set_facecolor("#030510")

    # Subtle grid lines for a "tech" feeling
    for x in np.linspace(-1, 1, 30):
        ax.axvline(x, color="#0a1028", linewidth=0.4, alpha=0.35)
    for y in np.linspace(-1, 1, 30):
        ax.axhline(y, color="#0a1028", linewidth=0.4, alpha=0.35)

    # Spring layout gives a natural "network" shape
    pos = nx.spring_layout(G, seed=42, k=1.2)

    # --- Background light particles (small glowing dots) ---
    particles_x = np.random.uniform(-1, 1, 140)
    particles_y = np.random.uniform(-1, 1, 140)
    plt.scatter(
        particles_x,
        particles_y,
        s=12,
        color="#3fd0ff",
        alpha=0.18,
    )

    # --- Segmented edges (imitating a gradient / neon line) ---
    for (u, v, edge_data) in G.edges(data=True):
        x1, y1 = pos[u]
        x2, y2 = pos[v]

        # Interpolate points between the two nodes
        steps = 40
        xs = np.linspace(x1, x2, steps)
        ys = np.linspace(y1, y2, steps)

        for i in range(steps - 1):
            # Alpha grows slightly along the edge
            alpha = (i / steps) ** 1.5
            plt.plot(
                xs[i : i + 2],
                ys[i : i + 2],
                color=(0.2, 0.8, 1.0, 0.15 + alpha * 0.5),
                linewidth=1.6,
            )

    # --- Draw rectangular nodes with glow ---
    for node, node_data in G.nodes(data=True):
        x, y = pos[node]
        size = node_data.get("size", 1800)
        freq_value = node_data.get("freq", 0)
        role = node_data.get("role", "normal")

        # Convert "size" to rectangle width/height in layout coordinates.
        # Denominators are tuned so labels fit comfortably inside.
        rect_width = size / 8000.0   # wider rectangles
        rect_height = size / 22000.0  # slightly taller rectangles

        # Color scheme depends on node role.
        # All faces are relatively light so black text is readable.
        if role == "center":
            face_color = "#ffe89c"    # light yellow
            glow_color = "#fff7c7"
        elif role == "top":
            face_color = "#ffd1d9"    # light pink
            glow_color = "#ffe4ea"
        else:
            face_color = "#d6ecff"    # light blue
            glow_color = "#e6f4ff"

        # Outer glow rectangle (first layer)
        outer_glow = plt.Rectangle(
            (x - rect_width / 2 - 0.012, y - rect_height / 2 - 0.012),
            rect_width + 0.024,
            rect_height + 0.024,
            facecolor=glow_color,
            edgecolor=None,
            alpha=0.18,
        )
        ax.add_patch(outer_glow)

        # Inner glow rectangle (second layer)
        inner_glow = plt.Rectangle(
            (x - rect_width / 2 - 0.006, y - rect_height / 2 - 0.006),
            rect_width + 0.012,
            rect_height + 0.012,
            facecolor=glow_color,
            edgecolor=None,
            alpha=0.35,
        )
        ax.add_patch(inner_glow)

        # Main rectangle for the node itself
        rect = plt.Rectangle(
            (x - rect_width / 2, y - rect_height / 2),
            rect_width,
            rect_height,
            facecolor=face_color,
            edgecolor="white",
            linewidth=1.8,
            alpha=0.96,
        )
        ax.add_patch(rect)

        # Node label in the center of the rectangle
        # All labels are black so they stand out on a light face color.
        plt.text(
            x,
            y,
            node,
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="black",
        )

        # Frequency value displayed slightly below the node (not for the center)
        if node != center_label:
            plt.text(
                x,
                y - rect_height * 0.9,
                f"{freq_value}",
                fontsize=8,
                color="#4a6b86",
                ha="center",
                va="center",
            )

    # Title explaining what the viewer is looking at
    plt.title(
        "Generative AI Vocabulary — Futuristic Graph",
        fontsize=20,
        color="white",
        pad=20,
    )

    plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
    plt.close()


def main() -> None:
    """
    Main entry point:
    - read markdown files
    - compute frequencies
    - write JSON statistics
    - build the visualization graph
    """
    research_text = load_text(RESEARCH_FILE)
    vocab_text = load_text(VOCAB_FILE)

    terms = extract_terms(vocab_text)
    freq = count_frequencies(research_text, terms)

    # Save frequency statistics as pretty-printed JSON
    OUTPUT_JSON.write_text(
        json.dumps(freq, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )

    # Build the graph
    build_graph(freq)


if __name__ == "__main__":
    main()
