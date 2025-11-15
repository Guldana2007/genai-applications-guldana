"""
generate_vocab_graph.py

Entry point for building usage statistics and the vocabulary graph.

This script is used by GitHub Actions (workflow .github/workflows/generate_graph.yml)
and can also be run locally.

It delegates all real work to stats.py:
- reads research.md and vocabulary.md
- counts frequencies
- saves usage_stats.json
- generates vocab_graph.png

The logic itself lives in stats.py (function main()), so that
we have a single source of truth.
"""

from stats import main


if __name__ == "__main__":
    # Call the main() function defined in stats.py
    main()
