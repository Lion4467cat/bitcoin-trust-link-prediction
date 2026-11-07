"""Reproducible Bitcoin Alpha signed-network structural balance analysis."""
from __future__ import annotations

import csv
import gzip
import json
import math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "soc-sign-bitcoinalpha.csv.gz"
OUT = ROOT / "outputs"
FIG = ROOT / "visualizations"
SEED = 2026
PERMUTATIONS = 1000

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titleweight": "bold",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def load_data(path: Path = RAW) -> tuple[pd.DataFrame, pd.DataFrame, nx.Graph]:
    raw = pd.read_csv(path, header=None, names=["source", "target", "rating", "time"])
    if raw.empty:
        raise ValueError("The raw dataset is empty.")
    for column in ["source", "target", "rating", "time"]:
        raw[column] = pd.to_numeric(raw[column], errors="coerce")
    if raw.isna().any().any():
        raise ValueError("The raw dataset contains missing values.")
    if not np.isfinite(raw[["source", "target", "rating", "time"]].to_numpy()).all():
        raise ValueError("The raw dataset contains non-finite values.")
    if raw[["source", "target", "rating", "time"]].apply(lambda col: (col % 1 != 0).any()).any():
        raise ValueError("User IDs, ratings, and timestamps must be integers.")
    if raw[["source", "target"]].duplicated().any():
        raise ValueError("Repeated directed user pairs found; inspect before continuing.")
    if (raw["source"] == raw["target"]).any():
        raise ValueError("Self-ties found; inspect before continuing.")
    if not raw["rating"].between(-10, 10).all():
        raise ValueError("Ratings outside the documented -10 to +10 range.")

    # Structural balance theory uses undirected signed ties. For each unordered
    # user pair, average all available ratings in either direction. Exact zero
    # means no net sign and is excluded from the signed projection.
    raw["u"] = np.minimum(raw["source"], raw["target"])
    raw["v"] = np.maximum(raw["source"], raw["target"])
    ties = (raw.groupby(["u", "v"], as_index=False)
            .agg(weight=("rating", "mean"), rating_count=("rating", "size"),
                 first_time=("time", "min"), last_time=("time", "max")))
    ties["sign"] = np.sign(ties["weight"]).astype(int)
    all_nodes = sorted(set(raw["source"]).union(raw["target"]))
    graph = nx.Graph()
    graph.add_nodes_from(all_nodes)
    signed = ties[ties["sign"] != 0].copy()
    for row in signed.itertuples(index=False):
        graph.add_edge(int(row.u), int(row.v), weight=float(row.weight), sign=int(row.sign),
                       rating_count=int(row.rating_count))
    return raw, ties, graph


def triangle_edge_indices(graph: nx.Graph) -> tuple[list[tuple[int, int, int]], list[tuple[int, int]]]:
    edges = sorted((min(u, v), max(u, v)) for u, v in graph.edges())
    edge_index = {edge: i for i, edge in enumerate(edges)}
    indexed = []
    for u in sorted(graph.nodes()):
        neighbors = sorted(v for v in graph.neighbors(u) if v > u)
        for i, v in enumerate(neighbors):
            for w in neighbors[i + 1:]:
                if graph.has_edge(v, w):
                    indexed.append((edge_index[(u, v)], edge_index[(u, w)], edge_index[(v, w)]))
    return indexed, edges


def collect_example_triangles(graph: nx.Graph) -> tuple[list[int], list[int]]:
    examples = {1: None, -1: None}
    for u in sorted(graph.nodes()):
        neighbors = sorted(v for v in graph.neighbors(u) if v > u)
        for i, v in enumerate(neighbors):
            for w in neighbors[i + 1:]:
                if graph.has_edge(v, w):
                    product = (graph[u][v]["sign"] * graph[u][w]["sign"] * graph[v][w]["sign"])
                    if examples[product] is None:
                        examples[product] = [u, v, w]
        if all(examples.values()):
            break
    return examples[1], examples[-1]


def save_figure(fig: plt.Figure, stem: str) -> None:
    fig.savefig(FIG / f"{stem}.png", dpi=220, bbox_inches="tight", facecolor="white")
    fig.savefig(FIG / f"{stem}.svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def create_figures(graph: nx.Graph, summary: dict, null_scores: np.ndarray,
                   signs: np.ndarray, triangles: np.ndarray) -> dict:
    FIG.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    # Edge sign balance
    pos = int(np.sum(signs > 0))
    neg = int(np.sum(signs < 0))
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    bars = ax.bar(["Positive trust", "Negative trust"], [pos, neg],
                  color=["#17806D", "#C8504B"], width=.56)
    ax.set_ylabel("Undirected ties")
    ax.set_title("The projected network is strongly positive")
    ax.bar_label(bars, labels=[f"{v:,}  ({v / (pos + neg):.1%})" for v in (pos, neg)], padding=5)
    ax.set_ylim(0, pos * 1.2)
    ax.grid(axis="y", color="#E4E8E9", linewidth=.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save_figure(fig, "edge_sign_distribution")

    # Null model histogram
    fig, ax = plt.subplots(figsize=(8.2, 4.7))
    ax.hist(null_scores, bins=28, color="#9DB4C0", edgecolor="white")
    ax.axvline(summary["balanced_triangle_fraction"], color="#C8504B", linewidth=2.4,
               label=f"Observed = {summary['balanced_triangle_fraction']:.1%}")
    ax.axvspan(summary["null_ci_low"], summary["null_ci_high"], color="#17806D", alpha=.12,
               label="95% null interval")
    ax.set_xlabel("Balanced triangle fraction after shuffling signs")
    ax.set_ylabel("Permutations")
    ax.set_title("Observed balance exceeds the sign-shuffle null model")
    ax.legend(frameon=False)
    ax.grid(axis="y", color="#E4E8E9", linewidth=.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    save_figure(fig, "balance_null_model")

    # Representative observed ego network. Pick the largest degree between
    # 12 and 20 so the display remains legible while showing local structure.
    candidates = [(d, n) for n, d in graph.degree() if 12 <= d <= 20]
    if candidates:
        _, center = max(candidates)
    else:
        center = max(graph.degree(), key=lambda item: item[1])[0]
    ego = nx.ego_graph(graph, center, radius=1)
    layout = nx.spring_layout(ego, seed=SEED, weight=None, k=1.15 / math.sqrt(max(1, len(ego))))
    fig, ax = plt.subplots(figsize=(8.2, 7.2))
    node_sizes = [210 if n == center else 105 for n in ego]
    nx.draw_networkx_edges(ego, layout, ax=ax,
        edgelist=[(u, v) for u, v, d in ego.edges(data=True) if d["sign"] > 0],
        edge_color="#17806D", width=1.8, alpha=.72)
    nx.draw_networkx_edges(ego, layout, ax=ax,
        edgelist=[(u, v) for u, v, d in ego.edges(data=True) if d["sign"] < 0],
        edge_color="#C8504B", width=1.8, style="dashed", alpha=.82)
    nx.draw_networkx_nodes(ego, layout, ax=ax, node_size=node_sizes,
                           node_color=["#D7A84A" if n == center else "#DCE6E8" for n in ego],
                           edgecolors="#35464D", linewidths=.8)
    sparse_labels = {n: str(n) for n in ego if n == center or graph.degree(n) <= 2}
    nx.draw_networkx_labels(ego, layout, labels=sparse_labels, ax=ax, font_size=7, font_color="#24343A")
    ax.set_title(f"Signed local network around user {center}", pad=14)
    ax.text(.5, -.03, "Green solid = positive trust    Red dashed = negative trust",
            transform=ax.transAxes, ha="center", va="top", fontsize=9, color="#52646B")
    ax.axis("off")
    fig.tight_layout()
    save_figure(fig, "signed_ego_network")

    # Two data-backed triangle motifs, one balanced and one unbalanced.
    balanced_nodes, unbalanced_nodes = collect_example_triangles(graph)
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.8))
    for ax, nodes, title, subtitle in [
        (axes[0], balanced_nodes, "Balanced example", "Product of signs = +1"),
        (axes[1], unbalanced_nodes, "Unbalanced example", "Product of signs = -1")]:
        motif = graph.subgraph(nodes).copy()
        posn = {nodes[0]: (-.5, 0), nodes[1]: (.5, 0), nodes[2]: (0, .82)}
        for u, v, data in motif.edges(data=True):
            color = "#17806D" if data["sign"] > 0 else "#C8504B"
            style = "solid" if data["sign"] > 0 else "dashed"
            nx.draw_networkx_edges(motif, posn, edgelist=[(u, v)], ax=ax, edge_color=color,
                                   style=style, width=2.5)
            x = (posn[u][0] + posn[v][0]) / 2
            y = (posn[u][1] + posn[v][1]) / 2
            ax.text(x, y + .06, "+" if data["sign"] > 0 else "−", ha="center", va="center",
                    fontsize=13, fontweight="bold", color=color,
                    bbox={"boxstyle": "circle,pad=.12", "facecolor": "white", "edgecolor": "none"})
        nx.draw_networkx_nodes(motif, posn, ax=ax, node_size=560, node_color="#DCE6E8",
                               edgecolors="#35464D", linewidths=1)
        nx.draw_networkx_labels(motif, posn, ax=ax, font_size=8)
        ax.set_title(title, fontsize=13, pad=4)
        ax.text(.5, -.06, subtitle, transform=ax.transAxes, ha="center", fontsize=9, color="#52646B")
        ax.set_xlim(-.95, .95); ax.set_ylim(-.35, 1.12); ax.axis("off")
    fig.tight_layout()
    save_figure(fig, "structural_balance_triads")

    # Standalone, dependency-free HTML uses the same selected ego network.
    nodes = [{"id": int(n), "label": str(n), "center": n == center} for n in ego]
    edges = [{"source": int(u), "target": int(v), "sign": int(d["sign"]),
              "weight": round(float(d["weight"]), 2)} for u, v, d in ego.edges(data=True)]
    html = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Bitcoin Alpha signed ego network</title>
<style>body{{font:16px system-ui,sans-serif;color:#24343a;margin:0;background:#f7f9f8}}header{{padding:20px 28px}}h1{{font-size:22px;margin:0 0 6px}}p{{margin:0;color:#52646b}}svg{{width:100%;height:78vh;display:block;background:white}}line{{stroke-width:2}}.pos{{stroke:#17806d}}.neg{{stroke:#c8504b;stroke-dasharray:6 4}}circle{{stroke:#35464d;stroke-width:1.4}}text{{font-size:12px;pointer-events:none}}.tip{{position:fixed;background:#24343a;color:white;padding:8px 10px;border-radius:4px;display:none;font-size:13px;pointer-events:none}}</style></head><body><header><h1>Bitcoin Alpha signed ego network</h1><p>Node {center} and its immediate neighbors. Green solid edges show positive trust; red dashed edges show negative trust. Hover for rating details.</p></header><svg id='graph' viewBox='0 0 1000 700' role='img' aria-label='Interactive signed network diagram'></svg><div id='tip' class='tip'></div>
<script>const nodes={json.dumps(nodes)};const edges={json.dumps(edges)};const svg=document.getElementById('graph'),tip=document.getElementById('tip'),ns='http://www.w3.org/2000/svg';let W=1000,H=700;
nodes.forEach((n,i)=>{{let a=2*Math.PI*i/nodes.length;n.x=W/2+250*Math.cos(a);n.y=H/2+245*Math.sin(a);n.vx=0;n.vy=0}});
function el(tag,attrs){{let x=document.createElementNS(ns,tag);for(const [k,v] of Object.entries(attrs))x.setAttribute(k,v);svg.appendChild(x);return x}}
let lines=edges.map(e=>{{let l=el('line',{{class:e.sign>0?'pos':'neg'}});return [e,l]}});let groups=nodes.map(n=>{{let g=document.createElementNS(ns,'g');svg.appendChild(g);let c=document.createElementNS(ns,'circle');c.setAttribute('r',n.center?13:9);c.setAttribute('fill',n.center?'#d7a84a':'#dce6e8');g.appendChild(c);let t=document.createElementNS(ns,'text');t.setAttribute('text-anchor','middle');t.setAttribute('dy',n.center?'-17':'-13');t.textContent=n.label;g.appendChild(t);g.addEventListener('mousemove',ev=>{{tip.style.display='block';tip.style.left=(ev.clientX+12)+'px';tip.style.top=(ev.clientY+12)+'px';tip.textContent='User '+n.label+(n.center?' (selected ego center)':'')}});g.addEventListener('mouseleave',()=>tip.style.display='none');return g}});
for(let k=0;k<180;k++){{for(const n of nodes){{n.vx+=(W/2-n.x)*.0008;n.vy+=(H/2-n.y)*.0008;for(const m of nodes){{if(n===m)continue;let dx=n.x-m.x,dy=n.y-m.y,d2=dx*dx+dy*dy+1;n.vx+=dx/d2*45;n.vy+=dy/d2*45}}}}for(const [e] of lines){{let a=nodes.find(n=>n.id===e.source),b=nodes.find(n=>n.id===e.target),dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1,f=(d-105)*.004;a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f}}for(const n of nodes){{n.x=Math.max(35,Math.min(W-35,n.x+n.vx*.85));n.y=Math.max(35,Math.min(H-35,n.y+n.vy*.85));n.vx*=.82;n.vy*=.82}}}}
lines.forEach(([e,l])=>{{let a=nodes.find(n=>n.id===e.source),b=nodes.find(n=>n.id===e.target);l.setAttribute('x1',a.x);l.setAttribute('y1',a.y);l.setAttribute('x2',b.x);l.setAttribute('y2',b.y);l.addEventListener('mousemove',ev=>{{tip.style.display='block';tip.style.left=(ev.clientX+12)+'px';tip.style.top=(ev.clientY+12)+'px';tip.textContent=(e.sign>0?'Positive':'Negative')+' tie, mean rating '+e.weight}});l.addEventListener('mouseleave',()=>tip.style.display='none')}});groups.forEach((g,i)=>g.setAttribute('transform',`translate(${{nodes[i].x}},${{nodes[i].y}})`));</script></body></html>"""
    (FIG / "interactive_signed_ego_network.html").write_text(html, encoding="utf-8")
    summary["ego_center_user_id"] = int(center)
    summary["ego_nodes"] = len(ego)
    summary["ego_edges"] = ego.number_of_edges()
    summary["balanced_example_nodes"] = balanced_nodes
    summary["unbalanced_example_nodes"] = unbalanced_nodes
    return summary


def main(verbose: bool = True) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    raw, all_pairs, graph = load_data()
    triangle_triples, edges = triangle_edge_indices(graph)
    triangle_array = np.asarray(triangle_triples, dtype=np.int32)
    if triangle_array.size == 0:
        raise ValueError("The projected graph contains no closed triads to analyze.")
    sign_by_edge = np.asarray([graph[u][v]["sign"] for u, v in edges], dtype=np.int8)
    observed = float(np.mean(np.prod(sign_by_edge[triangle_array], axis=1) > 0)) if len(triangle_array) else float("nan")

    rng = np.random.default_rng(SEED)
    null_scores = np.empty(PERMUTATIONS, dtype=float)
    for i in range(PERMUTATIONS):
        shuffled = rng.permutation(sign_by_edge)
        null_scores[i] = np.mean(np.prod(shuffled[triangle_array], axis=1) > 0)
    null_mean = float(null_scores.mean())
    null_sd = float(null_scores.std(ddof=1))
    p_upper = float((1 + np.sum(null_scores >= observed)) / (PERMUTATIONS + 1))
    components = sorted((len(c) for c in nx.connected_components(graph)), reverse=True)
    degrees = dict(graph.degree())
    clustering = nx.clustering(graph)
    top_nodes = sorted(graph.nodes(), key=lambda n: (-degrees[n], n))[:10]
    degree_centrality = nx.degree_centrality(graph)
    directed = nx.DiGraph()
    directed.add_nodes_from(sorted(set(raw["source"]).union(raw["target"])))
    directed.add_edges_from(zip(raw["source"], raw["target"]))
    pos_ties = int(np.sum(sign_by_edge > 0))
    neg_ties = int(np.sum(sign_by_edge < 0))
    balanced_n = int(np.sum(np.prod(sign_by_edge[triangle_array], axis=1) > 0))
    summary = {
        "source": "Stanford SNAP soc-sign-bitcoinalpha.csv.gz",
        "raw_ratings": int(len(raw)), "directed_users": int(directed.number_of_nodes()),
        "directed_ratings": int(directed.number_of_edges()),
        "undirected_pairs_before_neutral_removal": int(len(all_pairs)),
        "neutral_pairs_removed": int((all_pairs["sign"] == 0).sum()),
        "users_in_projection": int(graph.number_of_nodes()), "signed_ties": int(graph.number_of_edges()),
        "positive_ties": pos_ties, "negative_ties": neg_ties,
        "positive_tie_fraction": float(pos_ties / graph.number_of_edges()),
        "negative_tie_fraction": float(neg_ties / graph.number_of_edges()),
        "density": float(nx.density(graph)), "connected_components": int(len(components)),
        "largest_component_nodes": int(components[0]), "largest_component_fraction": float(components[0] / graph.number_of_nodes()),
        "isolates": int(nx.number_of_isolates(graph)),
        "mean_degree": float(np.mean(list(degrees.values()))),
        "median_degree": float(np.median(list(degrees.values()))),
        "mean_local_clustering": float(np.mean(list(clustering.values()))),
        "triangles": int(len(triangle_array)), "balanced_triangles": balanced_n,
        "unbalanced_triangles": int(len(triangle_array) - balanced_n),
        "balanced_triangle_fraction": observed,
        "null_model": "1000 permutations of signs across fixed undirected edges; sign counts preserved",
        "permutations": PERMUTATIONS, "random_seed": SEED,
        "null_mean": null_mean, "null_sd": null_sd,
        "null_ci_low": float(np.quantile(null_scores, .025)),
        "null_ci_high": float(np.quantile(null_scores, .975)),
        "z_score_vs_null": float((observed - null_mean) / null_sd),
        "permutation_p_upper": p_upper,
        "timestamp_min": int(raw["time"].min()), "timestamp_max": int(raw["time"].max()),
        "top_degree_users": [{"user_id": int(n), "degree": int(degrees[n]),
                              "degree_centrality": float(degree_centrality[n]),
                              "local_clustering": float(clustering[n])} for n in top_nodes],
    }

    # Processed graph edge list plus an audit trail for the projection.
    all_pairs.assign(sign=all_pairs["sign"].astype(int)).to_csv(OUT / "undirected_pair_aggregation.csv", index=False)
    all_pairs[all_pairs["sign"] != 0][["u", "v", "weight", "sign", "rating_count", "first_time", "last_time"]].to_csv(
        OUT / "signed_edge_list.csv", index=False)
    nx.write_graphml(graph, OUT / "bitcoin_alpha_signed.graphml")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    pd.DataFrame(summary["top_degree_users"]).to_csv(OUT / "top_degree_users.csv", index=False)
    (FIG / "README.md").write_text(
        "Generated by src/analyze.py. Figures use the Bitcoin Alpha signed network. "
        "Static plots are supplied as PNG and SVG; interactive_signed_ego_network.html "
        "is dependency-free and focuses on one ego network. For Cytoscape, import "
        "outputs/bitcoin_alpha_signed.graphml as a network. Map edge attribute `sign` "
        "to a discrete color (1 = green, -1 = red) and `weight` to edge width if desired.\n",
        encoding="utf-8")
    summary = create_figures(graph, summary, null_scores, sign_by_edge, triangle_array)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    np.savetxt(OUT / "null_model_scores.csv", null_scores, delimiter=",", header="balanced_triangle_fraction", comments="")
    if verbose:
        print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
