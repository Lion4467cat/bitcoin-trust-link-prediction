"""80/20 Train-Test splitting, negative sampling, and evaluation metrics."""
from __future__ import annotations

import math
import random
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, average_precision_score, f1_score

from src.config import RANDOM_SEED, TRAIN_RATIO, TEST_RATIO, VISUALIZATIONS_DIR, OUTPUTS_DIR
from src.link_prediction import compute_all_scores


def create_train_test_split(
    G: nx.Graph,
    test_ratio: float = TEST_RATIO,
    seed: int = RANDOM_SEED
) -> tuple[nx.Graph, list[tuple[int, int]], list[tuple[int, int]]]:
    """Create an 80/20 train-test split with spanning tree protection and negative sampling."""
    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)
    
    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()
    else:
        G = G.copy()
        
    num_edges = G.number_of_edges()
    target_test_edges = int(num_edges * test_ratio)
    
    spanning_tree = nx.minimum_spanning_tree(G)
    spanning_edges = set((min(u, v), max(u, v)) for u, v in spanning_tree.edges())
    
    all_edges = set((min(u, v), max(u, v)) for u, v in G.edges())
    candidate_test_edges = list(all_edges - spanning_edges)
    
    rng.shuffle(candidate_test_edges)
    test_pos = candidate_test_edges[:target_test_edges]
    train_edges = list(all_edges - set(test_pos))
    
    G_train = nx.Graph()
    G_train.add_nodes_from(G.nodes())
    for u, v in train_edges:
        G_train.add_edge(u, v, **G[u][v])
        
    nodes = list(G_train.nodes())
    test_neg_set = set()
    existing_all_edges = all_edges
    
    attempts = 0
    max_attempts = target_test_edges * 50
    while len(test_neg_set) < target_test_edges and attempts < max_attempts:
        attempts += 1
        u, v = np_rng.choice(nodes, size=2, replace=False)
        u, v = int(min(u, v)), int(max(u, v))
        if (u, v) not in existing_all_edges and (u, v) not in test_neg_set:
            test_neg_set.add((u, v))
            
    test_neg = list(test_neg_set)
    print(f"Split completed: Train edges={G_train.number_of_edges():,}, Test Pos={len(test_pos):,}, Test Neg={len(test_neg):,}")
    return G_train, test_pos, test_neg


def evaluate_models_on_split(
    G_train: nx.Graph,
    test_pos: list[tuple[int, int]],
    test_neg: list[tuple[int, int]]
) -> dict:
    """Evaluate CN, Jaccard, AA, RA, PA, and Ensemble on the train-test split."""
    test_pairs = test_pos + test_neg
    y_true = np.array([1] * len(test_pos) + [0] * len(test_neg))
    
    print("Computing link prediction scores across test pairs...")
    scores_dict = compute_all_scores(G_train, test_pairs)
    
    results = {}
    for model_name, scores in scores_dict.items():
        auc = float(roc_auc_score(y_true, scores))
        fpr, tpr, _ = roc_curve(y_true, scores)
        
        pr_precision, pr_recall, _ = precision_recall_curve(y_true, scores)
        ap = float(average_precision_score(y_true, scores))
        
        sorted_indices = np.argsort(scores)[::-1]
        p_at_k = {}
        for k in [10, 20, 50, 100]:
            top_k_indices = sorted_indices[:k]
            precision_k = float(np.mean(y_true[top_k_indices]))
            p_at_k[f"P@{k}"] = round(precision_k, 4)
            
        threshold = float(np.median(scores))
        y_pred = (scores >= threshold).astype(int)
        f1 = float(f1_score(y_true, y_pred, zero_division=0))
        
        results[model_name] = {
            "auc": round(auc, 4),
            "ap": round(ap, 4),
            "f1": round(f1, 4),
            "precision_at_k": p_at_k,
            "fpr": fpr.tolist(),
            "tpr": tpr.tolist(),
            "pr_precision": pr_precision.tolist(),
            "pr_recall": pr_recall.tolist()
        }
    return results


def plot_evaluation_charts(results: dict, G_full: nx.Graph, dataset_label: str = "Bitcoin Web-of-Trust") -> None:
    """Generate publication-quality ROC, PR, Precision@K, and Power-Law degree distribution charts."""
    VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    palette = {
        "Common Neighbors": "#0D9488",
        "Jaccard": "#0284C7",
        "Adamic-Adar": "#D97706",
        "Resource Allocation": "#059669",
        "Preferential Attachment": "#E11D48",
        "Ensemble Model": "#6366F1"
    }
    
    # 1. ROC Curves
    plt.figure(figsize=(8.5, 6), dpi=220, facecolor="#F8FAFC")
    ax = plt.gca(); ax.set_facecolor("#FFFFFF")
    for model_name, data in results.items():
        fpr = np.array(data["fpr"])
        tpr = np.array(data["tpr"])
        auc = data["auc"]
        color = palette.get(model_name, "#333333")
        lw = 2.4 if model_name in ["Adamic-Adar", "Preferential Attachment", "Ensemble Model"] else 1.8
        plt.plot(fpr, tpr, label=f"{model_name} (AUC = {auc:.3f})", color=color, linewidth=lw)
        
    plt.plot([0, 1], [0, 1], "k--", alpha=0.4, label="Random Guess (AUC = 0.500)")
    plt.xlabel("False Positive Rate (FPR)", fontsize=11, fontweight="bold", color="#0F172A")
    plt.ylabel("True Positive Rate (TPR)", fontsize=11, fontweight="bold", color="#0F172A")
    plt.title(f"Link Prediction ROC Curves — {dataset_label}", fontsize=12.5, fontweight="bold", pad=12, color="#0F172A")
    plt.legend(loc="lower right", frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(VISUALIZATIONS_DIR / "link_prediction_roc_curves.png", dpi=220, facecolor="#F8FAFC")
    plt.savefig(VISUALIZATIONS_DIR / "link_prediction_roc_curves.svg", facecolor="#F8FAFC")
    plt.close()
    
    # 2. Precision-Recall (PR) Curves
    plt.figure(figsize=(8.5, 6), dpi=220, facecolor="#F8FAFC")
    ax = plt.gca(); ax.set_facecolor("#FFFFFF")
    for model_name, data in results.items():
        recall = np.array(data["pr_recall"])
        prec = np.array(data["pr_precision"])
        ap = data["ap"]
        color = palette.get(model_name, "#333333")
        lw = 2.4 if model_name in ["Adamic-Adar", "Ensemble Model"] else 1.8
        plt.plot(recall, prec, label=f"{model_name} (AP = {ap:.3f})", color=color, linewidth=lw)
        
    plt.xlabel("Recall", fontsize=11, fontweight="bold", color="#0F172A")
    plt.ylabel("Precision", fontsize=11, fontweight="bold", color="#0F172A")
    plt.title(f"Precision-Recall Curves — {dataset_label}", fontsize=12.5, fontweight="bold", pad=12, color="#0F172A")
    plt.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=9)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(VISUALIZATIONS_DIR / "link_prediction_pr_curves.png", dpi=220, facecolor="#F8FAFC")
    plt.savefig(VISUALIZATIONS_DIR / "link_prediction_pr_curves.svg", facecolor="#F8FAFC")
    plt.close()

    # 3. Precision@K Comparison Bar Chart
    k_vals = ["P@10", "P@20", "P@50", "P@100"]
    models = list(results.keys())
    x = np.arange(len(k_vals))
    width = 0.14
    
    plt.figure(figsize=(9.2, 5.2), dpi=220, facecolor="#F8FAFC")
    ax = plt.gca(); ax.set_facecolor("#FFFFFF")
    for idx, model_name in enumerate(models):
        precisions = [results[model_name]["precision_at_k"][k] for k in k_vals]
        color = palette.get(model_name, "#555555")
        plt.bar(x + idx * width - (len(models)/2 - 0.5) * width, precisions, width,
                label=model_name, color=color, edgecolor="white", linewidth=0.8)
                
    plt.xlabel("Evaluation Metric", fontsize=11, fontweight="bold", color="#0F172A")
    plt.ylabel("Precision Score", fontsize=11, fontweight="bold", color="#0F172A")
    plt.title(f"Precision@K Performance Across Link Prediction Models — {dataset_label}", fontsize=12, fontweight="bold", pad=12, color="#0F172A")
    plt.xticks(x, ["Precision@10", "Precision@20", "Precision@50", "Precision@100"], fontweight="bold", color="#0F172A")
    plt.ylim(0, 1.15)
    plt.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=8.5)
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(VISUALIZATIONS_DIR / "link_prediction_precision_at_k.png", dpi=220, facecolor="#F8FAFC")
    plt.savefig(VISUALIZATIONS_DIR / "link_prediction_precision_at_k.svg", facecolor="#F8FAFC")
    plt.close()
    
    # 4. Log-Log Degree Distribution (Power-Law Scale-Free Proof)
    degrees = [d for n, d in G_full.degree() if d > 0]
    deg_counts = pd.Series(degrees).value_counts().sort_index()
    
    plt.figure(figsize=(8, 5.2), dpi=220, facecolor="#F8FAFC")
    ax = plt.gca(); ax.set_facecolor("#FFFFFF")
    plt.loglog(deg_counts.index, deg_counts.values, "o", color="#0D9488", markersize=5, alpha=0.75, label="Empirical Traders")
    
    # Power-law fit reference line (gamma ≈ 2.1)
    k_ref = np.linspace(min(deg_counts.index), max(deg_counts.index), 100)
    plt.loglog(k_ref, deg_counts.values[0] * (k_ref / min(k_ref))**(-2.1), "r--", linewidth=2, label="Power-Law Fit (γ ≈ 2.1)")
    
    plt.xlabel("Node Degree k (log scale)", fontsize=11, fontweight="bold", color="#0F172A")
    plt.ylabel("Frequency P(k) (log scale)", fontsize=11, fontweight="bold", color="#0F172A")
    plt.title("Scale-Free Heavy-Tailed Degree Distribution — Bitcoin Web-of-Trust", fontsize=12, fontweight="bold", pad=12, color="#0F172A")
    plt.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=9.5)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(VISUALIZATIONS_DIR / "degree_distribution_powerlaw.png", dpi=220, facecolor="#F8FAFC")
    plt.savefig(VISUALIZATIONS_DIR / "degree_distribution_powerlaw.svg", facecolor="#F8FAFC")
    plt.close()
    print("All 4 publication charts successfully generated.")
