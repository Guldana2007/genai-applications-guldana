"""
generate_vocab_graph.py

Small wrapper script that triggers the main logic from stats.py.

This file exists so that the GitHub Actions workflow can call a single
entry point, but it can also be used locally:

    python generate_vocab_graph.py
"""

from stats import main


if __name__ == "__main__":
    # Delegate all work to the main() function in stats.py
    main()
