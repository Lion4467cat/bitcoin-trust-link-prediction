"""Ultra-responsive, light-themed full-stack HTTP server and recommendation dashboard."""
from __future__ import annotations

import csv
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_loader import load_dataset
from src.recommend import recommend_links_for_user

PORT = 5000

print("Pre-loading Bitcoin Trust Network into memory for real-time inference...")
pairs_df, G_GLOBAL = load_dataset("combined")
print(f"Network loaded: {G_GLOBAL.number_of_nodes():,} traders, {G_GLOBAL.number_of_edges():,} verified trust ties.")

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
        h1 { font-size: 22px; font-weight: 700; color: var(--navy); }
        .subtitle { color: var(--text-muted); font-size: 13.5px; margin-top: 3px; }
        .badge-enterprise {
            background: #ECFDF5;
            color: #065F46;
            border: 1px solid #A7F3D0;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12.5px;
            font-weight: 600;
        }
        .nav-links {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 14px;
        }
        .nav-btn {
            background: #F1F5F9;
            border: 1px solid var(--border);
            color: var(--navy);
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12.5px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            transition: all 0.2s;
        }
        .nav-btn:hover {
            background: var(--primary);
            color: #FFFFFF;
            border-color: var(--primary);
        }
        .container {
            display: grid;
            grid-template-columns: 370px 1fr;
            gap: 24px;
        }
        @media (max-width: 1080px) {
            .container { grid-template-columns: 1fr; }
        }
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px 22px;
            box-shadow: var(--shadow-sm);
            margin-bottom: 22px;
        }
        h2 { font-size: 14.5px; font-weight: 700; color: var(--navy); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 14px; }
        label { display: block; font-size: 13px; font-weight: 600; color: var(--text-dark); margin-bottom: 6px; }
        select, input {
            width: 100%;
            padding: 10px 14px;
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-dark);
            font-size: 14px;
            margin-bottom: 14px;
            outline: none;
            transition: border-color 0.2s;
        }
        select:focus, input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.12); }
        .chip-group { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
        .chip {
            background: #F8FAFC;
            border: 1px solid var(--border);
            color: var(--text-dark);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s;
        }
        .chip:hover, .chip.active {
            background: var(--primary-light);
            border-color: var(--primary);
            color: var(--primary);
            font-weight: 600;
        }
        button.action-btn {
            width: 100%;
            background: var(--primary);
            color: #FFFFFF;
            border: none;
            padding: 11px;
            border-radius: 8px;
            font-size: 13.5px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.2s;
        }
        button.action-btn:hover { background: var(--primary-hover); }
        
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
        .stat-box .title { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }
        .stat-box .val { font-size: 17px; font-weight: 700; color: var(--navy); margin-top: 2px; }

        .table-wrap { overflow-x: auto; max-height: 440px; }
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
            margin-bottom: 14px;
            gap: 10px;
        }
        .tab-btn {
            background: none;
            border: none;
            padding: 8px 12px;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-bottom: 2px solid transparent;
        }
        .tab-btn.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
        }
    </style>
</head>
<body>

    <header>
        <div>
            <h1>Bitcoin Web-of-Trust | Trust Partner Recommendation Dashboard</h1>
            <p class="subtitle">Social Network Analysis (SNA) • Live Real-Time Topological Heuristics • Structural Balance Verification</p>
            <div class="nav-links">
                <a href="/reports/link_prediction_report.pdf" target="_blank" class="nav-btn">📄 Full Academic Report (PDF)</a>
                <a href="/slides/link_prediction_presentation.pdf" target="_blank" class="nav-btn">🖥️ Presentation Slides (PDF)</a>
                <a href="/reports/team_presentation_study_guide.pdf" target="_blank" class="nav-btn">📘 Team Study Guide (PDF)</a>
                <a href="/visualizations/link_prediction_roc_curves.png" target="_blank" class="nav-btn">📈 ROC Curves</a>
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
                                <th>Community Role</th>
                                <th>Structural Balance</th>
                            </tr>
                        </thead>
                        <tbody id="recBody">
                            <tr><td colspan="9" style="text-align: center; color: var(--text-muted);">Computing real-time recommendations...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        let networkInstance = null;
        let currentRecs = [];

        function setTrader(id) {
            document.getElementById('userIdInput').value = id;
            document.querySelectorAll('.chip').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            fetchRecommendations();
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
                        <td><span style="background:#F1F5F9; color:#0F766E; padding:3px 8px; border-radius:12px; font-size:11px; font-weight:600; border:1px solid #CCFBF1;">${r.community_role || 'Intra-Cluster'}</span></td>
                        <td><span class="badge-balance">${r.structural_balance_status}</span></td>
                    `;
                    tbody.appendChild(tr);
                });

                renderGraph(data.graph);
            } catch (err) {
                console.error(err);
            }
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
                    stabilization: { iterations: 100 }
                },
                interaction: { hover: true, zoomView: true }
            };
            if (networkInstance) { networkInstance.destroy(); }
            networkInstance = new vis.Network(container, data, options);
        }

        function downloadCSV() {
            if (!currentRecs.length) return;
            const headers = ["rank", "target_user", "common_neighbors", "jaccard", "adamic_adar", "preferential_attachment", "ensemble_score", "structural_balance_status"];
            let csvContent = "data:text/csv;charset=utf-8," + headers.join(",") + "\\n";
            currentRecs.forEach(r => {
                csvContent += headers.map(h => r[h]).join(",") + "\\n";
            });
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `recommendations_trader_${document.getElementById('userIdInput').value}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        window.onload = fetchRecommendations;
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

            payload = {
                "user_id": user_id,
                "stats": {
                    "degree": len(user_neighbors),
                    "candidates": len(two_hop_candidates)
                },
                "recommendations": recs,
                "graph": {"nodes": nodes, "edges": edges}
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
