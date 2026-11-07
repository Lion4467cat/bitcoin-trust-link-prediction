"""K-Core Decomposition and Centrality Rankings for Bitcoin Web-of-Trust.

Department of Machine Learning - Social Network Analysis (SNA)
Calculates k-core shell numbers, PageRank, betweenness centrality,
clustering coefficient, and identifies the core trading nucleus.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_loader import load_dataset
from src.community import detect_trading_communities

OUTPUTS_DIR = ROOT / "outputs"
VISUALIZATIONS_DIR = ROOT / "visualizations"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def analyze_k_core_and_centrality():
    print("Loading Bitcoin Trust Network...")
    pairs, G = load_dataset("combined")
    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()
    print(f"Graph loaded: {n_nodes:,} nodes, {n_edges:,} edges.")

    # 1. K-Core Decomposition
    print("Computing K-Core decomposition...")
    core_numbers = nx.core_number(G)
    max_k = max(core_numbers.values())
    print(f"Max coreness (k_max): {max_k}")

    # 2. Centrality metrics
    print("Computing PageRank...")
    pagerank = nx.pagerank(G, alpha=0.85, max_iter=100)

    print("Computing Betweenness Centrality (k=500 sampling)...")
    betweenness = nx.betweenness_centrality(G, k=500, seed=2026, normalized=True)

    print("Computing Clustering Coefficients...")
    clustering = nx.clustering(G)

    print("Detecting Communities...")
    node_to_comm, _, _ = detect_trading_communities(G)

    degrees = dict(G.degree())

    # Build DataFrame
    records = []
    for node in G.nodes():
        deg = degrees[node]
        core = core_numbers[node]
        pr = pagerank[node]
        bw = betweenness[node]
        cc = clustering[node]
        comm = node_to_comm.get(node, 0)

        # Role classification
        if core >= 15 and bw > 0.005:
            role = "Core Nucleus Broker"
        elif bw > 0.008:
            role = "Inter-Cluster Gateway"
        elif core >= 15:
            role = "Core Liquidity Provider"
        elif deg >= 20:
            role = "Local Cluster Hub"
        elif deg <= 3:
            role = "Peripheral Trader"
        else:
            role = "Active Member"

        records.append({
            "trader_id": node,
            "degree": deg,
            "core_number": core,
            "pagerank": round(pr, 6),
            "betweenness_centrality": round(bw, 6),
            "clustering_coefficient": round(cc, 4),
            "community_id": comm,
            "role": role,
        })

    df = pd.DataFrame(records)
    df = df.sort_values(by=["pagerank", "betweenness_centrality"], ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1

    out_csv = OUTPUTS_DIR / "trader_centrality_rankings.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved trader centrality rankings to {out_csv} ({len(df):,} rows)")

    # Generate 4-panel publication visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 11), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")

    # Panel A: K-Core Shell Distribution
    shell_counts = pd.Series(core_numbers).value_counts().sort_index()
    ax1 = axes[0, 0]
    bars = ax1.bar(shell_counts.index, shell_counts.values, color="#0D9488", edgecolor="#0F766E", alpha=0.85)
    # Highlight max core
    bars[-1].set_color("#E11D48")
    ax1.set_title("A. K-Core Shell Distribution (Nucleus vs Periphery)", fontsize=11.5, fontweight="bold", pad=8)
    ax1.set_xlabel("K-Core Shell Number (k)", fontsize=10, fontweight="bold")
    ax1.set_ylabel("Number of Traders (Log Scale)", fontsize=10, fontweight="bold")
    ax1.set_yscale("log")
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.annotate(f"Nucleus k={max_k}\n({shell_counts.iloc[-1]} Elite Brokers)",
                 xy=(max_k, shell_counts.iloc[-1]),
                 xytext=(max_k - 4, shell_counts.iloc[-1] * 3),
                 arrowprops=dict(arrowstyle="->", color="#E11D48", lw=1.5),
                 fontweight="bold", color="#E11D48", fontsize=9.5)

    # Panel B: Degree vs Core Number
    ax2 = axes[0, 1]
    scatter = ax2.scatter(df["core_number"], df["degree"], c=df["betweenness_centrality"],
                          cmap="viridis", alpha=0.6, s=28, edgecolors="none")
    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label("Betweenness Centrality", fontsize=9, fontweight="bold")
    ax2.set_title("B. Degree vs. K-Core Number (Hub-Core Stratification)", fontsize=11.5, fontweight="bold", pad=8)
    ax2.set_xlabel("Core Shell Number (k)", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Degree (Verified Ties)", fontsize=10, fontweight="bold")
    ax2.set_yscale("log")
    ax2.grid(True, linestyle="--", alpha=0.3)

    # Top broker callout
    top_broker = df.iloc[0]
    ax2.annotate(f"Trader #{top_broker['trader_id']}\n(Deg={top_broker['degree']}, k={top_broker['core_number']})",
                 xy=(top_broker['core_number'], top_broker['degree']),
                 xytext=(top_broker['core_number'] - 5, top_broker['degree'] * 0.5),
                 arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.5),
                 fontweight="bold", color="#0F172A", fontsize=9)

    # Panel C: PageRank vs. Betweenness Centrality
    ax3 = axes[1, 0]
    ax3.scatter(df["pagerank"], df["betweenness_centrality"], color="#6366F1", alpha=0.5, s=24)
    # Highlight top 5 brokers
    top5 = df.head(5)
    for _, row in top5.iterrows():
        ax3.scatter(row["pagerank"], row["betweenness_centrality"], color="#E11D48", s=65, edgecolors="#0F172A", zorder=5)
        ax3.text(row["pagerank"] * 1.04, row["betweenness_centrality"], f"#{int(row['trader_id'])}",
                 fontsize=8.5, fontweight="bold", color="#0F172A")
    ax3.set_title("C. PageRank vs. Betweenness Centrality (Broker Gatekeepers)", fontsize=11.5, fontweight="bold", pad=8)
    ax3.set_xlabel("PageRank Centrality", fontsize=10, fontweight="bold")
    ax3.set_ylabel("Betweenness Centrality", fontsize=10, fontweight="bold")
    ax3.grid(True, linestyle="--", alpha=0.3)

    # Panel D: Subgraph of the Core Nucleus (k=19)
    ax4 = axes[1, 1]
    nucleus_nodes = [n for n, c in core_numbers.items() if c == max_k]
    subG = G.subgraph(nucleus_nodes[:45])  # Draw top 45 for crystal clear layout
    pos = nx.spring_layout(subG, seed=2026, k=0.55)

    sub_degs = [subG.degree(n) for n in subG.nodes()]
    nx.draw_networkx_edges(subG, pos, ax=ax4, alpha=0.25, edge_color="#64748B", width=0.8)
    nx.draw_networkx_nodes(subG, pos, ax=ax4, node_color="#D97706",
                           node_size=[max(30, d * 8) for d in sub_degs],
                           edgecolors="#0F172A", linewidths=0.8)
    
    # Label top 8 highest degree nodes in subG
    top_in_sub = sorted(subG.nodes(), key=lambda n: subG.degree(n), reverse=True)[:8]
    sub_labels = {n: f"#{n}" for n in top_in_sub}
    nx.draw_networkx_labels(subG, pos, labels=sub_labels, ax=ax4, font_size=8,
                            font_color="#0F172A", font_weight="bold")

    ax4.set_title(f"D. Core Nucleus Subgraph (Top Elite Brokers, k={max_k})", fontsize=11.5, fontweight="bold", pad=8)
    ax4.axis("off")

    plt.suptitle("Bitcoin Web-of-Trust: K-Core Shell Decomposition & Centrality Topography\nDepartment of Machine Learning • SNA Research",
                 fontsize=13, fontweight="bold", y=0.98, color="#0F172A")
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    out_png = VISUALIZATIONS_DIR / "k_core_and_centrality_distribution.png"
    out_svg = VISUALIZATIONS_DIR / "k_core_and_centrality_distribution.svg"
    fig.savefig(out_png, dpi=220, facecolor="#FFFFFF")
    fig.savefig(out_svg, facecolor="#FFFFFF")
    plt.close(fig)
    print(f"Saved publication figures to {out_png} and {out_svg}")


if __name__ == "__main__":
    analyze_k_core_and_centrality()
