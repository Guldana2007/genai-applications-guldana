# **Generative AI Applications — Research and Automation Pipeline**

This repository implements a complete analytical pipeline that extracts vocabulary terms from markdown, computes usage statistics, and automatically generates a vocabulary relationship graph using Python and GitHub Actions.

The project demonstrates practical expertise in:
- research structuring  
- data extraction and processing  
- automated visualization  
- CI/CD engineering  
- repository-integrated AI assistance  

---

# **Codemie AI Assistant Integration**

This repository is connected to a custom Codemie assistant designed to support the project with documentation automation, code explanation, repository analysis, and CI orchestration.

## **Assistant Profile**
**Name:** GenAI Repository Automator  
**Platform:** EPAM Codemie  
**Created by:** Guldana Kassym-Ashim  
**Datasource:** `genai-repo` (full repository index)  
**Status:** Active  

### **Capabilities**
The assistant can:
- analyze the structure and logic of the repository  
- interpret Python scripts and workflows  
- generate descriptions and summaries  
- identify issues or improvement opportunities  
- support research writing  
- trigger the CI pipeline that regenerates `vocab_graph.png`  

---

# Using the Codemie Assistant

This repository is integrated with a custom AI assistant hosted on the EPAM **CodeMie platform**:  
https://codemie.lab.epam.com/  
(the enterprise environment for agentic AI tools and repository-aware assistants).

To access the assistant:

1. Open the CodeMie platform:  
   **https://codemie.lab.epam.com/**

2. Use the option **“Open Repository”** or **“Import from GitHub”**.

3. Provide the repository URL:  
   **https://github.com/Guldana2007/genai-applications-guldana**

4. After the repository loads, the assistant panel will open automatically.

5. All predefined high-level prompts and CI-related commands will become available.

The assistant interacts directly with the repository structure, Python code, markdown content, and GitHub workflows.  
No additional setup is required from the reviewer.


# **System Architecture**

                +------------------------------+
                |         vocabulary.md        |
                +------------------------------+
                            |
                            v
                +------------------------------+
                |          research.md         |
                +------------------------------+
                            |
                            v
                +------------------------------+
                |           stats.py           |
                |------------------------------|
                | - extract terms              |
                | - compute frequencies        |
                | - build usage_stats.json     |
                | - generate vocab_graph.png   |
                +------------------------------+
                            |
                 +----------+-----------+
                 |                      |
                 v                      v
    +--------------------+    +-----------------------+
    |  usage_stats.json  |    |    vocab_graph.png    |
    +--------------------+    +-----------------------+
                            ^
                            |
                +------------------------------+
                |   generate_vocab_graph.py    |
                +------------------------------+
                            ^
                            |
                +------------------------------+
                |  GitHub Actions Workflow     |
                |   generate_graph.yml         |
                +------------------------------+
                            ^
                            |
                +------------------------------+
                |      Codemie Assistant       |
                +------------------------------+


---

# **Continuous Integration (CI)**

GitHub Actions workflow:  
`.github/workflows/generate_graph.yml`

### **Triggered when:**
- `research.md` is updated  
- `vocabulary.md` is updated  
- `stats.py` changes  
- `requirements.txt` changes  
- workflow file updates  
- manual run from the Actions tab  
- the Codemie assistant triggers the pipeline  

---

# **Project Structure**

- **research.md** — structured analysis of Generative AI applications  
- **vocabulary.md** — curated list of AI terminology  
- **stats.py** — extraction, frequency analysis, visualization  
- **generate_vocab_graph.py** — CI entry point  
- **vocab_graph.png** — automatically rendered graph  
- **usage_stats.json** — auto-generated vocabulary frequency data  

---

# **Generated Visualization**

Latest automatically generated graph:

![Vocabulary Graph](./vocab_graph.png)

---

# **Vocabulary Usage Statistics**

| **Term** | **Count** |
|---------|-----------|
| generative ai | 3 |
| generate | 2 |
| context window | 1 |
| semantic search | 1 |
| alignment | 1 |
| latency | 1 |
| personalization | 1 |
| summarization | 1 |
| classification | 1 |
| large language model | 0 |
| foundation model | 0 |
| embeddings | 0 |
| tokenization | 0 |
| prompt engineering | 0 |
| chain of thought | 0 |
| few-shot learning | 0 |
| zero-shot learning | 0 |
| hallucination | 0 |
| rag | 0 |
| vector database | 0 |
| diffusion model | 0 |
| fine-tuning | 0 |
| inference | 0 |
| gpu acceleration | 0 |
| multimodal model | 0 |
| model drift | 0 |
| knowledge base | 0 |
| parsing | 0 |
| grounding | 0 |
| api endpoint | 0 |
| safety guardrails | 0 |
| function calling | 0 |
| orchestration | 0 |
| optimization | 0 |
| evaluate | 0 |
| monitor | 0 |
| retrieve | 0 |
| transform | 0 |
| validate | 0 |

---

# **Running the Project Locally**

pip install -r requirements.txt
python stats.py


This produces:
- `usage_stats.json`  
- `vocab_graph.png`  

---

# **Project Improvement Opportunities**

Several improvements could extend the project’s functionality and visual quality:

- **Interactive visualization**  
  Converting the static PNG to an interactive graph (D3.js / Plotly) with zooming, filtering, clustering.

- **Automated README updates**  
  Updating the generated statistics table inside the README automatically during each CI run.

- **Extended NLP features**  
  Adding lemmatization, phrase detection, and semantic clustering could improve the depth of analysis.

- **External image-generation integration**  
  A more advanced illustration could be created by integrating with external services such as  
  *Leonardo.ai*, *Midjourney API*, or *Stability AI*.  
  These platforms can render highly detailed conceptual diagrams.  
  However, they are paid platforms, and Codemie currently does not support direct image generation or external API calls.  

  A generated image could look like this:

  **(Insert generated image here once available)**

This would significantly enhance the presentation value of the project.

---

# **Summary**

This project combines structured research, automated term extraction, Python-based analytics, CI-driven visualization, and an integrated AI assistant.  
It provides a robust, reproducible workflow that aligns academic rigor with modern engineering practices.

