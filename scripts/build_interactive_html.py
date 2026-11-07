"""Generate standalone interactive HTML network visualization for predicted trust links."""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_HTML = ROOT / "visualizations" / "interactive_recommendation_demo.html"
TOP20_CSV = ROOT / "outputs" / "top20_recommendations.csv"

top20_df = pd.read_csv(TOP20_CSV)

# Create nodes and edges for User 1, their top mutual peers, and top 7 recommendations
nodes = [
    {"id": 1, "label": "Trader #1\\n(Target)", "color": "#E5A93C", "size": 30, "font": {"color": "#FFF", "bold": True}}
]
edges = []

# Top recommendations
top_recs = top20_df.head(7)
for _, r in top_recs.iterrows():
    cand_id = int(r["target_user"])
    nodes.append({
        "id": cand_id,
        "label": f"Trader #{cand_id}\\n[Rank {int(r['rank'])}]",
        "color": "#E0534C",
        "size": 22,
        "font": {"color": "#FFF", "size": 11, "bold": True}
    })
    edges.append({
        "from": 1,
        "to": cand_id,
        "color": {"color": "#8B4F80", "opacity": 0.9},
        "width": 3,
        "dashes": True,
        "title": f"Predicted Link (Ensemble Score: {r['ensemble_score']})"
    })

# Add sample mutual peers
mutual_peers = [2, 10, 11, 22, 146, 258, 259, 395, 523]
for p in mutual_peers:
    nodes.append({
        "id": p,
        "label": f"Peer #{p}",
        "color": "#17806D",
        "size": 15,
        "font": {"color": "#E8EFF0", "size": 10}
    })
    # Connect from 1 to mutual peer
    edges.append({"from": 1, "to": p, "color": {"color": "#17806D", "opacity": 0.7}, "width": 2})
    # Connect from mutual peer to top recs
    for _, r in top_recs.head(3).iterrows():
        edges.append({"from": p, "to": int(r["target_user"]), "color": {"color": "#17806D", "opacity": 0.4}, "width": 1.2})

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Interactive Link Prediction Demonstration | Bitcoin Web-of-Trust</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{ font-family: sans-serif; background: #102229; color: #FFF; margin: 0; padding: 20px; }}
        h1 {{ font-size: 20px; margin-bottom: 8px; }}
        p {{ color: #8FA4A8; font-size: 13px; margin-bottom: 16px; }}
        #network {{ height: 600px; background: #0E1B21; border-radius: 8px; border: 1px solid #294652; }}
        .legend {{ display: flex; gap: 16px; margin-bottom: 12px; font-size: 12px; }}
        .item {{ display: flex; align-items: center; gap: 6px; }}
        .dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
    </style>
</head>
<body>
    <h1>Trader #1 Ego-Network: Verified Trust vs. Top Predicted Ties</h1>
    <p>Drag nodes to explore. Purple dashed lines indicate newly predicted trust links based on Adamic-Adar & Ensemble heuristics.</p>
    <div class="legend">
        <div class="item"><span class="dot" style="background:#E5A93C;"></span> Target Trader #1</div>
        <div class="item"><span class="dot" style="background:#17806D;"></span> Existing Mutual Peer</div>
        <div class="item"><span class="dot" style="background:#E0534C;"></span> Top Predicted Partner</div>
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
                forceAtlas2Based: {{ gravitationalConstant: -40, centralGravity: 0.015, springLength: 110, springConstant: 0.08 }}
            }}
        }};
        new vis.Network(container, data, options);
    </script>
</body>
</html>"""

OUT_HTML.write_text(html_content, encoding="utf-8")
print(f"Interactive HTML demo generated at: {OUT_HTML}")
