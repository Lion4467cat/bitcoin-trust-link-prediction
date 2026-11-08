"""Chronological Temporal Link Prediction Backtest for Bitcoin Web-of-Trust (2010-2016)."""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from src.config import DATA_DIR, OUTPUTS_DIR, VISUALIZATIONS_DIR
from src.evaluate import evaluate_models_on_split


def run_temporal_backtest(cutoff_ratio: float = 0.80, seed: int = 42) -> dict:
    """Evaluate link prediction forward through time: train on historical past, predict future arrivals."""
    random.seed(seed)
    np.random.seed(seed)
    
    alpha_path = DATA_DIR / "soc-sign-bitcoinalpha.csv.gz"
    otc_path = DATA_DIR / "soc-sign-bitcoinotc.csv.gz"
    
    alpha = pd.read_csv(alpha_path, header=None, names=["source", "target", "rating", "time"])
    otc = pd.read_csv(otc_path, header=None, names=["source", "target", "rating", "time"])
    all_df = pd.concat([alpha, otc], ignore_index=True)
    
    # Exclude self-loops
    all_df = all_df[all_df["source"] != all_df["target"]]
    all_df["u"] = all_df[["source", "target"]].min(axis=1)
    all_df["v"] = all_df[["source", "target"]].max(axis=1)
    
    # Group by pair: mean rating and first time link was formed
    pair_grouped = all_df.groupby(["u", "v"]).agg(
        weight=("rating", "mean"),
        first_seen=("time", "min")
    ).reset_index()
    
    # Filter positive reciprocal trust ties
    pair_positive = pair_grouped[pair_grouped["weight"] > 0].sort_values("first_seen").reset_index(drop=True)
    
    # Split chronologically
    cutoff_idx = int(cutoff_ratio * len(pair_positive))
    train_df = pair_positive.iloc[:cutoff_idx]
    test_pos_df = pair_positive.iloc[cutoff_idx:]
    
    # Build temporal training graph
    G_train = nx.Graph()
    for _, r in train_df.iterrows():
        G_train.add_edge(int(r["u"]), int(r["v"]), weight=float(r["weight"]))
        
    train_nodes = set(G_train.nodes())
    
    # Filter test edges where both participants existed in training period
    test_pos_edges = [
        (int(r["u"]), int(r["v"]))
        for _, r in test_pos_df.iterrows()
        if r["u"] in train_nodes and r["v"] in train_nodes
    ]
    
    # Sample balanced true negative edges (never interacted in entire dataset)
    existing_all = set(zip(pair_grouped["u"], pair_grouped["v"]))
    nodes_list = list(train_nodes)
    
    neg_edges = set()
    while len(neg_edges) < len(test_pos_edges):
        u = random.choice(nodes_list)
        v = random.choice(nodes_list)
        if u != v:
            pair = (min(u, v), max(u, v))
            if pair not in existing_all and pair not in neg_edges:
                neg_edges.add(pair)
                
    test_neg_edges = list(neg_edges)
    
    print(f"Temporal Split: Train Edges = {G_train.number_of_edges():,}, Test Pos = {len(test_pos_edges):,}, Test Neg = {len(test_neg_edges):,}")
    
    temporal_metrics = evaluate_models_on_split(G_train, test_pos_edges, test_neg_edges)
    
    # Save metrics
    out_json = OUTPUTS_DIR / "temporal_link_prediction_metrics.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(temporal_metrics, f, indent=2)
    print(f"Temporal backtest metrics saved to {out_json}")
    
    # Plot Comparison Chart: Topological Split vs Temporal Backtest
    plot_temporal_comparison(temporal_metrics)
    
    return temporal_metrics


def plot_temporal_comparison(temporal_metrics: dict) -> None:
    """Plot comparative bar chart contrasting Topological 80/20 Split vs Chronological Backtest."""
    topological_json = OUTPUTS_DIR / "link_prediction_metrics.json"
    if not topological_json.exists():
        return
        
    with open(topological_json, encoding="utf-8") as f:
        topo_data = json.load(f)["empirical_network"]["models"]
        
    models = ["Preferential Attachment", "Ensemble Model", "Adamic-Adar", "Resource Allocation", "Common Neighbors"]
    topo_aucs = [topo_data[m]["auc"] for m in models]
    temporal_aucs = [temporal_metrics[m]["auc"] for m in models]
    
    x = np.arange(len(models))
    width = 0.35
    
    plt.figure(figsize=(9.2, 5.2), dpi=220, facecolor="#F8FAFC")
    ax = plt.gca()
    ax.set_facecolor("#FFFFFF")
    
    rects1 = plt.bar(x - width/2, topo_aucs, width, label="Topological 80/20 Split (MST Protected)", color="#0D9488", edgecolor="white")
    rects2 = plt.bar(x + width/2, temporal_aucs, width, label="Chronological Temporal Backtest (2010-2013 → 2014-2016)", color="#6366F1", edgecolor="white")
    
    plt.ylabel("ROC-AUC Score", fontsize=11, fontweight="bold", color="#0F172A")
    plt.title("Dual Validation: Topological vs. Chronological Temporal Link Prediction", fontsize=12, fontweight="bold", pad=12, color="#0F172A")
    plt.xticks(x, [m.replace("Preferential Attachment", "PA").replace("Resource Allocation", "RA").replace("Common Neighbors", "CN").replace("Adamic-Adar", "AA") for m in models], fontweight="bold", color="#0F172A")
    plt.ylim(0.5, 1.05)
    plt.axhline(0.5, color="red", linestyle="--", alpha=0.5, label="Random Guess (0.500)")
    plt.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=9)
    plt.grid(axis="y", linestyle="--", alpha=0.3)
    plt.tight_layout()
    
    out_png = VISUALIZATIONS_DIR / "temporal_link_prediction_comparison.png"
    plt.savefig(out_png, dpi=220, facecolor="#F8FAFC")
    plt.savefig(VISUALIZATIONS_DIR / "temporal_link_prediction_comparison.svg", facecolor="#F8FAFC")
    plt.close()
    print(f"Temporal comparison chart saved to {out_png}")


if __name__ == "__main__":
    run_temporal_backtest()
