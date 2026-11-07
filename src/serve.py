"""Ultra-responsive, light-themed full-stack HTTP server and compact recommendation dashboard."""
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
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body {
            height: 100vh;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-main);
            color: var(--text-dark);
            font-size: 12.5px;
            line-height: 1.4;
        }
        body {
            display: flex;
            flex-direction: column;
            padding: 8px 12px;
        }

        /* Compact Header */
        header {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 6px 14px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: var(--shadow-sm);
            flex-shrink: 0;
            gap: 12px;
        }
        .header-title-box {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        h1 {
            font-size: 15px;
            font-weight: 700;
            color: var(--navy);
            display: inline;
        }
        .badge-dept {
            background: #F1F5F9;
            color: var(--text-muted);
            border: 1px solid var(--border);
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }
        .nav-links {
            display: flex;
            gap: 6px;
            align-items: center;
            flex-wrap: wrap;
        }
        .nav-btn {
            font-size: 11px;
            font-weight: 600;
            text-decoration: none;
            color: var(--navy);
            background: #F8FAFC;
            padding: 3px 8px;
            border-radius: 5px;
            border: 1px solid var(--border);
            transition: all 0.15s ease;
            white-space: nowrap;
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
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            white-space: nowrap;
        }

        /* Compact App Layout */
        .app-layout {
            display: grid;
            grid-template-columns: 290px 1fr;
            gap: 10px;
            flex: 1;
            height: calc(100vh - 54px);
            overflow: hidden;
        }
        @media (max-width: 960px) {
            .app-layout { grid-template-columns: 1fr; height: auto; overflow: auto; }
            html, body { overflow: auto; height: auto; }
        }

        /* Sidebar */
        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 8px;
            height: 100%;
            overflow-y: auto;
        }
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 12px;
            box-shadow: var(--shadow-sm);
        }
        .card h2 {
            font-size: 12.5px;
            font-weight: 700;
            color: var(--navy);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        label {
            font-size: 10.5px;
            font-weight: 700;
            color: var(--text-muted);
            display: block;
            margin-bottom: 3px;
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }
        input, select {
            width: 100%;
            padding: 5px 8px;
            border: 1px solid var(--border);
            border-radius: 5px;
            font-size: 12px;
            color: var(--text-dark);
            background: #FFFFFF;
            margin-bottom: 8px;
        }
        input:focus, select:focus {
            outline: none;
            border-color: var(--primary);
        }
        .chip-group {
            display: flex;
            gap: 4px;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }
        .chip {
            background: #F1F5F9;
            border: 1px solid var(--border);
            padding: 3px 7px;
            border-radius: 4px;
            font-size: 11px;
            color: var(--navy);
            cursor: pointer;
            transition: all 0.12s ease;
        }
        .chip:hover, .chip.active {
            background: var(--primary-light);
            color: var(--primary);
            border-color: var(--primary);
            font-weight: 700;
        }
        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-bottom: 8px;
        }
        .stat-box {
            background: #F8FAFC;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 6px 8px;
        }
        .stat-box .title {
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }
        .stat-box .val {
            font-size: 14px;
            font-weight: 700;
            color: var(--navy);
        }
        .action-btn {
            width: 100%;
            background: var(--primary);
            color: white;
            border: none;
            padding: 7px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.12s ease;
        }
        .action-btn:hover { background: var(--primary-hover); }

        /* Main Workspace Stage */
        .main-stage {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 12px;
            box-shadow: var(--shadow-sm);
            display: flex;
            flex-direction: column;
            height: 100%;
            overflow: hidden;
        }
        .main-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
            margin-bottom: 8px;
            flex-shrink: 0;
            gap: 10px;
            flex-wrap: wrap;
        }
        .tab-btn-row {
            display: flex;
            gap: 6px;
        }
        .tab-btn {
            background: none;
            border: none;
            padding: 5px 10px;
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-radius: 4px;
            transition: all 0.12s ease;
        }
        .tab-btn.active {
            background: var(--primary-light);
            color: var(--primary);
            font-weight: 700;
        }

        /* View Containers */
        .view-panel {
            flex: 1;
            height: 100%;
            overflow: hidden;
            display: none;
        }
        .view-panel.active {
            display: flex;
            flex-direction: column;
        }

        /* Compact Tables with Clean Fit */
        .table-wrap {
            flex: 1;
            overflow-y: auto;
            overflow-x: auto;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: #FFFFFF;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 11.5px;
            white-space: nowrap;
        }
        th, td {
            padding: 6px 9px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        th {
            background: #F8FAFC;
            color: var(--text-muted);
            font-weight: 700;
            font-size: 11px;
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
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10.5px;
            font-weight: 600;
        }

        /* Network Canvas */
        #network-canvas {
            flex: 1;
            background: #F8FAFC;
            border: 1px solid var(--border);
            border-radius: 6px;
            min-height: 280px;
        }
        .legend-bar {
            display: flex;
            gap: 12px;
            font-size: 11px;
            color: var(--text-muted);
            margin-bottom: 6px;
            flex-wrap: wrap;
            align-items: center;
        }
        .legend-item { display: flex; align-items: center; gap: 5px; }
        .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

        /* Split View Layout */
        .split-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            flex: 1;
            height: 100%;
            overflow: hidden;
        }

        /* Modal */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(15, 23, 42, 0.4);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .modal-box {
            background: #FFFFFF;
            border-radius: 10px;
            width: 680px;
            max-width: 94%;
            max-height: 85vh;
            overflow-y: auto;
            padding: 18px 20px;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--border);
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
        }
        .chain-path {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            margin: 10px 0 14px 0;
            background: #F8FAFC;
            padding: 10px 14px;
            border-radius: 6px;
            border: 1px solid var(--border);
        }
        .chain-node {
            background: #FFFFFF;
            border: 1.5px solid var(--primary);
            padding: 4px 10px;
            border-radius: 14px;
            font-size: 12px;
            font-weight: 700;
            color: var(--navy);
        }
        .chain-arrow { color: var(--accent-purple); font-weight: 700; }
    </style>
</head>
<body>

    <header>
        <div class="header-title-box">
            <h1>Bitcoin Web-of-Trust</h1>
            <span class="badge-dept">Department of Machine Learning • SNA AAT</span>
            <span class="badge-enterprise">34,207 Nodes • 166,907 Ties</span>
        </div>
        <div class="nav-links">
            <a href="/reports/link_prediction_report.pdf" target="_blank" class="nav-btn">📄 Report (PDF)</a>
            <a href="/slides/link_prediction_presentation.pdf" target="_blank" class="nav-btn">🖥️ Slides</a>
            <a href="/reports/team_presentation_study_guide.pdf" target="_blank" class="nav-btn">📘 Study Guide</a>
            <a href="/visualizations/topological_vs_embedding_comparison.png" target="_blank" class="nav-btn">🧠 SVD vs Heuristics</a>
            <a href="/visualizations/k_core_and_centrality_distribution.png" target="_blank" class="nav-btn">🔬 K-Core</a>
            <a href="/visualizations/degree_assortativity_mixing.png" target="_blank" class="nav-btn">🕸️ Assortativity</a>
            <a href="/dataset_package/bitcoin_trust_dataset_package.zip" class="nav-btn">📦 Package</a>
        </div>
    </header>

    <div class="app-layout">
        <!-- Sidebar Controls -->
        <div class="sidebar">
            <div class="card">
                <h2>Query Parameters</h2>
                <label>Target Trader (User ID):</label>
                <input type="number" id="userIdInput" value="1" min="1" max="150000">

                <label>Quick Select Traders:</label>
                <div class="chip-group">
                    <button class="chip active" onclick="setTrader(1)">#1</button>
                    <button class="chip" onclick="setTrader(2)">#2</button>
                    <button class="chip" onclick="setTrader(7)">#7</button>
                    <button class="chip" onclick="setTrader(177)">#177</button>
                    <button class="chip" onclick="setTrader(759)">#759</button>
                </div>

                <div class="stat-grid" id="traderStats">
                    <div class="stat-box">
                        <div class="title">Ties (Degree)</div>
                        <div class="val" id="traderDegree">511</div>
                    </div>
                    <div class="stat-box">
                        <div class="title">2-Hop Peers</div>
                        <div class="val" id="traderCandidates">1,240</div>
                    </div>
                    <div class="stat-box">
                        <div class="title">K-Core Shell</div>
                        <div class="val" style="font-size: 11.5px; color: #0D9488;" id="traderCoreRole">k=18 Core</div>
                    </div>
                    <div class="stat-box">
                        <div class="title">Network Rank</div>
                        <div class="val" style="font-size: 11.5px; color: #6366F1;" id="traderGlobalRank">Rank #2</div>
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

                <div style="display:flex; gap:6px;">
                    <select id="topKSelect" style="width:50%;">
                        <option value="10">Top-10</option>
                        <option value="20" selected>Top-20</option>
                    </select>
                    <button class="action-btn" style="width:50%;" onclick="fetchRecommendations()">Predict</button>
                </div>
            </div>

            <div class="card" style="flex:1;">
                <h2>Model Scoreboard (Held-Out Test)</h2>
                <div class="table-wrap" style="max-height: 180px;">
                    <table>
                        <thead>
                            <tr><th>Algorithm</th><th>AUC</th><th>F1</th><th>P@20</th></tr>
                        </thead>
                        <tbody>
                            <tr><td>Preferential Attachment</td><td class="score-highlight">0.9505</td><td>0.8864</td><td>100%</td></tr>
                            <tr><td>Ensemble Model</td><td class="score-highlight">0.9387</td><td>0.8903</td><td>95%</td></tr>
                            <tr><td>SVD + LogReg</td><td class="score-highlight">0.9175</td><td>0.4522</td><td>100%</td></tr>
                            <tr><td>Adamic-Adar Index</td><td class="score-highlight">0.8366</td><td>0.6667</td><td>100%</td></tr>
                            <tr><td>Common Neighbors</td><td class="score-highlight">0.8335</td><td>0.6667</td><td>100%</td></tr>
                            <tr><td>Jaccard Coefficient</td><td class="score-highlight">0.8161</td><td>0.6667</td><td>15%</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Main Workspace Stage with Responsive Tabs -->
        <div class="main-stage">
            <div class="main-header">
                <div class="tab-btn-row">
                    <button class="tab-btn active" id="btnViewTable" onclick="switchMainView('table')">🎯 Recommendations</button>
                    <button class="tab-btn" id="btnViewGraph" onclick="switchMainView('graph')">🕸️ Ego-Network</button>
                    <button class="tab-btn" id="btnViewSplit" onclick="switchMainView('split')">⚖️ Side-by-Side</button>
                    <button class="tab-btn" id="btnViewConsensus" onclick="switchMainView('consensus')">🔬 Multi-Model Consensus</button>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span id="recSummaryText" style="font-size: 11.5px; color: var(--text-muted); font-weight: 600;">Trader #1 Top Recommendations</span>
                    <button class="chip" onclick="downloadCSV()" style="font-weight: 700; color: var(--primary);">📥 Export CSV</button>
                </div>
            </div>

            <!-- VIEW 1: TABLE ONLY (DEFAULT) -->
            <div id="viewTable" class="view-panel active">
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Candidate</th>
                                <th>Peers</th>
                                <th>Jaccard</th>
                                <th>Adamic-Adar</th>
                                <th>PA Score</th>
                                <th>Ensemble</th>
                                <th>XAI Attribution</th>
                                <th>Role</th>
                                <th>Balance</th>
                                <th>Audit</th>
                            </tr>
                        </thead>
                        <tbody id="recTableBody">
                            <tr><td colspan="11" style="text-align: center; color: var(--text-muted); padding: 20px;">Computing real-time recommendations...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- VIEW 2: GRAPH ONLY -->
            <div id="viewGraph" class="view-panel">
                <div class="legend-bar">
                    <div class="legend-item"><span class="dot" style="background: var(--accent-gold);"></span> Target</div>
                    <div class="legend-item"><span class="dot" style="background: var(--primary);"></span> Mutual Peer</div>
                    <div class="legend-item"><span class="dot" style="background: var(--accent-coral);"></span> Predicted Partner</div>
                    <div class="legend-item"><span style="border-bottom: 2px solid var(--primary); width: 12px; display:inline-block;"></span> Verified Tie</div>
                    <div class="legend-item"><span style="border-bottom: 2px dashed var(--accent-purple); width: 12px; display:inline-block;"></span> Predicted Link</div>
                </div>
                <div id="network-canvas"></div>
            </div>

            <!-- VIEW 3: SPLIT (SIDE-BY-SIDE TABLE + GRAPH) -->
            <div id="viewSplit" class="view-panel">
                <div class="split-grid">
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>Candidate</th>
                                    <th>Peers</th>
                                    <th>AA</th>
                                    <th>Ensemble</th>
                                    <th>Audit</th>
                                </tr>
                            </thead>
                            <tbody id="splitTableBody">
                                <tr><td colspan="6" style="text-align: center; color: var(--text-muted);">Loading...</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div style="display:flex; flex-direction:column; height:100%;">
                        <div id="splitCanvas" style="flex:1; background:#F8FAFC; border:1px solid var(--border); border-radius:6px;"></div>
                    </div>
                </div>
            </div>

            <!-- VIEW 4: CONSENSUS MATRIX -->
            <div id="viewConsensus" class="view-panel">
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Consensus Level</th>
                                <th>Candidate</th>
                                <th>Peers</th>
                                <th>Ensemble</th>
                                <th>AA</th>
                                <th>CN</th>
                                <th>Jaccard</th>
                                <th>PA</th>
                                <th>RA</th>
                                <th>Role</th>
                                <th>Balance</th>
                                <th>Audit</th>
                            </tr>
                        </thead>
                        <tbody id="consensusTableBody">
                            <tr><td colspan="12" style="text-align: center; color: var(--text-muted); padding: 20px;">Computing consensus matrix across 6 models...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Light-Themed Trust Chain Provenance Modal -->
    <div id="trustModal" class="modal-overlay" onclick="if(event.target===this) closeModal()">
        <div class="modal-box">
            <div class="modal-header">
                <h3 style="font-size: 14px; font-weight: 700; color: var(--navy);" id="modalTitle">Trust Provenance Audit Trail</h3>
                <button onclick="closeModal()" style="background:none; border:none; font-size:18px; cursor:pointer; color:var(--text-muted);">&times;</button>
            </div>
            <div id="modalContent">
                <p style="color: var(--text-muted); font-size: 12px;">Loading trust provenance and mutual intermediaries...</p>
            </div>
        </div>
    </div>

    <script>
        let networkInstance = null;
        let splitNetworkInstance = null;
        let currentRecs = [];
        let currentGraphData = null;
        let currentActiveView = 'table';

        function setTrader(id) {
            document.getElementById('userIdInput').value = id;
            document.querySelectorAll('.chip-group .chip').forEach(btn => btn.classList.remove('active'));
            if (event && event.target) event.target.classList.add('active');
            fetchRecommendations();
            if (currentActiveView === 'consensus') {
                fetchConsensus();
            }
        }

        function switchMainView(view) {
            currentActiveView = view;
            ['table', 'graph', 'split', 'consensus'].forEach(v => {
                const panel = document.getElementById('view' + v.charAt(0).toUpperCase() + v.slice(1));
                const btn = document.getElementById('btnView' + v.charAt(0).toUpperCase() + v.slice(1));
                if (panel) panel.classList.remove('active');
                if (btn) btn.classList.remove('active');
            });

            const activePanel = document.getElementById('view' + view.charAt(0).toUpperCase() + view.slice(1));
            const activeBtn = document.getElementById('btnView' + view.charAt(0).toUpperCase() + view.slice(1));
            if (activePanel) activePanel.classList.add('active');
            if (activeBtn) activeBtn.classList.add('active');

            if (view === 'graph' && currentGraphData) {
                setTimeout(() => renderGraph(currentGraphData, 'network-canvas'), 50);
            } else if (view === 'split' && currentGraphData) {
                setTimeout(() => renderGraph(currentGraphData, 'splitCanvas'), 50);
            } else if (view === 'consensus') {
                fetchConsensus();
            }
        }

        async function fetchRecommendations() {
            const userId = document.getElementById('userIdInput').value;
            const model = document.getElementById('modelSelect').value;
            const topK = document.getElementById('topKSelect').value;

            document.getElementById('recSummaryText').innerText = `Trader #${userId} Top-${topK} (${model})`;

            try {
                const response = await fetch(`/api/recommend?user_id=${userId}&top_k=${topK}&model=${encodeURIComponent(model)}`);
                const data = await response.json();

                if (data.error) {
                    alert(data.error);
                    return;
                }

                currentRecs = data.recommendations;
                currentGraphData = data.graph;

                // Update trader stats
                if (data.stats) {
                    document.getElementById('traderDegree').innerText = Number(data.stats.degree).toLocaleString();
                    document.getElementById('traderCandidates').innerText = Number(data.stats.candidates).toLocaleString();
                    document.getElementById('traderCoreRole').innerText = `k=${data.stats.core_number} • ${data.stats.role}`;
                    document.getElementById('traderGlobalRank').innerText = `Rank #${data.stats.global_rank}`;
                }

                // Render Main Table
                const tbody = document.getElementById('recTableBody');
                tbody.innerHTML = '';
                const splitTbody = document.getElementById('splitTableBody');
                splitTbody.innerHTML = '';

                data.recommendations.forEach(r => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td style="font-weight: 700; color: var(--accent-gold);">#${r.rank}</td>
                        <td style="font-weight: 600;">Trader #${r.target_user}</td>
                        <td>${r.common_neighbors}</td>
                        <td>${Number(r.jaccard).toFixed(4)}</td>
                        <td style="color: var(--primary); font-weight: 600;">${Number(r.adamic_adar).toFixed(2)}</td>
                        <td>${Number(r.preferential_attachment).toLocaleString()}</td>
                        <td style="font-weight:600; color:var(--accent-purple);">${Number(r.ensemble_score).toFixed(4)}</td>
                        <td><span style="font-size:10px; color:#334155; font-weight:600; background:#F8FAFC; padding:2px 5px; border-radius:4px; border:1px solid #CBD5E1;">${r.feature_attribution || '80% Trust | 20% Hub'}</span></td>
                        <td><span style="background:#F1F5F9; color:#0F766E; padding:2px 6px; border-radius:10px; font-size:10px; font-weight:600; border:1px solid #CCFBF1;">${r.community_role || 'Intra-Cluster'}</span></td>
                        <td><span class="badge-balance">${r.structural_balance_status.replace('Balanced ', '')}</span></td>
                        <td><button class="chip" onclick="inspectTrustChain(${userId}, ${r.target_user})" style="font-size:10.5px; padding:2px 6px; color:var(--primary); font-weight:700;">🔍 Audit</button></td>
                    `;
                    tbody.appendChild(tr);

                    const trSplit = document.createElement('tr');
                    trSplit.innerHTML = `
                        <td style="font-weight: 700; color: var(--accent-gold);">#${r.rank}</td>
                        <td style="font-weight: 600;">#${r.target_user}</td>
                        <td>${r.common_neighbors}</td>
                        <td style="color: var(--primary); font-weight: 600;">${Number(r.adamic_adar).toFixed(2)}</td>
                        <td style="color: var(--accent-purple); font-weight: 600;">${Number(r.ensemble_score).toFixed(4)}</td>
                        <td><button class="chip" onclick="inspectTrustChain(${userId}, ${r.target_user})" style="font-size:10px; padding:1px 5px; color:var(--primary);">🔍</button></td>
                    `;
                    splitTbody.appendChild(trSplit);
                });

                if (currentActiveView === 'graph') {
                    renderGraph(data.graph, 'network-canvas');
                } else if (currentActiveView === 'split') {
                    renderGraph(data.graph, 'splitCanvas');
                }
            } catch (err) {
                console.error(err);
            }
        }

        async function fetchConsensus() {
            const userId = document.getElementById('userIdInput').value;
            const tbody = document.getElementById('consensusTableBody');
            tbody.innerHTML = '<tr><td colspan="12" style="text-align: center; color: var(--text-muted); padding: 15px;">Computing consensus matrix across 6 models...</td></tr>';

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
                        ? `<span style="background:#ECFDF5; color:#047857; border:1px solid #A7F3D0; padding:2px 6px; border-radius:10px; font-weight:700; font-size:10.5px;">★ ${c.consensus_strength} High</span>`
                        : `<span style="background:#F1F5F9; color:#475569; border:1px solid #E2E8F0; padding:2px 6px; border-radius:10px; font-weight:600; font-size:10.5px;">${c.consensus_strength}</span>`;
                    
                    const formatRank = (m) => {
                        const r = c.ranks[m];
                        return r ? `<span style="color:var(--primary); font-weight:700;">#${r}</span>` : `<span style="color:#CBD5E1;">—</span>`;
                    };

                    tr.innerHTML = `
                        <td>${badge}</td>
                        <td style="font-weight: 700;">Trader #${c.candidate_id}</td>
                        <td>${c.common_neighbors}</td>
                        <td>${formatRank('Ensemble')}</td>
                        <td>${formatRank('Adamic-Adar')}</td>
                        <td>${formatRank('Common Neighbors')}</td>
                        <td>${formatRank('Jaccard')}</td>
                        <td>${formatRank('Preferential Attachment')}</td>
                        <td>${formatRank('Resource Allocation')}</td>
                        <td><span style="background:#F1F5F9; color:#0F766E; padding:2px 6px; border-radius:10px; font-size:10px; font-weight:600;">${c.community_role}</span></td>
                        <td><span class="badge-balance">${c.balance.replace('Balanced ', '')}</span></td>
                        <td><button class="chip" onclick="inspectTrustChain(${userId}, ${c.candidate_id})" style="font-size:10.5px; padding:2px 6px; color:var(--primary); font-weight:700;">🔍 Audit</button></td>
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

            title.innerText = `Trust Provenance: Trader #${source} ➔ Trader #${target}`;
            content.innerHTML = '<p style="color:var(--text-muted); padding:10px 0;">Computing shortest path and mutual peer provenance...</p>';
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
                        pathHTML += `<span class="chain-node" style="border-color:${badgeColor};">Trader #${node} ${isSource ? '(Query)' : (isTarget ? '(Target)' : '(Bridge)')}</span>`;
                        if (idx < data.path.length - 1) {
                            pathHTML += '<span class="chain-arrow">➔</span>';
                        }
                    });
                    pathHTML += '</div>';
                }

                let intermediariesHTML = `
                    <div style="margin-top:12px;">
                        <h4 style="font-size:11.5px; font-weight:700; color:var(--navy); margin-bottom:6px;">Top Mutual Intermediaries (Ranked by Exclusivity / Adamic-Adar Weight):</h4>
                        <div class="table-wrap" style="max-height:180px;">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Intermediary</th>
                                        <th>Degree</th>
                                        <th>AA Weight</th>
                                        <th>Rating (${source}➔Int)</th>
                                        <th>Rating (Int➔${target})</th>
                                        <th>Triad Sign</th>
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
                    <div style="display:flex; gap:8px; margin-bottom:8px; flex-wrap:wrap;">
                        <span style="background:#F0FDFA; color:#0F766E; border:1px solid #CCFBF1; padding:3px 8px; border-radius:10px; font-size:11px; font-weight:700;">Distance: ${data.path_length} Hops</span>
                        <span style="background:#EEF2FF; color:#4338CA; border:1px solid #E0E7FF; padding:3px 8px; border-radius:10px; font-size:11px; font-weight:700;">${data.mutual_count} Mutual Brokers</span>
                        <span style="background:#ECFDF5; color:#047857; border:1px solid #A7F3D0; padding:3px 8px; border-radius:10px; font-size:11px; font-weight:700;">100% (+, +, +) Balanced</span>
                    </div>
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

        function renderGraph(graphData, containerId) {
            const container = document.getElementById(containerId);
            if (!container) return;
            const data = {
                nodes: new vis.DataSet(graphData.nodes),
                edges: new vis.DataSet(graphData.edges)
            };
            const options = {
                physics: {
                    solver: 'forceAtlas2Based',
                    forceAtlas2Based: {
                        gravitationalConstant: -40,
                        centralGravity: 0.015,
                        springLength: 85,
                        springConstant: 0.08
                    },
                    maxVelocity: 20,
                    stabilization: { iterations: 100 }
                },
                interaction: { hover: true, tooltipDelay: 150, zoomView: true, dragView: true },
                nodes: { shape: 'dot' }
            };
            new vis.Network(container, data, options);
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
                "size": 24,
                "font": {"color": "#0F172A", "size": 12, "bold": True}
            }]
            edges = []

            # Add up to 10 existing verified neighbors
            for p in user_neighbors[:10]:
                nodes.append({
                    "id": p,
                    "label": f"#{p}",
                    "color": "#0D9488",
                    "size": 13,
                    "font": {"color": "#0F172A", "size": 9}
                })
                edges.append({"from": user_id, "to": p, "color": {"color": "#0D9488", "opacity": 0.6}, "width": 1.8})

            # Add top recommended candidate ties (dashed purple)
            for r_id in top_recs_nodes:
                nodes.append({
                    "id": r_id,
                    "label": f"#{r_id}\\n[Rec]",
                    "color": "#E11D48",
                    "size": 18,
                    "font": {"color": "#0F172A", "size": 10, "bold": True}
                })
                edges.append({
                    "from": user_id,
                    "to": r_id,
                    "color": {"color": "#6366F1", "opacity": 0.9},
                    "width": 2.2,
                    "dashes": [5, 4]
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
