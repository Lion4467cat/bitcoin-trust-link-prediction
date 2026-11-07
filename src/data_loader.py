"""Data loading and graph construction for Bitcoin Web-of-Trust networks."""
from __future__ import annotations

import gzip
from pathlib import Path
import networkx as nx
import numpy as np
import pandas as pd

from src.config import ALPHA_PATH, OTC_PATH, COMBINED_CSV


def load_raw_csv(path: Path) -> pd.DataFrame:
    """Load and validate raw SNAP Bitcoin CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}")
    
    df = pd.read_csv(path, header=None, names=["source", "target", "rating", "time"])
    for col in ["source", "target", "rating", "time"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    df = df.dropna()
    df["source"] = df["source"].astype(int)
    df["target"] = df["target"].astype(int)
    df["rating"] = df["rating"].astype(int)
    df["time"] = df["time"].astype(int)
    
    # Remove self-loops
    df = df[df["source"] != df["target"]].copy()
    return df


def aggregate_undirected_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate directed ratings into undirected signed pairs."""
    df["u"] = np.minimum(df["source"], df["target"])
    df["v"] = np.maximum(df["source"], df["target"])
    
    grouped = df.groupby(["u", "v"], as_index=False).agg(
        weight=("rating", "mean"),
        rating_count=("rating", "count"),
        min_time=("time", "min"),
        max_time=("time", "max")
    )
    grouped["sign"] = np.sign(grouped["weight"]).astype(int)
    return grouped


def build_trust_network(pairs_df: pd.DataFrame, positive_only: bool = True) -> nx.Graph:
    """Build a NetworkX graph from aggregated pairs.
    
    If positive_only is True, links represent positive trust (suitable for positive link recommendation).
    """
    G = nx.Graph()
    if positive_only:
        filtered = pairs_df[pairs_df["sign"] > 0]
    else:
        filtered = pairs_df[pairs_df["sign"] != 0]
        
    for row in filtered.itertuples(index=False):
        G.add_edge(
            int(row.u), int(row.v),
            weight=float(row.weight),
            sign=int(row.sign),
            rating_count=int(row.rating_count)
        )
    return G


def load_dataset(dataset_name: str = "combined") -> tuple[pd.DataFrame, nx.Graph]:
    """Load specified dataset: 'alpha', 'otc', or 'combined'."""
    if dataset_name == "alpha":
        raw = load_raw_csv(ALPHA_PATH)
        pairs = aggregate_undirected_pairs(raw)
    elif dataset_name == "otc":
        raw = load_raw_csv(OTC_PATH)
        pairs = aggregate_undirected_pairs(raw)
    elif dataset_name == "combined":
        raw_alpha = load_raw_csv(ALPHA_PATH)
        raw_alpha["platform"] = "alpha"
        raw_otc = load_raw_csv(OTC_PATH)
        raw_otc["platform"] = "otc"
        # Offset OTC user IDs by 100,000 to keep disjoint namespaces while allowing unified analysis
        raw_otc["source"] += 100000
        raw_otc["target"] += 100000
        raw = pd.concat([raw_alpha, raw_otc], ignore_index=True)
        pairs = aggregate_undirected_pairs(raw)
    else:
        raise ValueError(f"Unknown dataset name: {dataset_name}")
        
    G = build_trust_network(pairs, positive_only=True)
    return pairs, G
