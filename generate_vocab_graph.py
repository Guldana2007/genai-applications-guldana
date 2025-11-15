import matplotlib.pyplot as plt
import numpy as np
import json
import math

# ---------------------------------------------------------
# LOAD VOCABULARY & STATS
# ---------------------------------------------------------
with open("vocabulary.md", "r", encoding="utf-8") as f:
    vocab_text = f.read()

with open("usage_stats.json", "r", encoding="utf-8") as f:
    stats = json.load(f)

# Extract vocabulary terms
vocab_terms = [line.strip("- ").strip() for line in vocab_text.split("\n") if line.startswith("- ")]

# Center node
center_label = "Generative AI Applications"

# Determine top frequency terms (highlighted)
sorted_terms = sorted(stats.items(), key=lambda x: x[1], reverse=True)
top_terms = set([t for t, c in sorted_terms[:3]])

# ---------------------------------------------------------
# VISUAL STYLE SETTINGS (NEON STYLE)
# ---------------------------------------------------------
bg_color = "#050915"
center_color = "#ffd700"
top_color = "#ff6b6b"
normal_color = "#63c7ff"

glow_strength = 25

plt.figure(figsize=(14, 10), facecolor=bg_color)
ax = plt.gca()
ax.set_facecolor(bg_color)
plt.axis("off")

# ---------------------------------------------------------
# POSITIONING NODES IN CIRCLE
# ---------------------------------------------------------
N = len(vocab_terms)
radius = 4.5

angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
positions = [(radius * np.cos(a), radius * np.sin(a)) for a in angles]

# ---------------------------------------------------------
# DRAW CENTER NODE
# ---------------------------------------------------------
plt.scatter(0, 0, s=1800, color=center_color, edgecolor="white", linewidth=2, zorder=5)
plt.text(
    0, 0, center_label,
    color="black",
    fontsize=14,
    ha="center",
    va="center",
    weight="bold"
)

# ---------------------------------------------------------
# DRAW VOCABULARY NODES
# ---------------------------------------------------------
for i, term in enumerate(vocab_terms):
    x, y = positions[i]
    count = stats.get(term.lower(), 0)

    # Color depending on frequency
    node_color = top_color if term.lower() in top_terms else normal_color
    size = 800 if term.lower() in top_terms else 650

    # Node glow effect (multiple circles)
    for glow in range(glow_strength):
        alpha = (glow_strength - glow) / (glow_strength * 80)
        plt.scatter(
            x, y,
            s=size + glow * 15,
            color=node_color,
            alpha=alpha,
            edgecolor=None,
            zorder=1
        )

    # Main node
    plt.scatter(x, y, s=size, color=node_color, edgecolor="white", linewidth=2, zorder=3)

    # Node label
    plt.text(
        x, y,
        f"{term}\n({count})",
        color="white",
        fontsize=10,
        ha="center",
        va="center",
        zorder=4
    )

    # Edge to center
    plt.plot(
        [0, x], [0, y],
        color="white",
        alpha=0.25,
        linewidth=1.5,
        zorder=2
    )

# ---------------------------------------------------------
# FOOTNOTE
# ---------------------------------------------------------
plt.text(
    -6, -5.5,
    "Center: Generative AI Applications\n"
    "Red nodes: Top-3 frequent terms\n"
    "Blue nodes: Other terms\n"
    "Value = frequency in research.md",
    fontsize=8,
    color="#b8c6d1",
    ha="left"
)

# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------
plt.savefig("vocab_graph.png", dpi=300, facecolor=bg_color)
plt.close()

print("Generated neon vocabulary graph: vocab_graph.png created.")
