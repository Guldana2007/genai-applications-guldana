📘 Generative AI Applications — Research Project

A research project exploring Generative AI applications, vocabulary analytics, automated graph generation, and integration with the EPAM Codemie AI Assistant.

This repository demonstrates practical skills in AI research, Python automation, visualization, CI/CD, and AI-powered documentation.

🤖 Codemie AI Assistant Integration
GenAI Repository Automator (EPAM Codemie)

A custom AI assistant created specifically for this repository to support automation, documentation, analytics, and intelligent insights.

🔍 Assistant Overview

Name: GenAI Repository Automator

Platform: EPAM Codemie

Created by: Guldana Kassym-Ashim

Purpose: Analyze, document, and enhance this repository using AI tools

Status: Active and fully connected to GitHub

🧠 Capabilities

The assistant can:

Analyze repository structure

Explain Python code and workflows

Generate documentation (README, summaries, descriptions)

Suggest improvements and identify issues

Assist with research writing

Provide development recommendations

Use indexed repository data as a knowledge base

📦 Connected Datasource

A linked datasource (genai-repo) allows the assistant to access and process the entire GitHub repository.

Datasource details:

Repository: https://github.com/Guldana2007/genai-applications-guldana

Branch: main

Scope: Whole codebase

Embeddings: Text Embedding Ada

Status: Completed (fully indexed)

📂 Project Structure
research.md

A detailed research analysis of modern Generative AI use cases, challenges, and industry opportunities.

vocabulary.md

A curated vocabulary list of 35+ key AI terms used throughout the research.

stats.py

A Python script that:

extracts vocabulary terms

analyzes their usage frequency

generates usage_stats.json

produces vocab_graph.png (relationship graph)

🔄 GitHub Actions Automation

Workflow file: .github/workflows/generate_graph.yml

Automatically runs when:

pushing to the main branch

manually via Run workflow

What it does:

Sets up Python

Installs dependencies

Executes stats.py

Saves:

usage_stats.json

vocab_graph.png

Ensuring analytics always stay up to date.

📊 Generated Outputs
📌 Vocabulary Relationship Graph

📌 Word Usage Statistics (Auto-Generated)
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
rag	0
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

📁 Additional Documentation

Located in the docs/ folder:

assistant-overview.md — description of the Codemie assistant

datasource.md — indexing and configuration details

screenshots/ — UI screenshots (assistant, datasource, workflows)

🎯 Summary

This repository demonstrates:

Generative AI research

Vocabulary engineering

Automated graph creation

Python analytics

GitHub Actions CI/CD

AI assistant integration (Codemie)

Providing a real-world example of combining development, research, and AI automation.
