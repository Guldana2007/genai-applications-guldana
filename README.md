# 📘 Generative AI Applications — Research Project  
### *Use Cases, Vocabulary Analytics, Automated Graph Generation*

This project presents a complete analytical workflow around Generative AI, including a curated vocabulary, usage frequency analysis, and an automatically generated relationship graph using GitHub Actions. It demonstrates research skills, Python text processing, visualization, and automation practices.

---

## 📂 Project Structure

### ✔ research.md  
A detailed research report describing modern applications of Generative AI: business value, real-world examples, technical challenges, and opportunities.

### ✔ vocabulary.md  
A manually created vocabulary of 35+ key Generative AI terms and verbs with clear definitions.

### ✔ stats.py  
A Python script that:
- extracts vocabulary terms,
- scans the research report,
- counts usage frequency,
- generates usage_stats.json,
- creates vocab_graph.png (relationship graph).

---

## 🤖 GitHub Actions Automation  
Workflow: `.github/workflows/generate_graph.yml`

The workflow runs:
- on every push to the main branch,
- or manually via “Run workflow”.

Workflow steps:
1. Check out the repository  
2. Set up Python  
3. Install dependencies  
4. Execute stats.py  
5. Commit updated files:
   - vocab_graph.png  
   - usage_stats.json  

### Benefits:
- reproducibility  
- CI/CD automation  
- seamless Python + GitHub integration  
- always up-to-date analytics  

---

## 📊 Generated Outputs

### 1️⃣ Vocabulary Relationship Graph  
Automatically generated visualization:

![Vocabulary Graph](vocab_graph.png)

### 2️⃣ Frequency Statistics  
Automatically generated JSON file (`usage_stats.json`) containing vocabulary term usage counts.

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
python stats.py
