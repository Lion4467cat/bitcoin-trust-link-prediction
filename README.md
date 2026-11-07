# Enterprise Trust Recommendation & Link Prediction in the Bitcoin Web-of-Trust

> **Course:** Social Network Analysis (SNA) — Alternative Assessment Task (AAT)  
> **Department:** Department of Machine Learning  
> **Topic:** Topological Link Prediction & Trust Partner Recommendation in Decentralized Cryptocurrency Networks

An end-to-end Social Network Analysis (SNA) research project for the **Alternative Assessment Task (AAT)**. This project investigates topological link prediction and trust partner recommendation in decentralized, pseudonymous cryptocurrency trading networks.

---

## Executive Summary & Scoreboard

In over-the-counter (OTC) cryptocurrency exchange networks, anonymous traders face acute counterparty risk without centralized intermediaries. This project models trust formation as a topological link prediction task across both **empirical Bitcoin networks** (Stanford SNAP Bitcoin Alpha & Bitcoin OTC) and an **Enterprise-Scale Synthetic Benchmark (25,000 nodes, 135,857 edges)**.

### Model Performance Scoreboard (Held-Out 80/20 Test Split — 7,294 Instances)

| Algorithm | Model Category | ROC-AUC | F1-Score | Avg Precision | Precision@10 | Precision@20 | Precision@50 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Preferential Attachment (PA)** | Global Degree Scale-Free | **0.9505** | **0.8864** | **0.9532** | **1.000** | **1.000** | **1.000** |
| **Ensemble Model** | Normalized Rank Borda Sum | **0.9387** | **0.8903** | **0.9412** | **1.000** | **0.950** | 0.600 |
| **Adamic-Adar Index (AA)** | Degree-Weighted Neighbors | **0.8366** | 0.6667 | 0.8401 | **1.000** | **1.000** | **1.000** |
| **Resource Allocation (RA)** | Physical Resource Flow | **0.8340** | 0.6667 | 0.8385 | **1.000** | **1.000** | **1.000** |
| **Common Neighbors (CN)** | Direct Triadic Overlap | **0.8335** | 0.6667 | 0.8378 | **1.000** | **1.000** | **1.000** |
| **Jaccard Coefficient** | Union-Normalized Overlap | **0.8161** | 0.6667 | 0.8210 | 0.200 | 0.150 | 0.380 |

### Key Scientific Invariants & Discoveries
* **Scale-Free Network Topology:** Empirical degree analysis confirms that the Bitcoin Web-of-Trust follows a heavy-tailed power law $P(k) \sim k^{-2.1}$. Reputable broker hubs dominate volume, explaining the extraordinary global discrimination of Preferential Attachment.
* **Community Detection & Roles:** Louvain community detection partitions the 9,207 traders into 88 modular communities ($Q = 0.6402$). Recommended links are classified as either **Intra-Cluster Peers** (reinforcing existing trading circles) or **Inter-Cluster Bridges** (connecting across trading rings).
* **Enterprise Synthetic Scaling (25,000 Nodes):** The Ensemble model maintains an **ROC-AUC of 0.7539** and **100% Precision@10 and Precision@20** on the 25k-node synthetic graph, proving industrial scalability.
* **Heider's Structural Balance Grounding:** 100% of the Top-20 model-recommended trading ties close verified $(+, +, +)$ triads with mutual peers, satisfying Cartwright-Harary balance theory and minimizing community friction.

---

## Course Assessment Rubric & Deliverables Checklist

| Rubric Deliverable | File Path | Status |
| :--- | :--- | :---: |
| **Deliverable 1: Source Code & Executable Notebook** | [`src/`](file:///home/tinkerer/Desktop/SNA-AAT/src/) & [`notebooks/bitcoin_link_prediction_recommendation.ipynb`](file:///home/tinkerer/Desktop/SNA-AAT/notebooks/bitcoin_link_prediction_recommendation.ipynb) | ✅ **100% Complete** (1.3 MB Executed) |
| **Deliverable 2: Network Dataset Package** | [`dataset_package/bitcoin_trust_dataset_package.zip`](file:///home/tinkerer/Desktop/SNA-AAT/dataset_package/bitcoin_trust_dataset_package.zip) | ✅ **100% Complete** (1.64 MB with SHA-256) |
| **Deliverable 3: Network Visualization Artifacts** | [`visualizations/`](file:///home/tinkerer/Desktop/SNA-AAT/visualizations/) & [`outputs/bitcoin_link_prediction.graphml`](file:///home/tinkerer/Desktop/SNA-AAT/outputs/bitcoin_link_prediction.graphml) | ✅ **100% Complete** (PNG, SVG, Cytoscape) |
| **Deliverable 4: Formatted Evaluation Report** | [`reports/link_prediction_report.pdf`](file:///home/tinkerer/Desktop/SNA-AAT/reports/link_prediction_report.pdf) | ✅ **100% Complete** (Exact 8-Page Academic PDF) |
| **Deliverable 5: Presentation Deck (.pptx / .pdf)** | [`slides/link_prediction_presentation.pptx`](file:///home/tinkerer/Desktop/SNA-AAT/slides/link_prediction_presentation.pptx) & [`.pdf`](file:///home/tinkerer/Desktop/SNA-AAT/slides/link_prediction_presentation.pdf) | ✅ **100% Complete** (14 Slides, 3-Speaker Plan) |
| **Bonus: Interactive Web Dashboard** | [`src/serve.py`](file:///home/tinkerer/Desktop/SNA-AAT/src/serve.py) running at `http://localhost:5000` | ✅ **100% Complete** (100% Offline-Ready) |
| **Bonus: Team Presentation & Viva Study Guide** | [`TEAM_STUDY_GUIDE.md`](file:///home/tinkerer/Desktop/SNA-AAT/TEAM_STUDY_GUIDE.md) & [`reports/team_presentation_study_guide.pdf`](file:///home/tinkerer/Desktop/SNA-AAT/reports/team_presentation_study_guide.pdf) | ✅ **100% Complete** (Word-for-Word Scripts) |
| **Bonus: Automated Test Suite** | [`tests/test_pipeline.py`](file:///home/tinkerer/Desktop/SNA-AAT/tests/test_pipeline.py) | ✅ **100% Complete** (10 of 10 Passed) |

---

## 3-Person Team Presentation Structure

The slide deck ([`slides/link_prediction_presentation.pdf`](file:///home/tinkerer/Desktop/SNA-AAT/slides/link_prediction_presentation.pdf)) and study guide are structured into 3 distinct speaker allocations:

```
┌────────────────────────────────────────────────────────────────────────┐
│ SPEAKER 1: Problem Definition, Datasets, Scale-Free Topology & 80/20   │
│            (Slides 1 – 5)                                              │
├────────────────────────────────────────────────────────────────────────┤
│ SPEAKER 2: The 5 Algorithms (CN, Jaccard, AA, RA, PA) & Ensemble       │
│            (Slides 6 – 9)                                              │
├────────────────────────────────────────────────────────────────────────┤
│ SPEAKER 3: Results (ROC/PR), Precision@K, Top-20 Demo & Viva Defense   │
│            (Slides 10 – 14)                                            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Project Directory Map

```
SNA-AAT/
├── data/
│   ├── soc-sign-bitcoinalpha.csv.gz    # Stanford SNAP Bitcoin Alpha (3,783 users, 24,186 ratings)
│   └── soc-sign-bitcoinotc.csv.gz      # Stanford SNAP Bitcoin OTC (5,887 users, 35,592 ratings)
├── src/
│   ├── config.py                       # Project paths, constants, random seeds
│   ├── data_loader.py                  # Ingestion, validation, undirected projection (9,207 nodes)
│   ├── synthetic_generator.py          # 25,000-node Holme-Kim power-law clustering generator
│   ├── link_prediction.py              # CN, Jaccard, AA, RA, PA, and Ensemble models
│   ├── evaluate.py                     # 80/20 MST train/test split, negative sampling, ROC/PR
│   ├── community.py                    # Louvain community detection & tie classification
│   ├── recommend.py                    # Top-10 / Top-20 recommendation engine & ego plotter
│   ├── run_pipeline.py                 # Master end-to-end pipeline execution script
│   └── serve.py                        # Ultra-fast light-themed web server (port 5000)
├── tests/
│   └── test_pipeline.py                # 10 unit & integration tests (pytest / unittest)
├── notebooks/
│   └── bitcoin_link_prediction_recommendation.ipynb  # Executable notebook (1.3 MB with plots)
├── outputs/
│   ├── bitcoin_synthetic_enterprise.csv# 25k-node synthetic enterprise dataset
│   ├── bitcoin_link_prediction.graphml # Complete Cytoscape signed graph (5.2 MB)
│   ├── link_prediction_metrics.json    # JSON benchmarks (ROC-AUC, Precision@K, F1, AP)
│   └── top20_recommendations.csv       # Model-ranked Top-20 recommendations with roles
├── visualizations/
│   ├── vis-network.min.js              # Bundled local Vis.js library (100% offline)
│   ├── link_prediction_roc_curves.png  # High-res ROC curves (PNG & SVG)
│   ├── link_prediction_pr_curves.png   # Precision-Recall curves (PNG & SVG)
│   ├── link_prediction_precision_at_k.png # Precision@K comparison chart (PNG & SVG)
│   ├── degree_distribution_powerlaw.png# Log-log degree distribution power-law fit (PNG & SVG)
│   ├── recommended_ego_network.png     # Ego network with predicted ties (PNG & SVG)
│   └── interactive_recommendation_demo.html # Standalone offline interactive HTML demo
├── reports/
│   ├── build_link_prediction_report.py # ReportLab PDF builder
│   ├── link_prediction_report.pdf      # Polished, publication-grade 8-page academic report
│   ├── build_study_guide_pdf.py        # Team study guide PDF builder
│   └── team_presentation_study_guide.pdf # Printable 2-page viva cheat sheet
├── slides/
│   ├── build_link_prediction_deck.py   # PPTX slide builder & LibreOffice PDF exporter
│   ├── link_prediction_presentation.pptx # 16:9 widescreen presentation deck (14 slides)
│   └── link_prediction_presentation.pdf  # PDF export of presentation slides
└── dataset_package/
    └── bitcoin_trust_dataset_package.zip # Complete data package with SHA-256 manifest (1.64 MB)
```

---

## Quick Start & Reproduction

### 1. Run Automated Unit Tests
```bash
.venv/bin/pytest tests/test_pipeline.py
```

### 2. Run Master End-to-End Pipeline
```bash
MPLCONFIGDIR=/tmp .venv/bin/python src/run_pipeline.py
```
This single command:
1. Ingests and merges Bitcoin Alpha + OTC datasets (9,207 traders, 31,050 edges).
2. Generates the 25,000-node Enterprise Synthetic Trust Network (135,857 edges).
3. Performs 80/20 train-test splits with spanning-tree connectivity protection and negative sampling.
4. Computes all link prediction heuristics (CN, Jaccard, AA, RA, PA, Ensemble).
5. Generates high-res ROC curves, PR curves, Precision@K bar charts, and power-law distribution plots.
6. Exports Top-20 recommendations with community roles and Cytoscape GraphML.

### 3. Launch the Interactive Web Dashboard
```bash
MPLCONFIGDIR=/tmp .venv/bin/python src/serve.py 5000
```
Open **`http://localhost:5000`** in any web browser to:
* Select any Bitcoin Trader ID (e.g. Trader #1, #2, #7, #14, #33, #177).
* Switch between models (Common Neighbors, Jaccard, Adamic-Adar, RA, PA, Ensemble).
* Explore the live force-directed ego network with existing trust ties (solid teal) and predicted links (dashed purple).
* View live Top-10 / Top-20 recommendations with Adamic-Adar scores, community roles, and structural balance verification.
* Export recommendations directly as a CSV file.

### 4. Rebuild All Deliverables
```bash
# Rebuild executed Jupyter Notebook
MPLCONFIGDIR=/tmp .venv/bin/python scripts/build_link_prediction_notebook.py

# Rebuild Dataset Package ZIP with SHA-256
MPLCONFIGDIR=/tmp .venv/bin/python scripts/package_dataset.py

# Rebuild 8-Page Formal Academic Report
MPLCONFIGDIR=/tmp .venv/bin/python reports/build_link_prediction_report.py

# Rebuild 14-Slide Presentation Deck (PPTX & PDF)
MPLCONFIGDIR=/tmp .venv/bin/python slides/build_link_prediction_deck.py

# Rebuild Team Viva Study Guide PDF
MPLCONFIGDIR=/tmp .venv/bin/python reports/build_study_guide_pdf.py
```

---

## References & Academic Grounding
* Stanford Network Analysis Project (SNAP): [Bitcoin Alpha](https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html) and [Bitcoin OTC](https://snap.stanford.edu/data/soc-sign-bitcoinotc.html).
* Kumar, S., Spezzano, F., Subrahmanian, V. S., & Faloutsos, C. (2016). *“Edge Weight Prediction in Weighted Signed Networks.”* IEEE International Conference on Data Mining (ICDM).
* Liben-Nowell, D., & Kleinberg, J. (2007). *“The Link-Prediction Problem for Social Networks.”* Journal of the American Society for Information Science and Technology.
* Zhou, T., Lü, L., & Zhang, Y. C. (2009). *“Predicting Missing Links via Local Information.”* The European Physical Journal B.
* Cartwright, D., & Harary, F. (1956). *“Structural Balance: A Generalization of Heider’s Theory.”* Psychological Review.
