"""Unit and Integration Tests for the Bitcoin SNA Link Prediction & Recommendation Pipeline."""
from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import networkx as nx
import numpy as np

from src.data_loader import load_dataset
from src.link_prediction import (
    compute_common_neighbors,
    compute_jaccard_coefficient,
    compute_adamic_adar,
    compute_resource_allocation,
    compute_preferential_attachment,
    compute_all_scores,
)
from src.evaluate import create_train_test_split, evaluate_models_on_split
from src.recommend import recommend_links_for_user
from src.community import detect_trading_communities, classify_link_community_role


class TestLinkPredictionFormulas(unittest.TestCase):
    """Verify analytical correctness of SNA topological link prediction algorithms on toy graphs."""

    def setUp(self):
        # Create a kite graph:
        # Nodes 0, 1 share common neighbors 2 and 3.
        # Node 2 connects to 0, 1, 4. (deg=3)
        # Node 3 connects to 0, 1. (deg=2)
        # Node 0 has neighbors {2, 3}. (deg=2)
        # Node 1 has neighbors {2, 3, 5}. (deg=3)
        self.G = nx.Graph()
        self.G.add_edges_from([
            (0, 2), (0, 3),
            (1, 2), (1, 3), (1, 5),
            (2, 4)
        ])
        self.pairs = [(0, 1)]

    def test_common_neighbors(self):
        # Mutual neighbors are {2, 3} -> count = 2
        cn = compute_common_neighbors(self.G, self.pairs)
        self.assertEqual(cn[0], 2)

    def test_jaccard_coefficient(self):
        # Neighbors of 0: {2, 3}; Neighbors of 1: {2, 3, 5}
        # Intersection = {2, 3} (size 2); Union = {2, 3, 5} (size 3)
        # Jaccard = 2/3 ≈ 0.666667
        jaccard = compute_jaccard_coefficient(self.G, self.pairs)
        self.assertAlmostEqual(jaccard[0], 2.0 / 3.0, places=5)

    def test_adamic_adar_index(self):
        # Deg(2) = 3 (edges: 0, 1, 4); Deg(3) = 2 (edges: 0, 1)
        # AA = 1/ln(3) + 1/ln(2) ≈ 0.91024 + 1.44270 ≈ 2.35293
        expected_aa = (1.0 / math.log(3)) + (1.0 / math.log(2))
        aa = compute_adamic_adar(self.G, self.pairs)
        self.assertAlmostEqual(aa[0], expected_aa, places=5)

    def test_resource_allocation_index(self):
        # RA = 1/deg(2) + 1/deg(3) = 1/3 + 1/2 = 5/6 ≈ 0.833333
        expected_ra = (1.0 / 3.0) + (1.0 / 2.0)
        ra = compute_resource_allocation(self.G, self.pairs)
        self.assertAlmostEqual(ra[0], expected_ra, places=5)

    def test_preferential_attachment(self):
        # Deg(0) = 2, Deg(1) = 3
        # PA = 2 * 3 = 6
        pa = compute_preferential_attachment(self.G, self.pairs)
        self.assertEqual(pa[0], 6.0)

    def test_all_scores_and_ensemble(self):
        scores = compute_all_scores(self.G, self.pairs)
        self.assertIn("Common Neighbors", scores)
        self.assertIn("Jaccard", scores)
        self.assertIn("Adamic-Adar", scores)
        self.assertIn("Resource Allocation", scores)
        self.assertIn("Preferential Attachment", scores)
        self.assertIn("Ensemble Model", scores)
        self.assertEqual(len(scores["Common Neighbors"]), 1)


class TestTrainTestSplitProtocol(unittest.TestCase):
    """Verify 80/20 train-test split, MST connectivity guarantee, and negative sampling."""

    def setUp(self):
        # Generate a small Barabasi-Albert scale-free graph
        self.G = nx.barabasi_albert_graph(n=200, m=3, seed=42)

    def test_minimum_spanning_tree_protection(self):
        # The training graph G_train MUST remain fully connected
        G_train, pos_test, neg_test = create_train_test_split(self.G, test_ratio=0.20, seed=42)
        self.assertTrue(nx.is_connected(G_train), "G_train fragmented into multiple components!")
        self.assertEqual(G_train.number_of_nodes(), self.G.number_of_nodes())

    def test_balanced_negative_sampling(self):
        G_train, pos_test, neg_test = create_train_test_split(self.G, test_ratio=0.20, seed=42)
        self.assertEqual(len(pos_test), len(neg_test), "Negative sampling is not 50/50 balanced!")
        
        # Ensure negative samples are true non-edges in the full graph G
        full_edges = set(map(lambda e: tuple(sorted(e)), self.G.edges()))
        for u, v in neg_test:
            pair = tuple(sorted((u, v)))
            self.assertNotIn(pair, full_edges, f"Negative sample ({u}, {v}) exists in ground truth!")
            self.assertNotEqual(u, v, "Self-loop found in negative sample!")


class TestCommunityDetection(unittest.TestCase):
    """Verify Louvain community detection and role categorization."""

    def setUp(self):
        # Two cliques connected by a single bridge
        self.G = nx.caveman_graph(2, 10)

    def test_louvain_modularity(self):
        node_to_comm, modularity, communities = detect_trading_communities(self.G, seed=42)
        self.assertEqual(len(communities), 2)
        self.assertGreater(modularity, 0.40)
        
        # Test link classification
        role_intra = classify_link_community_role(0, 1, node_to_comm)
        self.assertIn("Intra-Cluster", role_intra)


class TestRecommendationEngine(unittest.TestCase):
    """Verify Top-K recommendation sorting, structural balance, and output schema."""

    def setUp(self):
        self.G = nx.barabasi_albert_graph(n=100, m=4, seed=42)

    def test_recommend_links(self):
        user_id = 0
        recs = recommend_links_for_user(self.G, user_id=user_id, top_k=10, model="Ensemble")
        self.assertFalse(recs.empty)
        self.assertLessEqual(len(recs), 10)
        
        # Validate columns
        required_cols = [
            "rank", "target_user", "common_neighbors", "jaccard",
            "adamic_adar", "resource_allocation", "preferential_attachment",
            "ensemble_score", "structural_balance_status", "community_role",
            "feature_attribution", "local_trust_pct", "hub_popularity_pct"
        ]
        for col in required_cols:
            self.assertIn(col, recs.columns, f"Missing required column {col}")

        # Check ranking monotonicity
        ranks = list(recs["rank"])
        self.assertEqual(ranks, list(range(1, len(recs) + 1)))

        # Check balance status
        for status in recs["structural_balance_status"]:
            self.assertEqual(status, "Balanced (+, +, +)")

        # Check percentage attribution sum
        for _, row in recs.iterrows():
            total_pct = row["local_trust_pct"] + row["hub_popularity_pct"]
            self.assertAlmostEqual(total_pct, 100.0, places=0)


class TestKCoreAndConsensus(unittest.TestCase):
    """Verify K-Core shell decomposition and multi-algorithm consensus ranking."""

    def setUp(self):
        self.G = nx.barabasi_albert_graph(n=120, m=4, seed=42)

    def test_k_core_shell_decomposition(self):
        core_numbers = nx.core_number(self.G)
        self.assertEqual(len(core_numbers), self.G.number_of_nodes())
        max_core = max(core_numbers.values())
        self.assertGreaterEqual(max_core, 4)
        for node, k in core_numbers.items():
            self.assertGreaterEqual(self.G.degree(node), k, f"Node {node} has degree less than its core number {k}!")

    def test_consensus_ranking_structure(self):
        user_id = 0
        df = recommend_links_for_user(self.G, user_id=user_id, top_k=50, model="Ensemble")
        models = [
            ("ensemble_score", "Ensemble"),
            ("adamic_adar", "Adamic-Adar"),
            ("common_neighbors", "Common Neighbors"),
            ("jaccard", "Jaccard"),
            ("preferential_attachment", "Preferential Attachment"),
            ("resource_allocation", "Resource Allocation")
        ]
        candidate_votes = {}
        for col, m_name in models:
            top5 = df.sort_values(col, ascending=False).head(5)
            for rank, cand in enumerate(top5["target_user"], 1):
                if cand not in candidate_votes:
                    candidate_votes[cand] = {"votes": 0, "ranks": {}}
                candidate_votes[cand]["votes"] += 1
                candidate_votes[cand]["ranks"][m_name] = rank

        self.assertGreater(len(candidate_votes), 0)
        for cand, info in candidate_votes.items():
            self.assertGreaterEqual(info["votes"], 1)
            self.assertLessEqual(info["votes"], 6)


if __name__ == "__main__":
    unittest.main()
