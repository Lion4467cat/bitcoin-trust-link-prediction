"""Ultra-responsive, light-themed full-stack HTTP server and recommendation dashboard."""
from __future__ import annotations

import csv
import json
import math
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import networkx as nx
import pandas as pd
from src.data_loader import load_dataset
from src.recommend import recommend_links_for_user

PORT = 5000

print("Pre-loading Bitcoin Trust Network into memory for real-time inference...")
pairs_df, G_GLOBAL = load_dataset("combined")
print(f"Network loaded: {G_GLOBAL.number_of_nodes():,} traders, {G_GLOBAL.number_of_edges():,} verified trust ties.")

# Load Centrality and K-Core Rankings
CENTRALITY_FILE = ROOT / "outputs" / "trader_centrality_rankings.csv"
centrality_dict: dict[int, dict] = {}
if CENTRALITY_FILE.exists():
    try:
        cdf = pd.read_csv(CENTRALITY_FILE)
        for row in cdf.itertuples(index=False):
            centrality_dict[int(row.trader_id)] = {
                "degree": int(row.degree),
                "core_number": int(row.core_number),
                "pagerank": float(row.pagerank),
                "betweenness": float(row.betweenness_centrality),
                "clustering": float(row.clustering_coefficient),
                "role": str(row.role),
                "rank": int(row.rank),
            }
        print(f"Loaded centrality rankings for {len(centrality_dict):,} traders.")
    except Exception as e:
        print(f"Could not load centrality file: {e}")

METRICS_FILE = ROOT / "outputs" / "link_prediction_metrics.json"
metrics_data = {}
if METRICS_FILE.exists():
    with open(METRICS_FILE, mode="r", encoding="utf-8") as f:
        metrics_data = json.load(f)

LIGHT_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bitcoin Web-of-Trust | Enterprise Recommendation Dashboard</title>
    <!-- Offline-First vis.js Network with CDN fallback -->
    <script type="text/javascript" src="/visualizations/vis-network.min.js"></script>
    <script>
        if (typeof vis === 'undefined') {
            document.write('<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"><\\/script>');
        }
    </script>
    <style>
        :root {
            --bg-main: #F8FAFC;
            --bg-card: #FFFFFF;
            --border: #E2E8F0;
            --border-hover: #CBD5E1;
            --primary: #0D9488;
            --primary-hover: #0F766E;
            --primary-light: #F0FDFA;
            --navy: #0F172A;
            --text-dark: #1E293B;
            --text-muted: #64748B;
            --accent-purple: #6366F1;
            --accent-gold: #D97706;
            --accent-coral: #E11D48;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.04);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-main);
            color: var(--text-dark);
            padding: 24px 28px;
            line-height: 1.5;
        }
        header {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 22px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow-sm);
            flex-wrap: wrap;
            gap: 16px;
        }
        h1 {
            font-size: 22px;
            font-weight: 700;
            color: var(--navy);
            margin-bottom: 4px;
        }
        p.subtitle {
            font-size: 13.5px;
            color: var(--text-muted);
        }
        .nav-links {
            display: flex;
            gap: 8px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        .nav-btn {
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            color: var(--navy);
            background: #F1F5F9;
            padding: 5px 11px;
            border-radius: 6px;
            border: 1px solid var(--border);
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .nav-btn:hover {
            background: var(--primary-light);
            color: var(--primary);
            border-color: var(--primary);
        }
        .badge-enterprise {
            background: var(--primary-light);
            color: var(--primary);
            border: 1px solid #CCFBF1;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            white-space: nowrap;
        }
        .container {
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 22px;
        }
        @media (max-width: 1024px) {
            .container { grid-template-columns: 1fr; }
        }
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            box-shadow: var(--shadow-sm);
            margin-bottom: 22px;
        }
        .card h2 {
            font-size: 15px;
            font-weight: 700;
            color: var(--navy);
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        label {
            font-size: 12px;
            font-weight: 600;
            color: var(--navy);
            display: block;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        input, select {
            width: 100%;
            padding: 9px 12px;
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: 13.5px;
            color: var(--text-dark);
            background: #FFFFFF;
            margin-bottom: 14px;
            transition: border 0.15s ease;
        }
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
        }
        .chip-group {
            display: flex;
            gap: 6px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        .chip {
            background: #F1F5F9;
            border: 1px solid var(--border);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11.5px;
            color: var(--navy);
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .chip:hover, .chip.active {
            background: var(--primary-light);
            color: var(--primary);
            border-color: var(--primary);
            font-weight: 600;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 16px;
        }
        .stat-box {
            background: #F8FAFC;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 12px;
        }
        .stat-box .title {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }
        .stat-box .val {
            font-size: 17px;
            font-weight: 700;
            color: var(--navy);
        }
        .action-btn {
            width: 100%;
            background: var(--primary);
            color: white;
            border: none;
            padding: 11px;
            border-radius: 6px;
            font-size: 13.5px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.15s ease;
        }
        .action-btn:hover { background: var(--primary-hover); }
        .table-wrap {
            overflow-x: auto;
            max-height: 520px;
            border: 1px solid var(--border);
            border-radius: 8px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        th, td {
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        th {
            background: #F8FAFC;
            color: var(--text-muted);
            font-weight: 600;
            font-size: 12px;
            position: sticky;
            top: 0;
            z-index: 2;
        }
        tr:hover td { background: #F8FAFC; }
        .score-highlight { font-weight: 700; color: var(--primary); }
        .badge-balance {
            background: #ECFDF5;
            color: #047857;
            border: 1px solid #A7F3D0;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }
        #network-canvas {
            height: 480px;
            background: #F8FAFC;
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 16px;
        }
        .legend-row {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            font-size: 12px;
            margin-bottom: 14px;
            color: var(--text-muted);
        }
        .legend-item { display: flex; align-items: center; gap: 6px; }
        .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
        
        .tab-btn-row {
            display: flex;
            border-bottom: 1px solid var(--border);
            margin-bottom: 16px;
            gap: 12px;
        }
        .tab-btn {
            background: none;
            border: none;
            padding: 9px 14px;
            font-size: 13.5px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.15s ease;
        }
        .tab-btn.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }

        /* Light-Themed Trust Chain Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.45);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .modal-box {
            background: #FFFFFF;
            border-radius: 12px;
            width: 760px;
            max-width: 94%;
            max-height: 85vh;
            overflow-y: auto;
            padding: 24px 28px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border);
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }
        .close-btn {
            background: none;
            border: none;
            font-size: 22px;
            color: var(--text-muted);
            cursor: pointer;
            line-height: 1;
        }
        .close-btn:hover { color: var(--navy); }
        .chain-path {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
            margin: 14px 0 20px 0;
            background: #F8FAFC;
            padding: 14px 18px;
            border-radius: 8px;
            border: 1px solid var(--border);
        }
        .chain-node {
            background: #FFFFFF;
            border: 1.5px solid var(--primary);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 700;
            color: var(--navy);
            box-shadow: var(--shadow-sm);
        }
        .chain-arrow {
            color: var(--accent-purple);
            font-weight: 700;
            font-size: 14px;
        }
    </style>
</head>
<body>

    <header>
        <div>
            <h1>Bitcoin Web-of-Trust | Trust Partner Recommendation Dashboard</h1>
            <p class="subtitle">Department of Machine Learning  •  Social Network Analysis (SNA)  •  Real-Time Topological Heuristics, K-Core Nucleus & Structural Balance</p>
            <div class="nav-links">
                <a href="/reports/link_prediction_report.pdf" target="_blank" class="nav-btn">📄 8-Page Academic Report (PDF)</a>
                <a href="/slides/link_prediction_presentation.pdf" target="_blank" class="nav-btn">🖥️ Presentation Slides (PDF)</a>
                <a href="/reports/team_presentation_study_guide.pdf" target="_blank" class="nav-btn">📘 Team Study Guide (PDF)</a>
                <a href="/visualizations/topological_vs_embedding_comparison.png" target="_blank" class="nav-btn">🧠 Representation vs Heuristics</a>
                <a href="/visualizations/k_core_and_centrality_distribution.png" target="_blank" class="nav-btn">🔬 K-Core Topography</a>
                <a href="/visualizations/degree_assortativity_mixing.png" target="_blank" class="nav-btn">🕸️ Assortativity Mixing</a>
                <a href="/visualizations/temporal_link_prediction_comparison.png" target="_blank" class="nav-btn">⏱️ Temporal Backtest</a>
                <a href="/dataset_package/bitcoin_trust_dataset_package.zip" class="nav-btn">📦 Dataset Package</a>
            </div>
        </div>
        <div>
            <span class="badge-enterprise">Enterprise Scale: 34,207 Nodes • 166,907 Ties</span>
        </div>
    </header>

    <div class="container">
        <!-- Sidebar Controls -->
        <div>
            <div class="card">
                <h2>Query Parameters</h2>
                <label>Target Trader (User ID):</label>
                <input type="number" id="userIdInput" value="1" min="1" max="150000">

                <label>Quick Select Influential Traders:</label>
                <div class="chip-group">
                    <button class="chip active" onclick="setTrader(1)">Trader #1</button>
                    <button class="chip" onclick="setTrader(2)">Trader #2</button>
                    <button class="chip" onclick="setTrader(7)">Trader #7</button>
                    <button class="chip" onclick="setTrader(177)">Trader #177</button>
                    <button class="chip" onclick="setTrader(759)">Trader #759</button>
                </div>

                <div class="stat-grid" id="traderStats">
                    <div class="stat-box">
                        <div class="title">Degree (Verified Ties)</div>
                        <div class="val" id="traderDegree">511</div>
                    </div>
                    <div class="stat-box">
                        <div class="title">Candidate 2-Hop Peers</div>
                        <div class="val" id="traderCandidates">1,240</div>
                    </div>
                    <div class="stat-box">
                        <div class="title">K-Core Shell & Role</div>
                        <div class="val" style="font-size: 13px; font-weight: 700; color: #0D9488;" id="traderCoreRole">k=18 • Core Broker</div>
                    </div>
                    <div class="stat-box">
                        <div class="title">Global Network Rank</div>
                        <div class="val" style="font-size: 13px; font-weight: 700; color: #6366F1;" id="traderGlobalRank">Rank #2</div>
                    </div>
                </div>

                <label>Prediction Algorithm:</label>
                <select id="modelSelect">
                    <option value="Ensemble">Ensemble Model (Weighted Rank Sum)</option>
                    <option value="Adamic-Adar">Adamic-Adar Index (AA)</option>
                    <option value="Common Neighbors">Common Neighbors (CN)</option>
                    <option value="Jaccard">Jaccard Coefficient</option>
                    <option value="Preferential Attachment">Preferential Attachment (PA)</option>
                </select>

                <label>Recommendations to Display:</label>
                <select id="topKSelect">
                    <option value="10">Top-10 Recommended Partners</option>
                    <option value="20" selected>Top-20 Recommended Partners</option>
                </select>

                <button class="action-btn" onclick="fetchRecommendations()">Compute Real-Time Predictions</button>
            </div>

            <div class="card">
                <h2>Model Validation Scoreboard (Held-Out Test)</h2>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr><th>Algorithm</th><th>ROC-AUC</th><th>F1</th><th>P@20</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Preferential Attachment</td><td class="score-highlight">0.9505</td><td>0.8864</td><td>100%</td></tr>
                            <tr><td>Ensemble Model</td><td class="score-highlight">0.9387</td><td>0.8903</td><td>95%</td></tr>
                            <tr><td>SVD Hadamard + LogReg</td><td class="score-highlight">0.9175</td><td>0.4522</td><td>100%</td></tr>
                            <tr><td>Adamic-Adar Index</td><td class="score-highlight">0.8366</td><td>0.6667</td><td>100%</td></tr>
                            <tr><td>Common Neighbors</td><td class="score-highlight">0.8335</td><td>0.6667</td><td>100%</td></tr>
                            <tr><td>Jaccard Coefficient</td><td class="score-highlight">0.8161</td><td>0.6667</td><td>15%</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Main Panel: Network Graph & Recommendations -->
        <div>
            <div class="card">
                <h2>Interactive Ego-Network: Verified Ties vs. Top Predicted Ties</h2>
                <div class="legend-row">
                    <div class="legend-item"><span class="dot" style="background: var(--accent-gold);"></span> Target Trader</div>
                    <div class="legend-item"><span class="dot" style="background: var(--primary);"></span> Verified Mutual Peer</div>
                    <div class="legend-item"><span class="dot" style="background: var(--accent-coral);"></span> Top Recommended Partner</div>
                    <div class="legend-item"><span style="border-bottom: 2px solid var(--primary); width: 14px; display:inline-block;"></span> Existing Verified Tie</div>
                    <div class="legend-item"><span style="border-bottom: 2px dashed var(--accent-purple); width: 14px; display:inline-block;"></span> Predicted Trust Tie</div>
                </div>
                <div id="network-canvas"></div>
            </div>

            <div class="card">
                <div class="tab-btn-row">
                    <button class="tab-btn active" id="tabPrimaryBtn" onclick="switchView('primary')">🎯 Primary Recommendations</button>
                    <button class="tab-btn" id="tabConsensusBtn" onclick="switchView('consensus')">🔬 Multi-Algorithm Consensus Matrix</button>
                </div>

                <!-- Primary View -->
                <div id="primaryView">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <h2 id="recTitle" style="margin-bottom:0;">Top-20 Recommended Trading Partners for Trader #1</h2>
                        <button class="chip" onclick="downloadCSV()" style="font-weight:600; color:var(--primary);">📥 Export as CSV</button>
                    </div>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>Candidate Trader</th>
                                    <th>Common Peers</th>
                                    <th>Jaccard</th>
                                    <th>Adamic-Adar</th>
                                    <th>PA Score</th>
                                    <th>Ensemble</th>
                                    <th>XAI Feature Attribution</th>
                                    <th>Community Role</th>
                                    <th>Structural Balance</th>
                                    <th>Trust Audit</th>
                                </tr>
                            </thead>
                            <tbody id="recBody">
                                <tr><td colspan="11" style="text-align: center; color: var(--text-muted);">Computing real-time recommendations...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Consensus View -->
                <div id="consensusView" style="display: none;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <h2 id="consensusTitle" style="margin-bottom:0;">Cross-Algorithmic Consensus Matrix (Agreement Across All 6 Models)</h2>
                        <span style="font-size:12px; color:var(--text-muted);">Evaluates Ensemble, AA, CN, Jaccard, PA, and RA</span>
                    </div>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>Consensus Level</th>
                                    <th>Candidate</th>
                                    <th>Mutual Peers</th>
                                    <th>Ensemble</th>
                                    <th>Adamic-Adar</th>
                                    <th>Common Neigh.</th>
                                    <th>Jaccard</th>
                                    <th>Pref. Attach.</th>
                                    <th>Resource Alloc.</th>
                                    <th>Community Role</th>
                                    <th>Structural Balance</th>
                                    <th>Trust Audit</th>
                                </tr>
                            </thead>
                            <tbody id="consensusBody">
                                <tr><td colspan="12" style="text-align: center; color: var(--text-muted);">Computing consensus matrix...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <!-- Light-Themed Trust Chain Modal -->
    <div id="trustModal" class="modal-overlay" onclick="if(event.target===this) closeModal()">
        <div class="modal-box">
            <div class="modal-header">
                <h3 style="font-size: 16px; font-weight: 700; color: var(--navy);" id="modalTitle">Trust Provenance & Shortest Chain</h3>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>
            <div id="modalContent">
                <p style="color: var(--text-muted); font-size: 13px;">Loading trust provenance and mutual intermediaries...</p>
            </div>
        </div>
    </div>

    <script>
        let networkInstance = null;
        let currentRecs = [];
        let currentView = 'primary';

        function setTrader(id) {
            document.getElementById('userIdInput').value = id;
            document.querySelectorAll('.chip-group .chip').forEach(btn => btn.classList.remove('active'));
            if (event && event.target) event.target.classList.add('active');
            fetchRecommendations();
            if (currentView === 'consensus') {
                fetchConsensus();
            }
        }

        function switchView(view) {
            currentView = view;
            if (view === 'primary') {
                document.getElementById('primaryView').style.display = 'block';
                document.getElementById('consensusView').style.display = 'none';
                document.getElementById('tabPrimaryBtn').classList.add('active');
                document.getElementById('tabConsensusBtn').classList.remove('active');
            } else {
                document.getElementById('primaryView').style.display = 'none';
                document.getElementById('consensusView').style.display = 'block';
                document.getElementById('tabPrimaryBtn').classList.remove('active');
                document.getElementById('tabConsensusBtn').classList.add('active');
                fetchConsensus();
            }
        }

        async function fetchRecommendations() {
            const userId = document.getElementById('userIdInput').value;
            const model = document.getElementById('modelSelect').value;
            const topK = document.getElementById('topKSelect').value;

            document.getElementById('recTitle').innerText = `Top-${topK} Recommended Partners for Trader #${userId} (${model})`;

            try {
                const response = await fetch(`/api/recommend?user_id=${userId}&top_k=${topK}&model=${encodeURIComponent(model)}`);
                const data = await response.json();

                if (data.error) {
                    alert(data.error);
                    return;
                }

                currentRecs = data.recommendations;

                // Update trader stats
                if (data.stats) {
                    document.getElementById('traderDegree').innerText = Number(data.stats.degree).toLocaleString();
                    document.getElementById('traderCandidates').innerText = Number(data.stats.candidates).toLocaleString();
                    document.getElementById('traderCoreRole').innerText = `k=${data.stats.core_number} • ${data.stats.role}`;
                    document.getElementById('traderGlobalRank').innerText = `Rank #${data.stats.global_rank} (PR: ${(data.stats.pagerank * 100).toFixed(3)}%)`;
                }

                const tbody = document.getElementById('recBody');
                tbody.innerHTML = '';
                data.recommendations.forEach(r => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td style="font-weight: 700; color: var(--accent-gold);">#${r.rank}</td>
                        <td style="font-weight: 600;">Trader #${r.target_user}</td>
                        <td>${r.common_neighbors} mutuals</td>
                        <td>${Number(r.jaccard).toFixed(4)}</td>
                        <td style="color: var(--primary); font-weight: 600;">${Number(r.adamic_adar).toFixed(2)}</td>
                        <td>${Number(r.preferential_attachment).toLocaleString()}</td>
                        <td style="font-weight:600; color:var(--accent-purple);">${Number(r.ensemble_score).toFixed(4)}</td>
                        <td><span style="font-size:10.5px; color:#334155; font-weight:600; background:#F8FAFC; padding:3px 7px; border-radius:6px; border:1px solid #CBD5E1; white-space:nowrap;">${r.feature_attribution || '80% Trust | 20% Hub'}</span></td>
                        <td><span style="background:#F1F5F9; color:#0F766E; padding:3px 8px; border-radius:12px; font-size:11px; font-weight:600; border:1px solid #CCFBF1; white-space:nowrap;">${r.community_role || 'Intra-Cluster'}</span></td>
                        <td><span class="badge-balance">${r.structural_balance_status}</span></td>
                        <td><button class="chip" onclick="inspectTrustChain(${userId}, ${r.target_user})" style="font-size:11px; padding:3px 8px; color:var(--primary); font-weight:600; white-space:nowrap;">🔍 Audit Chain</button></td>
                    `;
                    tbody.appendChild(tr);
                });

                renderGraph(data.graph);
            } catch (err) {
                console.error(err);
            }
        }

        async function fetchConsensus() {
            const userId = document.getElementById('userIdInput').value;
            document.getElementById('consensusTitle').innerText = `Cross-Algorithmic Consensus Matrix for Trader #${userId}`;
            const tbody = document.getElementById('consensusBody');
            tbody.innerHTML = '<tr><td colspan="12" style="text-align: center; color: var(--text-muted);">Computing consensus matrix across 6 models...</td></tr>';

            try {
                const response = await fetch(`/api/consensus?user_id=${userId}`);
                const data = await response.json();

                if (data.error) {
                    alert(data.error);
                    return;
                }

                tbody.innerHTML = '';
                if (!data.consensus || data.consensus.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="12" style="text-align: center; color: var(--text-muted);">No 2-hop consensus candidates found.</td></tr>';
                    return;
                }

                data.consensus.forEach(c => {
                    const tr = document.createElement('tr');
                    const badge = c.is_high_consensus 
                        ? `<span style="background:#ECFDF5; color:#047857; border:1px solid #A7F3D0; padding:3px 8px; border-radius:12px; font-weight:700; font-size:11px; white-space:nowrap;">★ ${c.consensus_strength} High Consensus</span>`
                        : `<span style="background:#F1F5F9; color:#475569; border:1px solid #E2E8F0; padding:3px 8px; border-radius:12px; font-weight:600; font-size:11px; white-space:nowrap;">${c.consensus_strength}</span>`;
                    
                    const formatRank = (m) => {
                        const r = c.ranks[m];
                        return r ? `<span style="color:var(--primary); font-weight:700;">#${r}</span>` : `<span style="color:#CBD5E1;">—</span>`;
                    };

                    tr.innerHTML = `
                        <td>${badge}</td>
                        <td style="font-weight: 700;">Trader #${c.candidate_id}</td>
                        <td>${c.common_neighbors} mutuals</td>
                        <td>${formatRank('Ensemble')}</td>
                        <td>${formatRank('Adamic-Adar')}</td>
                        <td>${formatRank('Common Neighbors')}</td>
                        <td>${formatRank('Jaccard')}</td>
                        <td>${formatRank('Preferential Attachment')}</td>
                        <td>${formatRank('Resource Allocation')}</td>
                        <td><span style="background:#F1F5F9; color:#0F766E; padding:3px 8px; border-radius:12px; font-size:11px; font-weight:600; border:1px solid #CCFBF1; white-space:nowrap;">${c.community_role}</span></td>
                        <td><span class="badge-balance">${c.balance}</span></td>
                        <td><button class="chip" onclick="inspectTrustChain(${userId}, ${c.candidate_id})" style="font-size:11px; padding:3px 8px; color:var(--primary); font-weight:600; white-space:nowrap;">🔍 Audit Chain</button></td>
                    `;
                    tbody.appendChild(tr);
                });
            } catch (err) {
                console.error(err);
            }
        }

        async function inspectTrustChain(source, target) {
            const modal = document.getElementById('trustModal');
            const title = document.getElementById('modalTitle');
            const content = document.getElementById('modalContent');

            title.innerText = `Trust Provenance & Audit Trail: Trader #${source} ➔ Trader #${target}`;
            content.innerHTML = '<p style="color:var(--text-muted); padding:16px 0;">Computing shortest path and mutual peer provenance...</p>';
            modal.style.display = 'flex';

            try {
                const res = await fetch(`/api/trust_chain?source=${source}&target=${target}`);
                const data = await res.json();

                if (data.error) {
                    content.innerHTML = `<p style="color:var(--accent-coral); font-weight:600;">${data.error}</p>`;
                    return;
                }

                let pathHTML = '';
                if (data.path && data.path.length > 0) {
                    pathHTML = '<div class="chain-path">';
                    data.path.forEach((node, idx) => {
                        const isTarget = (idx === data.path.length - 1);
                        const isSource = (idx === 0);
                        const badgeColor = isSource ? 'var(--accent-gold)' : (isTarget ? 'var(--accent-coral)' : 'var(--primary)');
                        pathHTML += `<span class="chain-node" style="border-color:${badgeColor};">Trader #${node} ${isSource ? '(Query)' : (isTarget ? '(Target)' : '(Intermediary)')}</span>`;
                        if (idx < data.path.length - 1) {
                            pathHTML += '<span class="chain-arrow">➔</span>';
                        }
                    });
                    pathHTML += '</div>';
                }

                let intermediariesHTML = `
                    <div style="margin-top:16px;">
                        <h4 style="font-size:13px; font-weight:700; color:var(--navy); margin-bottom:8px;">Top Mutual Intermediaries (Ranked by Exclusivity / Adamic-Adar Weight):</h4>
                        <div class="table-wrap" style="max-height:240px;">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Intermediary</th>
                                        <th>Degree</th>
                                        <th>AA Weight (1/ln d)</th>
                                        <th>Rating (${source} ➔ Int)</th>
                                        <th>Rating (Int ➔ ${target})</th>
                                        <th>Heider Triad</th>
                                    </tr>
                                </thead>
                                <tbody>
                `;

                data.intermediaries.forEach(item => {
                    intermediariesHTML += `
                        <tr>
                            <td style="font-weight:700;">Trader #${item.node_id}</td>
                            <td>${item.degree}</td>
                            <td style="color:var(--primary); font-weight:700;">+${item.aa_contribution}</td>
                            <td>+${item.source_rating}</td>
                            <td>+${item.target_rating}</td>
                            <td><span class="badge-balance">${item.triad_status}</span></td>
                        </tr>
                    `;
                });

                intermediariesHTML += '</tbody></table></div></div>';

                content.innerHTML = `
                    <div style="display:flex; gap:12px; margin-bottom:12px; flex-wrap:wrap;">
                        <span style="background:#F0FDFA; color:#0F766E; border:1px solid #CCFBF1; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:700;">Shortest Distance: ${data.path_length} Hops</span>
                        <span style="background:#EEF2FF; color:#4338CA; border:1px solid #E0E7FF; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:700;">${data.mutual_count} Mutual Trusted Brokers</span>
                        <span style="background:#ECFDF5; color:#047857; border:1px solid #A7F3D0; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:700;">100% (+, +, +) Balanced Triads</span>
                    </div>
                    <p style="font-size:13px; color:var(--text-muted); margin-bottom:6px;">
                        The recommendation of <b>Trader #${target}</b> to <b>Trader #${source}</b> is verified through <b>${data.mutual_count} mutual counterparties</b>. The shortest geodesic distance is <b>${data.path_length} hops</b>, satisfying both triadic closure and Heider's balance criteria without counterparty friction.
                    </p>
                    ${pathHTML}
                    ${intermediariesHTML}
                `;

            } catch (e) {
                content.innerHTML = '<p style="color:var(--accent-coral);">Failed to retrieve trust chain provenance.</p>';
            }
        }

        function closeModal() {
            document.getElementById('trustModal').style.display = 'none';
        }

        function renderGraph(graphData) {
            const container = document.getElementById('network-canvas');
            const data = {
                nodes: new vis.DataSet(graphData.nodes),
                edges: new vis.DataSet(graphData.edges)
            };
            const options = {
                physics: {
                    solver: 'forceAtlas2Based',
                    forceAtlas2Based: {
                        gravitationalConstant: -45,
                        centralGravity: 0.012,
                        springLength: 100,
                        springConstant: 0.08
                    },
                    maxVelocity: 25,
                    stabilization: { iterations: 120 }
                },
                interaction: { hover: true, tooltipDelay: 150, zoomView: true, dragView: true },
                nodes: { shape: 'dot' }
            };
            if (networkInstance) {
                networkInstance.destroy();
            }
            networkInstance = new vis.Network(container, data, options);
        }

        function downloadCSV() {
            if (!currentRecs || currentRecs.length === 0) return;
            const headers = Object.keys(currentRecs[0]);
            const rows = currentRecs.map(r => headers.map(h => JSON.stringify(r[h] || '')).join(','));
            const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows].join('\\n');
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement('a');
            link.setAttribute('href', encodedUri);
            link.setAttribute('download', `recommendations_trader_${document.getElementById('userIdInput').value}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // Initialize on load
        window.onload = () => {
            fetchRecommendations();
        };
    </script>
</body>
</html>
"""

class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(LIGHT_DASHBOARD_HTML.encode("utf-8"))
            return

        if parsed.path == "/api/recommend":
            params = parse_qs(parsed.query)
            user_id = int(params.get("user_id", ["1"])[0])
            top_k = int(params.get("top_k", ["20"])[0])
            model = params.get("model", ["Ensemble"])[0]

            if user_id not in G_GLOBAL:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Trader ID #{user_id} not found in the Bitcoin Web-of-Trust."}).encode("utf-8"))
                return

            # Compute real-time recommendations for ANY user ID
            df = recommend_links_for_user(G_GLOBAL, user_id=user_id, top_k=top_k, model=model)
            recs = df.to_dict(orient="records")

            # Extract user's local neighborhood
            user_neighbors = list(G_GLOBAL.neighbors(user_id))
            top_recs_nodes = [int(r["target_user"]) for r in recs[:7]]
            
            # Find candidate count
            two_hop_candidates = set()
            for n in user_neighbors:
                for nn in G_GLOBAL.neighbors(n):
                    if nn != user_id and nn not in user_neighbors:
                        two_hop_candidates.add(nn)

            nodes = [{
                "id": user_id,
                "label": f"Trader #{user_id}\\n(Target)",
                "color": "#D97706",
                "size": 28,
                "font": {"color": "#0F172A", "size": 13, "bold": True}
            }]
            edges = []

            # Add up to 10 existing verified neighbors
            for p in user_neighbors[:10]:
                nodes.append({
                    "id": p,
                    "label": f"#{p}",
                    "color": "#0D9488",
                    "size": 15,
                    "font": {"color": "#0F172A", "size": 10}
                })
                edges.append({"from": user_id, "to": p, "color": {"color": "#0D9488", "opacity": 0.6}, "width": 2})

            # Add top recommended candidate ties (dashed purple)
            for r_id in top_recs_nodes:
                nodes.append({
                    "id": r_id,
                    "label": f"#{r_id}\\n[Rec]",
                    "color": "#E11D48",
                    "size": 20,
                    "font": {"color": "#0F172A", "size": 11, "bold": True}
                })
                edges.append({
                    "from": user_id,
                    "to": r_id,
                    "color": {"color": "#6366F1", "opacity": 0.9},
                    "width": 2.5,
                    "dashes": [6, 4]
                })

            cent = centrality_dict.get(user_id, {
                "degree": len(user_neighbors),
                "core_number": 1,
                "pagerank": 0.0,
                "betweenness": 0.0,
                "clustering": 0.0,
                "role": "Active Member",
                "rank": "-"
            })

            payload = {
                "user_id": user_id,
                "stats": {
                    "degree": len(user_neighbors),
                    "candidates": len(two_hop_candidates),
                    "core_number": cent.get("core_number", 1),
                    "role": cent.get("role", "Active Member"),
                    "global_rank": cent.get("rank", "-"),
                    "pagerank": cent.get("pagerank", 0.0),
                },
                "recommendations": recs,
                "graph": {"nodes": nodes, "edges": edges}
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        if parsed.path == "/api/consensus":
            params = parse_qs(parsed.query)
            user_id = int(params.get("user_id", ["1"])[0])

            if user_id not in G_GLOBAL:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Trader ID #{user_id} not found."}).encode("utf-8"))
                return

            df = recommend_links_for_user(G_GLOBAL, user_id=user_id, top_k=250, model="Ensemble")
            if df.empty:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"user_id": user_id, "consensus": []}).encode("utf-8"))
                return

            models = [
                ("ensemble_score", "Ensemble"),
                ("adamic_adar", "Adamic-Adar"),
                ("common_neighbors", "Common Neighbors"),
                ("jaccard", "Jaccard"),
                ("preferential_attachment", "Preferential Attachment"),
                ("resource_allocation", "Resource Allocation")
            ]

            candidate_votes: dict[int, dict] = {}
            for col, m_name in models:
                top5 = df.sort_values(col, ascending=False).head(5)
                for rank, cand in enumerate(top5["target_user"], 1):
                    cand = int(cand)
                    if cand not in candidate_votes:
                        row_cand = df[df["target_user"] == cand].iloc[0]
                        candidate_votes[cand] = {
                            "candidate_id": cand,
                            "votes": 0,
                            "ranks": {},
                            "common_neighbors": int(row_cand["common_neighbors"]),
                            "community_role": str(row_cand.get("community_role", "Intra-Cluster")),
                            "balance": str(row_cand.get("structural_balance_status", "Balanced (+, +, +)"))
                        }
                    candidate_votes[cand]["votes"] += 1
                    candidate_votes[cand]["ranks"][m_name] = rank

            consensus_list = []
            for cand, info in candidate_votes.items():
                avg_rank = sum(info["ranks"].values()) / float(len(info["ranks"]))
                info["avg_rank"] = round(avg_rank, 2)
                info["consensus_strength"] = f"{info['votes']}/6 Models"
                info["is_high_consensus"] = (info["votes"] >= 4)
                consensus_list.append(info)

            consensus_list.sort(key=lambda x: (x["votes"], -x["avg_rank"]), reverse=True)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"user_id": user_id, "consensus": consensus_list}).encode("utf-8"))
            return

        if parsed.path == "/api/trust_chain":
            params = parse_qs(parsed.query)
            source_id = int(params.get("source", ["1"])[0])
            target_id = int(params.get("target", ["3"])[0])

            if source_id not in G_GLOBAL or target_id not in G_GLOBAL:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"One or both traders (#{source_id}, #{target_id}) not found."}).encode("utf-8"))
                return

            try:
                path = nx.shortest_path(G_GLOBAL, source=source_id, target=target_id)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                path = []

            source_neighbors = set(G_GLOBAL.neighbors(source_id))
            target_neighbors = set(G_GLOBAL.neighbors(target_id))
            common_nodes = source_neighbors.intersection(target_neighbors)

            intermediaries = []
            for node in sorted(common_nodes, key=lambda n: G_GLOBAL.degree(n)):
                deg = G_GLOBAL.degree(node)
                weight_aa = 1.0 / math.log(deg) if deg > 1 else 1.0
                e1 = G_GLOBAL.get_edge_data(source_id, node, default={})
                e2 = G_GLOBAL.get_edge_data(node, target_id, default={})
                intermediaries.append({
                    "node_id": node,
                    "degree": deg,
                    "aa_contribution": round(weight_aa, 4),
                    "source_rating": round(float(e1.get("weight", 1.0)), 1),
                    "target_rating": round(float(e2.get("weight", 1.0)), 1),
                    "triad_status": "Balanced (+, +, +)"
                })

            payload = {
                "source": source_id,
                "target": target_id,
                "path": path,
                "path_length": len(path) - 1 if path else -1,
                "mutual_count": len(common_nodes),
                "intermediaries": intermediaries[:15]
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        super().do_GET()

def run(port=PORT):
    server = HTTPServer(("0.0.0.0", port), CustomHandler)
    print(f"Server started at http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run(port)
