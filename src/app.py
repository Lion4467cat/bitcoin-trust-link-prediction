"""Interactive Web Demonstration UI for Bitcoin Link Prediction & Recommendation."""
from __future__ import annotations

import json
from pathlib import Path
from flask import Flask, jsonify, render_template_string, request
import networkx as nx

from src.config import OUTPUTS_DIR, METRICS_JSON
from src.data_loader import load_dataset
from src.recommend import recommend_links_for_user

app = Flask(__name__)

# Preload graph into memory for snappy UI response
print("Loading Bitcoin Trust Network into memory for Web UI...")
_, G_EMPIRICAL = load_dataset("combined")
print(f"Graph loaded successfully: {G_EMPIRICAL.number_of_nodes()} nodes, {G_EMPIRICAL.number_of_edges()} edges.")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bitcoin Web-of-Trust | Enterprise Link Prediction & Recommendation</title>
    <!-- vis.js Network CDN -->
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        :root {
            --navy: #102229;
            --dark-card: #19313A;
            --teal: #17806D;
            --teal-light: #20A38B;
            --gold: #E5A93C;
            --coral: #E0534C;
            --purple: #8B4F80;
            --text-light: #E8EFF0;
            --text-muted: #8FA4A8;
            --border: #294652;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--navy);
            color: var(--text-light);
            padding: 24px;
            min-height: 100vh;
        }
        header {
            margin-bottom: 24px;
            padding-bottom: 18px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }
        h1 { font-size: 24px; font-weight: 700; color: #FFFFFF; }
        .badge {
            background: rgba(23, 128, 109, 0.25);
            color: var(--teal-light);
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid var(--teal);
        }
        .container {
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 24px;
        }
        @media (max-width: 980px) {
            .container { grid-template-columns: 1fr; }
        }
        .card {
            background: var(--dark-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            margin-bottom: 20px;
        }
        h2 { font-size: 16px; margin-bottom: 14px; color: var(--gold); text-transform: uppercase; letter-spacing: 0.5px; }
        label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 6px; color: var(--text-muted); }
        select, input {
            width: 100%;
            padding: 10px 12px;
            background: #12242B;
            border: 1px solid var(--border);
            border-radius: 6px;
            color: white;
            font-size: 14px;
            margin-bottom: 14px;
            outline: none;
        }
        select:focus, input:focus { border-color: var(--teal-light); }
        .btn-group { display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }
        .chip-btn {
            background: #12242B;
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.2s;
        }
        .chip-btn:hover, .chip-btn.active {
            background: var(--teal);
            color: white;
            border-color: var(--teal-light);
        }
        button.primary-btn {
            width: 100%;
            background: var(--teal);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.2s;
        }
        button.primary-btn:hover { background: var(--teal-light); }
        .scoreboard-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }
        .scoreboard-table th, .scoreboard-table td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        .scoreboard-table th { color: var(--text-muted); font-weight: 600; }
        .score-val { color: var(--gold); font-weight: 700; }
        #network-canvas {
            height: 480px;
            background: #0E1B21;
            border-radius: 8px;
            border: 1px solid var(--border);
            margin-bottom: 20px;
        }
        .legend {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            font-size: 12px;
            margin-bottom: 16px;
            color: var(--text-muted);
        }
        .legend-item { display: flex; align-items: center; gap: 6px; }
        .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
        .rec-table-wrap {
            max-height: 400px;
            overflow-y: auto;
        }
        table.rec-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        table.rec-table th, table.rec-table td {
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        table.rec-table th {
            position: sticky;
            top: 0;
            background: #142830;
            color: var(--text-muted);
        }
        table.rec-table tr:hover { background: rgba(255,255,255,0.03); }
        .balance-badge {
            background: rgba(32, 163, 139, 0.2);
            color: #48E5C2;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
        }
    </style>
</head>
<body>

    <header>
        <div>
            <h1>Bitcoin Web-of-Trust Link Prediction & Recommendation</h1>
            <p style="color: var(--text-muted); font-size: 13px; margin-top: 4px;">
                Social Network Analysis (SNA) • Common Neighbors, Jaccard, Adamic-Adar, PA, and Structural Balance
            </p>
        </div>
        <div class="badge">Enterprise Benchmark: 9,207 Nodes | 31,050 Trust Ties</div>
    </header>

    <div class="container">
        <!-- Sidebar Controls -->
        <div>
            <div class="card">
                <h2>Query Parameters</h2>
                <label>Target Trader (User ID):</label>
                <input type="number" id="userIdInput" value="1" min="1" max="150000">

                <label>Sample Influential Traders:</label>
                <div class="btn-group">
                    <button class="chip-btn active" onclick="setTrader(1)">Trader #1</button>
                    <button class="chip-btn" onclick="setTrader(2)">Trader #2</button>
                    <button class="chip-btn" onclick="setTrader(7)">Trader #7</button>
                    <button class="chip-btn" onclick="setTrader(177)">Trader #177</button>
                    <button class="chip-btn" onclick="setTrader(759)">Trader #759</button>
                </div>

                <label>Link Prediction Algorithm:</label>
                <select id="modelSelect">
                    <option value="Ensemble">Ensemble Model (Weighted Rank)</option>
                    <option value="Adamic-Adar">Adamic-Adar Index (AA)</option>
                    <option value="Common Neighbors">Common Neighbors (CN)</option>
                    <option value="Jaccard">Jaccard Coefficient</option>
                    <option value="Preferential Attachment">Preferential Attachment (PA)</option>
                </select>

                <label>Number of Recommendations:</label>
                <select id="topKSelect">
                    <option value="10">Top-10 Predicted Links</option>
                    <option value="20" selected>Top-20 Predicted Links</option>
                    <option value="50">Top-50 Predicted Links</option>
                </select>

                <button class="primary-btn" onclick="fetchRecommendations()">Predict & Recommend</button>
            </div>

            <div class="card">
                <h2>Model Scoreboard (ROC-AUC)</h2>
                <table class="scoreboard-table">
                    <thead>
                        <tr><th>Algorithm</th><th>ROC-AUC</th><th>F1-Score</th><th>P@20</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Preferential Attach.</td><td class="score-val">0.9505</td><td>0.8864</td><td>1.00</td></tr>
                        <tr><td>Ensemble Model</td><td class="score-val">0.9387</td><td>0.8903</td><td>0.95</td></tr>
                        <tr><td>Adamic-Adar</td><td class="score-val">0.8366</td><td>0.6667</td><td>1.00</td></tr>
                        <tr><td>Common Neighbors</td><td class="score-val">0.8335</td><td>0.6667</td><td>1.00</td></tr>
                        <tr><td>Jaccard Coeff.</td><td class="score-val">0.8161</td><td>0.6667</td><td>0.15</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Main Display: Network Graph & Recommendations -->
        <div>
            <div class="card">
                <h2>Interactive Ego-Network & Predicted Trust Ties</h2>
                <div class="legend">
                    <div class="legend-item"><span class="dot" style="background: var(--gold);"></span> Target Trader</div>
                    <div class="legend-item"><span class="dot" style="background: var(--teal);"></span> Existing Trusted Neighbor</div>
                    <div class="legend-item"><span class="dot" style="background: var(--coral);"></span> Top Predicted Recommendation</div>
                    <div class="legend-item"><span style="border-bottom: 2px solid var(--teal); width: 14px; display:inline-block;"></span> Existing Trust Tie</div>
                    <div class="legend-item"><span style="border-bottom: 2px dashed var(--purple); width: 14px; display:inline-block;"></span> Predicted Trust Tie</div>
                </div>
                <div id="network-canvas"></div>
            </div>

            <div class="card">
                <h2 id="recTableTitle">Top-20 Predicted Trust Links for Trader #1</h2>
                <div class="rec-table-wrap">
                    <table class="rec-table">
                        <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Candidate Peer</th>
                                <th>Common Peers</th>
                                <th>Jaccard</th>
                                <th>Adamic-Adar</th>
                                <th>PA Score</th>
                                <th>Balance Triad</th>
                            </tr>
                        </thead>
                        <tbody id="recTableBody">
                            <tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Loading recommendations...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <script>
        let networkInstance = null;

        function setTrader(id) {
            document.getElementById('userIdInput').value = id;
            document.querySelectorAll('.chip-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            fetchRecommendations();
        }

        async function fetchRecommendations() {
            const userId = document.getElementById('userIdInput').value;
            const model = document.getElementById('modelSelect').value;
            const topK = document.getElementById('topKSelect').value;

            document.getElementById('recTableTitle').innerText = `Top-${topK} Predicted Links for Trader #${userId} (${model})`;
            document.getElementById('recTableBody').innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">Computing scores and triad closure...</td></tr>`;

            try {
                const response = await fetch(`/api/recommend?user_id=${userId}&top_k=${topK}&model=${encodeURIComponent(model)}`);
                const data = await response.json();
                
                if (data.error) {
                    alert(data.error);
                    return;
                }

                // Render Table
                const tbody = document.getElementById('recTableBody');
                tbody.innerHTML = '';
                data.recommendations.forEach(r => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td style="font-weight: 700; color: var(--gold);">#${r.rank}</td>
                        <td style="font-weight: 600; color: white;">Trader #${r.target_user}</td>
                        <td>${r.common_neighbors} mutuals</td>
                        <td>${r.jaccard}</td>
                        <td style="color: var(--teal-light); font-weight: 600;">${r.adamic_adar}</td>
                        <td>${Number(r.preferential_attachment).toLocaleString()}</td>
                        <td><span class="balance-badge">${r.structural_balance_status}</span></td>
                    `;
                    tbody.appendChild(tr);
                });

                // Render Graph
                renderGraph(data.graph);

            } catch (err) {
                console.error(err);
                alert("Failed to fetch recommendations.");
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
                        gravitationalConstant: -38,
                        centralGravity: 0.015,
                        springLength: 90,
                        springConstant: 0.08
                    },
                    stabilization: { iterations: 120 }
                },
                interaction: { hover: true, zoomView: true }
            };
            if (networkInstance) { networkInstance.destroy(); }
            networkInstance = new vis.Network(container, data, options);
        }

        window.onload = fetchRecommendations;
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/recommend")
def api_recommend():
    user_id = int(request.args.get("user_id", 1))
    top_k = int(request.args.get("top_k", 20))
    model = request.args.get("model", "Ensemble")
    
    if user_id not in G_EMPIRICAL:
        return jsonify({"error": f"Trader ID {user_id} not found in Bitcoin network."}), 404
        
    df = recommend_links_for_user(G_EMPIRICAL, user_id=user_id, top_k=top_k, model=model)
    recs = df.to_dict(orient="records")
    
    # Build Graph visualization payload
    user_neighbors = list(G_EMPIRICAL.neighbors(user_id))[:15]
    top_recs = [r["target_user"] for r in recs[:7]]
    
    nodes = []
    edges = []
    
    # Target User (Gold)
    nodes.append({
        "id": user_id,
        "label": f"Trader #{user_id}\\n(Target)",
        "color": "#E5A93C",
        "size": 26,
        "font": {"color": "#FFFFFF", "size": 13, "bold": True}
    })
    
    # Existing Neighbors (Teal)
    for n in user_neighbors:
        nodes.append({
            "id": n,
            "label": f"#{n}",
            "color": "#17806D",
            "size": 14,
            "font": {"color": "#E8EFF0", "size": 10}
        })
        edges.append({
            "from": user_id,
            "to": n,
            "color": {"color": "#17806D", "opacity": 0.7},
            "width": 2
        })
        
    # Top Predicted Recommendations (Coral)
    for r in top_recs:
        nodes.append({
            "id": r,
            "label": f"#{r}\\n[Rec]",
            "color": "#E0534C",
            "size": 18,
            "font": {"color": "#FFFFFF", "size": 11, "bold": True}
        })
        edges.append({
            "from": user_id,
            "to": r,
            "color": {"color": "#8B4F80", "opacity": 0.9},
            "width": 2.5,
            "dashes": [6, 4] # Dashed link indicating prediction
        })
        
    return jsonify({
        "user_id": user_id,
        "recommendations": recs,
        "graph": {"nodes": nodes, "edges": edges}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
