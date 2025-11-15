📘 Generative AI Applications — Research Project

Use Cases, Vocabulary Analytics, Automated Graph Generation, and Codemie AI Assistant Integration

This project presents a complete analytical workflow around Generative AI, including a curated vocabulary, usage frequency analysis, automated graph generation using GitHub Actions, and an integrated EPAM Codemie AI Assistant that analyzes and automates work with this repository.

🤖 Codemie AI Assistant Integration
GenAI Repository Automator (EPAM Codemie)

A custom-built AI assistant created specifically for this repository to support automation, documentation, and code analysis.

🔗 Assistant Overview

Name: GenAI Repository Automator
Platform: EPAM Codemie
Created by: Guldana Kassym-Ashim
Purpose: Automates repository analysis, documentation, and improvement workflows.
Status: Active and connected to this GitHub repository.

🧠 Assistant Capabilities

The assistant is able to:

analyze repository structure and files,

explain Python code and workflows,

generate documentation (README, module descriptions, summaries),

identify potential issues and improvement areas,

support research writing and technical explanations,

provide recommendations on automation and CI/CD,

use the repository as a fully indexed datasource.

📦 Connected Datasource

A dedicated datasource named genai-repo is linked to the assistant.

Datasource configuration:

Type: Git

Repository: https://github.com/Guldana2007/genai-applications-guldana

Branch: main

Indexing: Whole codebase

Embedding Model: Text Embedding Ada

Status: COMPLETED (fully indexed)

Screenshots are stored in:
📁 /docs/screenshots/

📂 Project Structure
✔ research.md

A detailed research report describing modern applications of Generative AI: business value, real-world examples, technical challenges, and technological impact.

✔ vocabulary.md

A curated vocabulary of 35+ essential Generative AI terms and verbs used in the research.

✔ stats.py

A Python script that:

extracts vocabulary terms from markdown,

analyzes frequency of usage in research.md,

generates a structured JSON (usage_stats.json),

creates a visual vocabulary relationship graph (vocab_graph.png).

🤖 GitHub Actions Automation

Workflow file: .github/workflows/generate_graph.yml

This workflow executes automatically:

on every push to the main branch,

or manually using Run workflow in GitHub Actions.

Workflow Steps:

Check out the repository

Set up Python

Install dependencies

Run stats.py

Commit and update:

usage_stats.json

vocab_graph.png

Benefits:

Continuous Integration (CI)

Automated analytics

Reproducible execution

Zero manual steps required

📊 Generated Outputs
1️⃣ Vocabulary Relationship Graph

Automatically created visualization:

2️⃣ Word Usage Statistics (Auto-Generated)
Term	Count
generative ai	3
generate	2
context window	1
semantic search	1
alignment	1
latency	1
personalization	1
summarization	1
classification	1
large language model	0
foundation model	0
embeddings	0
tokenization	0
prompt engineering	0
chain of thought	0
few-shot learning	0
zero-shot learning	0
hallucination	0
rag (retrieval-augmented generation)	0
vector database	0
diffusion model	0
fine-tuning	0
inference	0
gpu acceleration	0
multimodal model	0
model drift	0
knowledge base	0
parsing	0
grounding	0
api endpoint	0
safety guardrails	0
function calling	0
orchestration	0
optimization	0
evaluate	0
monitor	0
retrieve	0
transform	0
validate	0
🚀 Run Locally
pip install -r requirements.txt
python stats.py

📎 Additional Documentation
✔ /docs/assistant-overview.md

Overview of Codemie assistant configuration and capabilities.

✔ /docs/datasource.md

Detailed datasource configuration with indexing information.

✔ /docs/screenshots/

Includes images of:

assistant interface,

datasource status (COMPLETED),

workflow settings,

project structure.

🎉 Summary

This project demonstrates a complete integration of:

Generative AI research,

vocabulary engineering,

Python-based text analysis,

automated visualizations,

GitHub Actions automation,

Codemie AI-assisted documentation and code intelligence.

It showcases practical, real-world skills in AI engineering, automation, and repository management.
