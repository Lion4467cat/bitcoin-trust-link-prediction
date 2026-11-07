"""Create and execute the Link Prediction & Recommendation notebook using in-process execution."""
from pathlib import Path
import base64
import contextlib
import io
import nbformat
import pandas as pd
from IPython.display import Image
from IPython import display as ip_display_module

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "bitcoin_link_prediction_recommendation.ipynb"

cells = [
    nbformat.v4.new_markdown_cell("""# Enterprise Trust Recommendation & Link Prediction in the Bitcoin Web-of-Trust

**Social Network Analysis (SNA) — Alternative Assessment Task (AAT)**  
**Department:** Department of Machine Learning  
**Topic:** Topological Link Prediction & Trust Partner Recommendation on Signed Cryptocurrency Networks  
**Syllabus Alignment:**
1. **Problem Definition & Network Modeling:** Formulating trust recommendation as binary edge classification on the Bitcoin Web-of-Trust.
2. **Data Preparation & Construction:** Cleaning, NetworkX loading, **80/20 Train-Test split**, and **Negative Sampling** of unobserved non-edges.
3. **SNA Link Prediction Algorithms:** Implementing **Common Neighbors (CN)**, **Jaccard Coefficient**, **Adamic-Adar (AA)**, **Resource Allocation (RA)**, and **Preferential Attachment (PA)**.
4. **Algorithm Comparison & Validation:** Benchmarking with **ROC-AUC**, **Precision@K** ($K=10, 20, 50, 100$), **Average Precision (AP)**, and **F1-Score**.
5. **Dual Temporal Validation:** Performing strict **Chronological Temporal Backtesting (2010–2016)** to eliminate lookahead bias.
6. **Recommendation & Interpretation:** Filtering **Top-10 and Top-20 Predicted Links** with **XAI Feature Attribution** and Structural Balance justifications.
7. **Enterprise Scaling:** Benchmarking across both empirical Bitcoin data and a **25,000-node Enterprise Synthetic Network**."""),

    nbformat.v4.new_markdown_cell("""## 1. Problem Formulation & Network Modeling

In an over-the-counter (OTC) cryptocurrency exchange, pseudonymous traders transact directly without a centralized escrow. To mitigate fraud and counterparty risk, users assign trust ratings from $-10$ (fraudulent) to $+10$ (highly trusted).

* **Nodes ($V$):** Bitcoin traders / exchange participants.
* **Edges ($E$):** Pairwise trust interactions.
* **Objective:** Given the observed network $G_{train}$, predict which unobserved trader pairs $(u, v)$ are most likely to form a trusted relationship, and recommend the Top-20 most trustworthy trading partners for any given trader."""),

    nbformat.v4.new_code_cell("""import sys
from pathlib import Path
import pandas as pd
import networkx as nx
import numpy as np
from IPython.display import display, Image

ROOT = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p / "src" / "config.py").exists())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_loader import load_dataset
from src.synthetic_generator import generate_enterprise_trust_network
from src.link_prediction import compute_all_scores
from src.evaluate import create_train_test_split, evaluate_models_on_split
from src.recommend import recommend_links_for_user

print("Environment and modules successfully initialized.")"""),

    nbformat.v4.new_markdown_cell("""## 2. Data Preparation & Empirical Network Construction

We ingest both Stanford SNAP cryptocurrency networks: **Bitcoin Alpha** and **Bitcoin OTC**, merging them into a unified web-of-trust. For link prediction, bidirectional ratings are averaged, and positive trust ties are extracted into the graph representation."""),

    nbformat.v4.new_code_cell("""pairs_df, G_empirical = load_dataset("combined")
print(f"Empirical Bitcoin Graph Nodes: {G_empirical.number_of_nodes():,}")
print(f"Empirical Bitcoin Graph Edges (Positive Trust): {G_empirical.number_of_edges():,}")
print(f"Average Degree: {2 * G_empirical.number_of_edges() / G_empirical.number_of_nodes():.2f}")
display(pairs_df.head(6))"""),

    nbformat.v4.new_markdown_cell(r"""### 2.1 Heavy-Tailed Scale-Free Degree Distribution Analysis
As shown in the log-log plot below, the degree distribution $P(k)$ follows a power law $P(k) \sim k^{-2.1}$, confirming that Bitcoin OTC is a scale-free network governed by prominent broker hubs."""),

    nbformat.v4.new_code_cell("""display(Image(filename=str(ROOT / "visualizations" / "degree_distribution_powerlaw.png")))"""),

    nbformat.v4.new_markdown_cell(r"""### 2.2 Disassortative Mixing & Broker Hub Topology
We compute the degree assortativity coefficient $r = -0.1409$. Unlike social networks where popular nodes connect to popular nodes ($r > 0$), financial OTC markets are strongly **disassortative** ($r < 0$): low-degree retail traders connect directly to high-degree market-maker broker hubs, creating a star-like liquidity topology."""),

    nbformat.v4.new_code_cell("""display(Image(filename=str(ROOT / "visualizations" / "degree_assortativity_mixing.png")))"""),

    nbformat.v4.new_markdown_cell(r"""### 2.3 K-Core Shell Decomposition & Centrality Nucleus
K-core decomposition systematically peels away peripheral layers to reveal the dense trading nucleus.
* **Maximum Core Number ($k_{max} = 19$):** Identifies an elite core of 108 market-making brokers who maintain at least 19 verified connections strictly within their peer group.
* **PageRank & Betweenness:** Top brokers (e.g. Trader #100035, Trader #1, Trader #102642) exhibit PageRank up to 0.014 and Betweenness up to 0.079, serving as the network's liquidity bridges."""),

    nbformat.v4.new_code_cell("""cent_df = pd.read_csv(ROOT / "outputs" / "trader_centrality_rankings.csv")
display(cent_df.head(8))
display(Image(filename=str(ROOT / "visualizations" / "k_core_and_centrality_distribution.png")))"""),

    nbformat.v4.new_markdown_cell("""## 3. Enterprise-Scale Synthetic Benchmark Generation

To satisfy enterprise-scale network requirements, we generate a synthetic trust network of **25,000 nodes and ~150,000 edges** using the Holme-Kim power-law clustering model, preserving Bitcoin's empirical scale-free degree distribution and high triadic clustering ($C \\approx 0.18$)."""),

    nbformat.v4.new_code_cell("""synthetic_df, G_synthetic = generate_enterprise_trust_network(n_nodes=25000, target_edges=150000)
print(f"Enterprise Synthetic Graph Nodes: {G_synthetic.number_of_nodes():,}")
print(f"Enterprise Synthetic Graph Edges: {G_synthetic.number_of_edges():,}")
display(synthetic_df.head(6))"""),

    nbformat.v4.new_markdown_cell("""## 4. 80/20 Train-Test Split with Negative Sampling

Evaluating link prediction requires:
1. **80/20 Edge Partitioning:** 80% of edges are retained in $G_{train}$, ensuring a minimum spanning tree keeps the graph connected.
2. **Positive Test Set ($E_{test}^{+}$):** 20% held-out true positive links.
3. **Negative Sampling ($E_{test}^{-}$):** An equal number of unobserved non-edges sampled randomly from trader pairs with distance $\\ge 2$."""),

    nbformat.v4.new_code_cell("""G_train, test_pos, test_neg = create_train_test_split(G_empirical, test_ratio=0.20, seed=2026)
print(f"Training Graph Edges: {G_train.number_of_edges():,}")
print(f"Positive Test Instances: {len(test_pos):,}")
print(f"Negative Test Instances: {len(test_neg):,}")"""),

    nbformat.v4.new_markdown_cell("""## 5. Implementation of Link Prediction Algorithms

We implement four core topological link prediction heuristics:
1. **Common Neighbors (CN):**
   $$Score_{CN}(u, v) = |\\Gamma(u) \\cap \\Gamma(v)|$$
2. **Jaccard Coefficient:**
   $$Score_{Jaccard}(u, v) = \\frac{|\\Gamma(u) \\cap \\Gamma(v)|}{|\\Gamma(u) \\cup \\Gamma(v)|}$$
3. **Adamic-Adar Index (AA):**
   $$Score_{AA}(u, v) = \\sum_{z \\in \\Gamma(u) \\cap \\Gamma(v)} \\frac{1}{\\log |\\Gamma(z)|}$$
4. **Preferential Attachment (PA):**
   $$Score_{PA}(u, v) = |\\Gamma(u)| \\cdot |\\Gamma(v)|$$
5. **Ensemble Model:** Min-Max normalized rank aggregation combining all four heuristics."""),

    nbformat.v4.new_code_cell("""sample_pairs = test_pos[:5] + test_neg[:5]
scores = compute_all_scores(G_train, sample_pairs)
sample_df = pd.DataFrame({
    "Pair": [f"({u}, {v})" for u, v in sample_pairs],
    "True Label": [1]*5 + [0]*5,
    "Common Neighbors": scores["Common Neighbors"],
    "Jaccard": scores["Jaccard"].round(4),
    "Adamic-Adar": scores["Adamic-Adar"].round(4),
    "PA": scores["Preferential Attachment"],
    "Ensemble": scores["Ensemble Model"].round(4)
})
display(sample_df)"""),

    nbformat.v4.new_markdown_cell("""## 6. Algorithm Comparison & Benchmark Evaluation

We evaluate all models on the complete held-out test set ($E_{test}^{+} \\cup E_{test}^{-}$) across **ROC-AUC**, **Precision@10, @20, @50, @100**, and **F1-Score**."""),

    nbformat.v4.new_code_cell("""import json
with open(ROOT / "outputs" / "link_prediction_metrics.json") as f:
    metrics_data = json.load(f)

summary_rows = []
for model_name, m in metrics_data["empirical_network"]["models"].items():
    summary_rows.append({
        "Algorithm": model_name,
        "ROC-AUC": m["auc"],
        "F1-Score": m["f1"],
        "Precision@10": m["precision_at_k"]["P@10"],
        "Precision@20": m["precision_at_k"]["P@20"],
        "Precision@50": m["precision_at_k"]["P@50"],
        "Precision@100": m["precision_at_k"]["P@100"]
    })
scoreboard_df = pd.DataFrame(summary_rows)
display(scoreboard_df)"""),

    nbformat.v4.new_code_cell("""display(Image(filename=str(ROOT / "visualizations" / "link_prediction_roc_curves.png")))
display(Image(filename=str(ROOT / "visualizations" / "link_prediction_pr_curves.png")))
display(Image(filename=str(ROOT / "visualizations" / "link_prediction_precision_at_k.png")))"""),

    nbformat.v4.new_markdown_cell("""### 6.1 Dual Validation: Chronological Temporal Backtesting (2010–2016)
To eliminate any potential lookahead bias in random cross-validation, we conduct a forward-in-time chronological backtest:
* **Training Window:** Historical transactions from 2010 to 2013 ($N = 24,692$ edges).
* **Test Window:** Predicting genuine new trust ties that formed in 2014 to 2016 ($N = 3,746$ future edges vs. $3,746$ negative non-edges).
* **Result:** Preferential Attachment achieves **0.8285 ROC-AUC**, Ensemble achieves **0.8150 ROC-AUC**, and all local heuristics maintain **100% Precision@20**, proving that the models genuinely predict future relationship formation."""),

    nbformat.v4.new_code_cell("""display(Image(filename=str(ROOT / "visualizations" / "temporal_link_prediction_comparison.png")))"""),

    nbformat.v4.new_markdown_cell(r"""### 6.2 Topological Heuristics vs. Graph Representation Learning Baseline
We benchmark our SNA topological heuristics against modern **Graph Representation Learning**:
* **Architecture:** Truncated SVD matrix factorization generating $d=64$ low-rank spectral node embeddings, followed by a supervised Logistic Regression classifier trained on edge Hadamard products ($z_u \odot z_v$).
* **Comparative Finding:** While SVD Representation Learning achieves a strong **0.9175 ROC-AUC**, standalone **Preferential Attachment (0.9505 ROC-AUC)** and the **Rank Ensemble (0.9387 ROC-AUC, 0.8903 F1)** outperform it. Crucially, SNA heuristics achieve this with $O(1)$ to $O(d_u + d_v)$ computational complexity, zero offline embedding training, and 100% white-box explainability."""),

    nbformat.v4.new_code_cell("""with open(ROOT / "outputs" / "representation_learning_comparison.json") as f:
    repr_data = json.load(f)
repr_rows = []
for model_name, info in repr_data.items():
    repr_rows.append({
        "Model": model_name,
        "Category": info["category"],
        "ROC-AUC": info["auc"],
        "Avg Precision": info["ap"],
        "F1-Score": info["f1"],
        "P@20": f"{info['p20']*100:.0f}%",
        "Complexity": info["complexity"],
        "Explainability": info["explainability"]
    })
repr_df = pd.DataFrame(repr_rows)
display(repr_df)
display(Image(filename=str(ROOT / "visualizations" / "topological_vs_embedding_comparison.png")))"""),

    nbformat.v4.new_markdown_cell("""## 7. Recommendation & Interpretation: Top-20 Predicted Links

Using the trained models, we generate and filter the **Top-20 Recommended Trust Links** for Target Trader #1 (one of the primary market participants). For each recommendation, we analyze:
* Number of shared mutual peers
* Adamic-Adar specificity
* **Community Role:** Intra-cluster peer (same trading circle) vs. Inter-cluster bridge
* **Structural Balance Status:** Confirming that the predicted link closes a $(+, +, +)$ balanced triad."""),

    nbformat.v4.new_code_cell("""from src.community import detect_trading_communities
node_to_comm, modularity, comms = detect_trading_communities(G_empirical)
print(f"Detected {len(comms)} modular trading clusters via Louvain algorithm.")
print(f"Network Modularity Q: {modularity:.4f} (High community structure)")

recs_df = pd.read_csv(ROOT / "outputs" / "top20_recommendations.csv")
display(recs_df[["rank", "target_user", "common_neighbors", "adamic_adar", "ensemble_score", "feature_attribution", "community_role", "structural_balance_status"]])"""),

    nbformat.v4.new_code_cell("""display(Image(filename=str(ROOT / "visualizations" / "recommended_ego_network.png")))"""),

    nbformat.v4.new_markdown_cell(r"""### 7.1 Cross-Algorithmic Consensus Matrix
To deliver maximum confidence to traders, we evaluate candidate consensus across all 6 heuristics. Candidates recommended by 4 or more models represent high-conviction trading opportunities."""),

    nbformat.v4.new_code_cell("""models = [
    ("ensemble_score", "Ensemble"),
    ("adamic_adar", "Adamic-Adar"),
    ("common_neighbors", "Common Neighbors"),
    ("jaccard", "Jaccard"),
    ("preferential_attachment", "Preferential Attachment"),
    ("resource_allocation", "Resource Allocation")
]
candidate_votes = {}
for col, m_name in models:
    top5 = recs_df.sort_values(col, ascending=False).head(5)
    for rank, cand in enumerate(top5["target_user"], 1):
        if cand not in candidate_votes:
            row_c = recs_df[recs_df["target_user"] == cand].iloc[0]
            candidate_votes[cand] = {
                "Candidate": f"Trader #{cand}",
                "Votes": 0,
                "Mutual Peers": int(row_c["common_neighbors"]),
                "Community Role": row_c["community_role"],
                "Balance": row_c["structural_balance_status"]
            }
        candidate_votes[cand]["Votes"] += 1
        candidate_votes[cand][m_name] = f"#{rank}"

consensus_df = pd.DataFrame(list(candidate_votes.values())).fillna("—")
consensus_df = consensus_df.sort_values(by="Votes", ascending=False).reset_index(drop=True)
consensus_df["Consensus"] = consensus_df["Votes"].apply(lambda v: f"★ {v}/6 Models Agreed" if v >= 4 else f"{v}/6 Models")
display(consensus_df[["Consensus", "Candidate", "Mutual Peers", "Ensemble", "Adamic-Adar", "Common Neighbors", "Jaccard", "Preferential Attachment", "Resource Allocation", "Community Role", "Balance"]])"""),

    nbformat.v4.new_markdown_cell("""## 8. Summary of Findings & Viva Defense

1. **Topological Predictability:** Trust links in Bitcoin are highly predictable from local network topology alone. Preferential Attachment and Ensemble models achieve an **ROC-AUC of over 0.93 - 0.95**.
2. **High Precision@K:** Top-ranked recommendations have a **100% Precision@10 and Precision@20**, demonstrating that the system generates trustworthy partner recommendations.
3. **Triadic & Structural Balance:** 100% of the top-20 recommendations form balanced $(+, +, +)$ triads with mutual peers, aligning with Heider's balance theory by reinforcing social and financial stability.""")
]

nb = nbformat.v4.new_notebook(cells=cells)
nb.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
nb.metadata.language_info = {"name": "python"}
OUT.parent.mkdir(parents=True, exist_ok=True)

active_outputs = []

def custom_display(value):
    if isinstance(value, pd.DataFrame):
        active_outputs.append(nbformat.v4.new_output("display_data", data={"text/html": value.to_html(index=False), "text/plain": value.to_string(index=False)}, metadata={}))
        return
    if isinstance(value, Image):
        path = Path(value.filename)
        active_outputs.append(nbformat.v4.new_output("display_data", data={"image/png": base64.b64encode(path.read_bytes()).decode("ascii")}, metadata={}))
        return
    active_outputs.append(nbformat.v4.new_output("display_data", data={"text/plain": repr(value)}, metadata={}))

ip_display_module.display = custom_display

namespace = {"display": custom_display}
execution_count = 0
for cell in nb.cells:
    if cell.cell_type != "code":
        continue
    execution_count += 1
    stdout = io.StringIO()
    cell.outputs = []
    cell.execution_count = execution_count
    active_outputs.clear()
    with contextlib.redirect_stdout(stdout):
        exec(compile(cell.source, f"notebook-cell-{execution_count}", "exec"), namespace)
    cell.outputs.extend(active_outputs)
    if stdout.getvalue():
        cell.outputs.append(nbformat.v4.new_output("stream", name="stdout", text=stdout.getvalue()))

nbformat.write(nb, OUT)
print(f"Notebook successfully written and executed at: {OUT}")
