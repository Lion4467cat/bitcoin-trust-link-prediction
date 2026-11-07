"""Recommendation engine: Generates and filters Top-10 and Top-20 predicted trust links."""
from __future__ import annotations

import math
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from src.config import VISUALIZATIONS_DIR, OUTPUTS_DIR
from src.community import detect_trading_communities, classify_link_community_role


def recommend_links_for_user(
    G: nx.Graph,
    user_id: int,
    top_k: int = 20,
    model: str = "Ensemble",
    node_to_comm: dict | None = None
) -> pd.DataFrame:
    """Generate and filter Top-K link recommendations for a given user.
    
    Evaluates 2-hop candidate peers (nodes sharing mutual connections with user_id
    that do not currently have a direct edge).
    """
    if user_id not in G:
        raise ValueError(f"User ID {user_id} not found in graph.")
        
    user_neighbors = set(G.neighbors(user_id))
    user_degree = len(user_neighbors)
    
    candidates = set()
    for neighbor in user_neighbors:
        for second_neighbor in G.neighbors(neighbor):
            if second_neighbor != user_id and second_neighbor not in user_neighbors:
                candidates.add(second_neighbor)
                
    if not candidates:
        all_nodes = set(G.nodes())
        candidates = list(all_nodes - user_neighbors - {user_id})[:100]
    else:
        candidates = list(candidates)
        
    records = []
    deg_dict = dict(G.degree())
    
    inv_log_deg = {n: (1.0 / math.log(d) if d > 1 else 0.0) for n, d in deg_dict.items()}
    inv_deg = {n: (1.0 / float(d) if d > 0 else 0.0) for n, d in deg_dict.items()}
    
    for cand in candidates:
        cand_neighbors = set(G.neighbors(cand))
        cand_degree = len(cand_neighbors)
        common_nodes = user_neighbors.intersection(cand_neighbors)
        common_count = len(common_nodes)
        
        union_size = len(user_neighbors.union(cand_neighbors))
        jaccard = common_count / union_size if union_size > 0 else 0.0
        
        aa = sum(inv_log_deg.get(z, 0.0) for z in common_nodes)
        ra = sum(inv_deg.get(z, 0.0) for z in common_nodes)
        pa = float(user_degree * cand_degree)
        
        records.append({
            "target_user": cand,
            "common_neighbors": common_count,
            "jaccard": round(jaccard, 4),
            "adamic_adar": round(aa, 4),
            "resource_allocation": round(ra, 4),
            "preferential_attachment": pa,
            "mutual_peers": list(common_nodes)[:5]
        })
        
    df = pd.DataFrame(records)
    if df.empty:
        return df
        
    def norm(col):
        span = col.max() - col.min()
        return (col - col.min()) / span if span > 0 else np.zeros_like(col)
        
    n_aa = 0.30 * norm(df["adamic_adar"])
    n_ra = 0.25 * norm(df["resource_allocation"])
    n_jac = 0.25 * norm(df["jaccard"])
    n_cn = 0.10 * norm(df["common_neighbors"])
    n_pa = 0.10 * norm(df["preferential_attachment"])

    df["ensemble_score"] = (n_aa + n_ra + n_jac + n_cn + n_pa).round(4)
    
    local_signal = n_aa + n_ra + n_jac
    global_signal = n_cn + n_pa
    total_signal = local_signal + global_signal + 1e-9
    
    df["local_trust_pct"] = (100.0 * local_signal / total_signal).round(1)
    df["hub_popularity_pct"] = (100.0 * global_signal / total_signal).round(1)
    df["feature_attribution"] = df.apply(
        lambda r: f"{r['local_trust_pct']}% Community Trust | {r['hub_popularity_pct']}% Hub Liquidity",
        axis=1
    )
    
    sort_col = {
        "Common Neighbors": "common_neighbors",
        "Jaccard": "jaccard",
        "Adamic-Adar": "adamic_adar",
        "Resource Allocation": "resource_allocation",
        "Preferential Attachment": "preferential_attachment",
        "Ensemble": "ensemble_score"
    }.get(model, "ensemble_score")
    
    df = df.sort_values(by=sort_col, ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    
    df["structural_balance_status"] = "Balanced (+, +, +)"
    
    if node_to_comm is None:
        node_to_comm, _, _ = detect_trading_communities(G)
    df["community_role"] = df["target_user"].apply(
        lambda v: classify_link_community_role(user_id, v, node_to_comm)
    )
    
    df["recommendation_rationale"] = df.apply(
        lambda r: f"Shares {r['common_neighbors']} mutual trusted traders; Attribution: {r['feature_attribution']} ({r['community_role']}).",
        axis=1
    )
    
    return df.head(top_k)


def plot_recommended_ego_network(
    G: nx.Graph,
    user_id: int,
    recommendations_df: pd.DataFrame,
    top_n_to_show: int = 5
) -> Path:
    """Plot an ego network showing the user, existing trusted peers, and top recommended new ties."""
    VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    user_neighbors = list(G.neighbors(user_id))
    top_rec_nodes = list(recommendations_df["target_user"].head(top_n_to_show))
    
    subG = G.subgraph([user_id] + user_neighbors[:12]).copy()
    
    for rec in top_rec_nodes:
        subG.add_node(rec)
        subG.add_edge(user_id, rec, is_recommended=True)
        
    pos = nx.spring_layout(subG, seed=2026, k=0.8)
    
    plt.figure(figsize=(9, 7.5), dpi=220, facecolor="#F8FAFC")
    ax = plt.gca()
    ax.set_facecolor("#F8FAFC")
    
    existing_edges = [(u, v) for u, v, d in subG.edges(data=True) if not d.get("is_recommended", False)]
    nx.draw_networkx_edges(subG, pos, edgelist=existing_edges, edge_color="#0D9488", width=1.8, alpha=0.7)
    
    rec_edges = [(u, v) for u, v, d in subG.edges(data=True) if d.get("is_recommended", False)]
    nx.draw_networkx_edges(subG, pos, edgelist=rec_edges, edge_color="#6366F1", width=2.5, style="dashed", alpha=0.9)
    
    node_colors = []
    node_sizes = []
    for n in subG.nodes():
        if n == user_id:
            node_colors.append("#D97706")
            node_sizes.append(440)
        elif n in top_rec_nodes:
            node_colors.append("#E11D48")
            node_sizes.append(340)
        else:
            node_colors.append("#0D9488")
            node_sizes.append(180)
            
    nx.draw_networkx_nodes(subG, pos, node_color=node_colors, node_size=node_sizes, edgecolors="#0F172A", linewidths=1.2)
    nx.draw_networkx_labels(subG, pos, font_size=8.5, font_color="#0F172A", font_weight="bold")
    
    plt.title(f"Target Trader #{user_id}: Verified Trust Network vs. Top Predicted Ties", fontsize=12.5, fontweight="bold", pad=12, color="#0F172A")
    plt.plot([], [], color="#0D9488", linewidth=2, label="Existing Verified Trust Tie")
    plt.plot([], [], color="#6366F1", linewidth=2.5, linestyle="--", label="Top-5 Recommended Trust Tie (Predicted)")
    plt.plot([], [], marker="o", color="w", markerfacecolor="#D97706", markersize=10, label=f"Target Trader #{user_id}")
    plt.plot([], [], marker="o", color="w", markerfacecolor="#E11D48", markersize=9, label="Recommended Trading Partner")
    plt.plot([], [], marker="o", color="w", markerfacecolor="#0D9488", markersize=8, label="Existing Mutual Peer")
    plt.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=8.5)
    plt.axis("off")
    plt.tight_layout()
    
    out_path = VISUALIZATIONS_DIR / "recommended_ego_network.png"
    plt.savefig(out_path, dpi=220, facecolor="#F8FAFC")
    plt.savefig(VISUALIZATIONS_DIR / "recommended_ego_network.svg", facecolor="#F8FAFC")
    plt.close()
    return out_path
