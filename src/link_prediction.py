"""SNA Link Prediction algorithms: CN, Jaccard, Adamic-Adar, Resource Allocation, and PA."""
from __future__ import annotations

import math
import networkx as nx
import numpy as np


def compute_common_neighbors(G: nx.Graph, pairs: list[tuple[int, int]]) -> np.ndarray:
    """Compute Common Neighbors (CN) score for each node pair (u, v).
    
    CN(u, v) = |Gamma(u) cap Gamma(v)|
    """
    scores = np.zeros(len(pairs), dtype=float)
    adj = {n: set(G.neighbors(n)) for n in G.nodes()}
    
    for i, (u, v) in enumerate(pairs):
        nu = adj.get(u, set())
        nv = adj.get(v, set())
        scores[i] = len(nu.intersection(nv))
    return scores


def compute_jaccard_coefficient(G: nx.Graph, pairs: list[tuple[int, int]]) -> np.ndarray:
    """Compute Jaccard Coefficient score for each node pair (u, v).
    
    Jaccard(u, v) = |Gamma(u) cap Gamma(v)| / |Gamma(u) cup Gamma(v)|
    """
    scores = np.zeros(len(pairs), dtype=float)
    adj = {n: set(G.neighbors(n)) for n in G.nodes()}
    
    for i, (u, v) in enumerate(pairs):
        nu = adj.get(u, set())
        nv = adj.get(v, set())
        union_size = len(nu.union(nv))
        if union_size > 0:
            scores[i] = len(nu.intersection(nv)) / union_size
        else:
            scores[i] = 0.0
    return scores


def compute_adamic_adar(G: nx.Graph, pairs: list[tuple[int, int]]) -> np.ndarray:
    """Compute Adamic-Adar (AA) score for each node pair (u, v).
    
    AA(u, v) = sum_{z in Gamma(u) cap Gamma(v)} (1 / log(|Gamma(z)|))
    """
    scores = np.zeros(len(pairs), dtype=float)
    adj = {n: set(G.neighbors(n)) for n in G.nodes()}
    deg = dict(G.degree())
    
    inv_log_deg = {n: (1.0 / math.log(d) if d > 1 else 0.0) for n, d in deg.items()}
            
    for i, (u, v) in enumerate(pairs):
        nu = adj.get(u, set())
        nv = adj.get(v, set())
        common = nu.intersection(nv)
        scores[i] = sum(inv_log_deg.get(z, 0.0) for z in common)
    return scores


def compute_resource_allocation(G: nx.Graph, pairs: list[tuple[int, int]]) -> np.ndarray:
    """Compute Resource Allocation (RA) index score for each node pair (u, v).
    
    RA(u, v) = sum_{z in Gamma(u) cap Gamma(v)} (1 / |Gamma(z)|)
    Ref: Zhou, Lu, Cui (2009).
    """
    scores = np.zeros(len(pairs), dtype=float)
    adj = {n: set(G.neighbors(n)) for n in G.nodes()}
    deg = dict(G.degree())
    
    inv_deg = {n: (1.0 / float(d) if d > 0 else 0.0) for n, d in deg.items()}
    
    for i, (u, v) in enumerate(pairs):
        nu = adj.get(u, set())
        nv = adj.get(v, set())
        common = nu.intersection(nv)
        scores[i] = sum(inv_deg.get(z, 0.0) for z in common)
    return scores


def compute_preferential_attachment(G: nx.Graph, pairs: list[tuple[int, int]]) -> np.ndarray:
    """Compute Preferential Attachment (PA) score for each node pair (u, v).
    
    PA(u, v) = |Gamma(u)| * |Gamma(v)|
    """
    scores = np.zeros(len(pairs), dtype=float)
    deg = dict(G.degree())
    for i, (u, v) in enumerate(pairs):
        scores[i] = float(deg.get(u, 0) * deg.get(v, 0))
    return scores


def compute_all_scores(G: nx.Graph, pairs: list[tuple[int, int]]) -> dict[str, np.ndarray]:
    """Compute all 5 classic link prediction scores plus normalized ensemble score."""
    cn = compute_common_neighbors(G, pairs)
    jac = compute_jaccard_coefficient(G, pairs)
    aa = compute_adamic_adar(G, pairs)
    ra = compute_resource_allocation(G, pairs)
    pa = compute_preferential_attachment(G, pairs)
    
    def normalize(arr: np.ndarray) -> np.ndarray:
        denom = arr.max() - arr.min()
        return (arr - arr.min()) / denom if denom > 0 else np.zeros_like(arr)
        
    ensemble = (
        0.30 * normalize(aa) +
        0.25 * normalize(ra) +
        0.25 * normalize(jac) +
        0.10 * normalize(cn) +
        0.10 * normalize(pa)
    )
    
    return {
        "Common Neighbors": cn,
        "Jaccard": jac,
        "Adamic-Adar": aa,
        "Resource Allocation": ra,
        "Preferential Attachment": pa,
        "Ensemble Model": ensemble
    }
