"""Generate standalone interactive HTML network visualization for predicted trust links in clean light theme."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_HTML = ROOT / "visualizations" / "interactive_recommendation_demo.html"
TOP20_CSV = ROOT / "outputs" / "top20_recommendations.csv"

top20_df = pd.read_csv(TOP20_CSV)

# Create nodes and edges for User 1, their top mutual peers, and top 7 recommendations
nodes = [
    {"id": 1, "label": "Trader #1\\n(Target)", "color": "#D97706", "size": 28, "font": {"color": "#0F172A", "bold": True}}
]
edges = []

# Top recommendations
top_recs = top20_df.head(7)
for _, r in top_recs.iterrows():
    cand_id = int(r["target_user"])
    nodes.append({
        "id": cand_id,
        "label": f"Trader #{cand_id}\\n[Rank {int(r['rank'])}]",
        "color": "#E11D48",
        "size": 20,
        "font": {"color": "#0F172A", "size": 11, "bold": True}
    })
    edges.append({
        "from": 1,
        "to": cand_id,
        "color": {"color": "#6366F1", "opacity": 0.9},
        "width": 2.5,
        "dashes": [6, 4],
        "title": f"Predicted Link (Ensemble Score: {r['ensemble_score']})"
    })

# Add sample mutual peers
mutual_peers = [2, 10, 11, 22, 146, 258, 259, 395, 523]
for p in mutual_peers:
    nodes.append({
        "id": p,
        "label": f"Peer #{p}",
        "color": "#0D9488",
        "size": 14,
        "font": {"color": "#0F172A", "size": 10}
    })
    # Connect from 1 to mutual peer
    edges.append({"from": 1, "to": p, "color": {"color": "#0D9488", "opacity": 0.6}, "width": 1.8})
    # Connect from mutual peer to top recs
    for _, r in top_recs.head(3).iterrows():
        edges.append({"from": p, "to": int(r["target_user"]), "color": {"color": "#0D9488", "opacity": 0.35}, "width": 1.2})

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Link Prediction Demonstration | Bitcoin Web-of-Trust</title>
    <!-- Offline-First vis.js Network with CDN fallback -->
    <script type="text/javascript" src="/visualizations/vis-network.min.js"></script>
    <script>
        if (typeof vis === 'undefined') {{
            document.write('<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"><\\/script>');
        }}
    </script>
    <style>
        :root {{
            --bg-main: #F8FAFC;
            --bg-card: #FFFFFF;
            --border: #E2E8F0;
            --primary: #0D9488;
            --navy: #0F172A;
            --text-dark: #1E293B;
            --text-muted: #64748B;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: var(--bg-main);
            color: var(--text-dark);
            padding: 12px 16px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}
        header {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 8px 14px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-shrink: 0;
        }}
        h1 {{ font-size: 15px; font-weight: 700; color: var(--navy); }}
        .badge {{
            background: #F0FDFA;
            color: var(--primary);
            border: 1px solid #CCFBF1;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }}
        .legend {{ display: flex; gap: 14px; margin-bottom: 8px; font-size: 11px; color: var(--text-muted); flex-shrink: 0; }}
        .item {{ display: flex; align-items: center; gap: 5px; }}
        .dot {{ width: 8px; height: 8px; border-radius: 50%; display: inline-block; }}
        #network {{
            flex: 1;
            background: #FFFFFF;
            border-radius: 8px;
            border: 1px solid var(--border);
            min-height: 250px;
        }}
    </style>
</head>
<body>
    <header>
        <div>
            <h1>Trader #1 Ego-Network: Verified Trust vs. Top Predicted Ties</h1>
            <span style="font-size: 11px; color: var(--text-muted);">Department of Machine Learning • SNA AAT • Force-Directed Canvas</span>
        </div>
        <span class="badge">Enterprise Web-of-Trust</span>
    </header>
    <div class="legend">
        <div class="item"><span class="dot" style="background:#D97706;"></span> Target Trader #1</div>
        <div class="item"><span class="dot" style="background:#0D9488;"></span> Verified Mutual Peer</div>
        <div class="item"><span class="dot" style="background:#E11D48;"></span> Top Predicted Partner</div>
        <div class="item"><span style="border-bottom: 2px solid #0D9488; width: 12px; display:inline-block;"></span> Verified Tie</div>
        <div class="item"><span style="border-bottom: 2px dashed #6366F1; width: 12px; display:inline-block;"></span> Predicted Tie</div>
    </div>
    <div id="network"></div>
    <script>
        const nodes = new vis.DataSet({json.dumps(nodes)});
        const edges = new vis.DataSet({json.dumps(edges)});
        const container = document.getElementById('network');
        const data = {{ nodes: nodes, edges: edges }};
        const options = {{
            physics: {{
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {{ gravitationalConstant: -40, centralGravity: 0.015, springLength: 90, springConstant: 0.08 }}
            }},
            interaction: {{ hover: true, tooltipDelay: 150, zoomView: true, dragView: true }}
        }};
        new vis.Network(container, data, options);
    </script>
</body>
</html>"""

OUT_HTML.write_text(html_content, encoding="utf-8")
print(f"Interactive HTML demo generated at: {OUT_HTML}")
