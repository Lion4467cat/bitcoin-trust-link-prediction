"""Plot Degree Assortativity and Neighbor Degree Mixing for Bitcoin Trust Network."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from src.data_loader import load_dataset
from src.config import VISUALIZATIONS_DIR

_, G = load_dataset("combined")

r = nx.degree_assortativity_coefficient(G)
knn = nx.average_degree_connectivity(G)

k_vals = sorted(knn.keys())
knn_vals = [knn[k] for k in k_vals]

plt.figure(figsize=(8.5, 5.4), dpi=220, facecolor="#F8FAFC")
ax = plt.gca()
ax.set_facecolor("#FFFFFF")

plt.loglog(k_vals, knn_vals, "o", color="#0D9488", markersize=5.5, alpha=0.8, label=f"Traders (Assortativity r = {r:.4f})")

# Fit power trendline
log_k = np.log(k_vals)
log_knn = np.log(knn_vals)
poly = np.polyfit(log_k, log_knn, 1)
fit_knn = np.exp(poly[1]) * (np.array(k_vals) ** poly[0])

plt.loglog(k_vals, fit_knn, "r--", linewidth=2.2, label=f"Disassortative Fit (Slope μ ≈ {poly[0]:.2f})")

plt.xlabel("Node Degree k (log scale)", fontsize=11, fontweight="bold", color="#0F172A")
plt.ylabel("Avg Neighbor Degree <k_nn(k)> (log scale)", fontsize=11, fontweight="bold", color="#0F172A")
plt.title(f"Disassortative Network Mixing: Broker-Hub Structure (r = {r:.4f})", fontsize=12, fontweight="bold", pad=12, color="#0F172A")
plt.grid(True, linestyle="--", alpha=0.3)
plt.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0", fontsize=9.5)
plt.tight_layout()

out_png = VISUALIZATIONS_DIR / "degree_assortativity_mixing.png"
out_svg = VISUALIZATIONS_DIR / "degree_assortativity_mixing.svg"
plt.savefig(out_png, dpi=220, facecolor="#F8FAFC")
plt.savefig(out_svg, facecolor="#F8FAFC")
plt.close()
print(f"Assortativity mixing plot saved to {out_png}")
