"""Master End-to-End Pipeline for Enterprise-Scale Bitcoin Link Prediction & Recommendation."""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import networkx as nx
import numpy as np
import pandas as pd

from src.config import (
    ROOT, OUTPUTS_DIR, VISUALIZATIONS_DIR, METRICS_JSON,
    SYNTHETIC_CSV, TOP20_RECOMMENDATIONS_CSV, GRAPHML_PATH
)
from src.data_loader import load_dataset
from src.synthetic_generator import generate_enterprise_trust_network
from src.evaluate import create_train_test_split, evaluate_models_on_split, plot_evaluation_charts
from src.recommend import recommend_links_for_user, plot_recommended_ego_network


def run_full_pipeline():
    print("=" * 70)
    print("STARTING ENTERPRISE BITCOIN LINK PREDICTION & RECOMMENDATION PIPELINE")
    print("=" * 70)
    
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Empirical Bitcoin Alpha + OTC Combined Network
    print("\n[Step 1/6] Loading Empirical Bitcoin Trust Network (Alpha + OTC)...")
    pairs_df, G_empirical = load_dataset("combined")
    print(f"Empirical Graph: Nodes={G_empirical.number_of_nodes():,}, Edges={G_empirical.number_of_edges():,}")
    
    # 2. Generate Enterprise-Scale Synthetic Benchmark
    print("\n[Step 2/6] Generating Enterprise-Scale Synthetic Benchmark (25k nodes, 150k edges)...")
    synthetic_df, G_synthetic = generate_enterprise_trust_network(n_nodes=25000, target_edges=150000)
    synthetic_df.to_csv(SYNTHETIC_CSV, index=False)
    print(f"Synthetic Graph: Nodes={G_synthetic.number_of_nodes():,}, Edges={G_synthetic.number_of_edges():,}")
    print(f"Saved synthetic enterprise dataset to {SYNTHETIC_CSV}")
    
    # 3. 80/20 Train-Test Split & Evaluation on Empirical Network
    print("\n[Step 3/6] Running 80/20 Train-Test Split on Empirical Bitcoin Network...")
    G_train_emp, test_pos_emp, test_neg_emp = create_train_test_split(G_empirical)
    empirical_metrics = evaluate_models_on_split(G_train_emp, test_pos_emp, test_neg_emp)
    
    # 4. 80/20 Train-Test Split & Evaluation on Enterprise Synthetic Network
    print("\n[Step 4/6] Running 80/20 Train-Test Split on Enterprise Synthetic Network...")
    # For speed on the 25k synthetic graph, take a representative 10k edge sample for test
    G_train_syn, test_pos_syn, test_neg_syn = create_train_test_split(G_synthetic, test_ratio=0.10)
    synthetic_metrics = evaluate_models_on_split(G_train_syn, test_pos_syn, test_neg_syn)
    
    # 5. Generate Visualizations & Compile Metrics JSON
    print("\n[Step 5/6] Generating Publication-Quality Evaluation Charts...")
    plot_evaluation_charts(empirical_metrics, G_empirical, dataset_label="Empirical Bitcoin Web-of-Trust (Alpha + OTC)")
    
    all_metrics = {
        "empirical_network": {
            "name": "Bitcoin Web-of-Trust (Alpha + OTC Combined)",
            "nodes": G_empirical.number_of_nodes(),
            "edges": G_empirical.number_of_edges(),
            "train_edges": G_train_emp.number_of_edges(),
            "test_positive_edges": len(test_pos_emp),
            "test_negative_edges": len(test_neg_emp),
            "models": empirical_metrics
        },
        "enterprise_synthetic_network": {
            "name": "Enterprise-Scale Synthetic Trust Network (25,000 Nodes)",
            "nodes": G_synthetic.number_of_nodes(),
            "edges": G_synthetic.number_of_edges(),
            "train_edges": G_train_syn.number_of_edges(),
            "test_positive_edges": len(test_pos_syn),
            "test_negative_edges": len(test_neg_syn),
            "models": synthetic_metrics
        }
    }
    
    with open(METRICS_JSON, "w") as f:
        json.dump(all_metrics, f, indent=2)
    print(f"Metrics saved to {METRICS_JSON}")
    
    # 6. Recommendation Case Study & Cytoscape Export
    print("\n[Step 6/6] Generating Top-20 Link Recommendations for Case Study...")
    # Select user 1 (the foundational high-activity node in Bitcoin Alpha)
    target_user = 1
    top20_df = recommend_links_for_user(G_empirical, user_id=target_user, top_k=20, model="Ensemble")
    top20_df.to_csv(TOP20_RECOMMENDATIONS_CSV, index=False)
    print(f"Top-20 Recommendations for User {target_user} saved to {TOP20_RECOMMENDATIONS_CSV}")
    
    plot_recommended_ego_network(G_empirical, user_id=target_user, recommendations_df=top20_df, top_n_to_show=5)
    
    # Cytoscape GraphML Export
    print("Exporting GraphML for Cytoscape...")
    # Add attributes to graph for Cytoscape
    G_export = G_empirical.copy()
    for u, v in G_export.edges():
        G_export[u][v]["interaction_type"] = "positive_trust"
        
    nx.write_graphml(G_export, GRAPHML_PATH)
    print(f"Cytoscape GraphML saved to {GRAPHML_PATH}")
    
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_full_pipeline()
