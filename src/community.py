"""Community Detection & Modular Structure Analysis for Bitcoin Web-of-Trust."""
from __future__ import annotations

import networkx as nx
from typing import Dict, Tuple, List, Set


def detect_trading_communities(G: nx.Graph, seed: int = 42) -> Tuple[Dict[int, int], float, List[Set[int]]]:
    """Detect modular trading circles using the Louvain algorithm.
    
    Returns:
        node_to_community: Dict mapping trader ID to community ID.
        modularity: Newman-Girvan modularity score Q.
        communities: List of sets of node IDs for each community.
    """
    communities = list(nx.community.louvain_communities(G, seed=seed))
    # Sort communities by size descending
    communities.sort(key=len, reverse=True)
    
    node_to_community = {}
    for comm_id, comm_nodes in enumerate(communities):
        for node in comm_nodes:
            node_to_community[node] = comm_id
            
    modularity = float(nx.community.modularity(G, communities))
    return node_to_community, modularity, communities


def classify_link_community_role(u: int, v: int, node_to_comm: Dict[int, int]) -> str:
    """Classify whether a link between u and v is intra-community or an inter-community bridge."""
    c_u = node_to_comm.get(u, -1)
    c_v = node_to_comm.get(v, -2)
    if c_u == c_v and c_u != -1:
        return f"Intra-Cluster (Circle #{c_u})"
    else:
        return f"Inter-Cluster Bridge (#{c_u} ↔ #{c_v})"
