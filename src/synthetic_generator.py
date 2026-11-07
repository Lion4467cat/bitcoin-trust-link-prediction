"""Enterprise-scale synthetic trust network generator matching empirical Bitcoin topology."""
from __future__ import annotations

import networkx as nx
import numpy as np
import pandas as pd
from src.config import SYNTHETIC_NODES, SYNTHETIC_EDGES, RANDOM_SEED, SYNTHETIC_CSV


def generate_enterprise_trust_network(
    n_nodes: int = SYNTHETIC_NODES,
    target_edges: int = SYNTHETIC_EDGES,
    seed: int = RANDOM_SEED
) -> tuple[pd.DataFrame, nx.Graph]:
    """Generate an enterprise-scale synthetic trust network.
    
    Uses Holme-Kim power-law clustering model:
    - Scale-free preferential attachment (hubs / market makers)
    - High triadic closure matching empirical Bitcoin Alpha clustering (p ≈ 0.18)
    - Empirical signed trust rating distribution (90.7% positive, 9.3% negative)
    """
    rng = np.random.default_rng(seed)
    
    # Calculate average edges added per step: target_edges ≈ n_nodes * m
    m = max(2, int(round(target_edges / n_nodes)))
    p_triangle = 0.18  # Matches Bitcoin Alpha empirical clustering coefficient (0.175)
    
    print(f"Generating synthetic enterprise graph (N={n_nodes:,}, m={m}, p_tri={p_triangle})...")
    base_graph = nx.powerlaw_cluster_graph(n_nodes, m, p_triangle, seed=seed)
    
    # Generate realistic trust ratings (-10 to +10, 90.7% positive)
    edges = list(base_graph.edges())
    records = []
    
    # Sample ratings from empirical Bitcoin distribution
    # Positive ratings mostly +1, +2, +3, +5, +10
    pos_ratings = [1, 2, 3, 5, 8, 10]
    pos_probs = [0.45, 0.20, 0.15, 0.10, 0.05, 0.05]
    neg_ratings = [-1, -2, -3, -5, -8, -10]
    neg_probs = [0.15, 0.10, 0.10, 0.15, 0.15, 0.35] # Many negative ratings are -10 (scammer/fraud)
    
    for u, v in edges:
        is_positive = (rng.random() < 0.907)
        if is_positive:
            rating = int(rng.choice(pos_ratings, p=pos_probs))
            sign = 1
        else:
            rating = int(rng.choice(neg_ratings, p=neg_probs))
            sign = -1
        
        rating_count = int(rng.geometric(p=0.8)) # Most pairs have 1-2 ratings
        records.append({
            "u": min(u, v),
            "v": max(u, v),
            "weight": float(rating),
            "sign": sign,
            "rating_count": rating_count
        })
    
    df = pd.DataFrame(records)
    
    # Build NetworkX graph
    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))
    for row in df.itertuples(index=False):
        if row.sign > 0: # Positive trust graph for link prediction
            G.add_edge(int(row.u), int(row.v), weight=row.weight, sign=row.sign, rating_count=row.rating_count)
            
    return df, G
