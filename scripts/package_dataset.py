"""Assemble raw, processed, and enterprise synthetic network data into a portable ZIP package."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "dataset_package" / "bitcoin_trust_dataset_package"
ZIP = ROOT / "dataset_package" / "bitcoin_trust_dataset_package.zip"

for rel in ["raw", "processed"]:
    (PACKAGE / rel).mkdir(parents=True, exist_ok=True)

# Copy raw files
shutil.copy2(ROOT / "data" / "soc-sign-bitcoinalpha.csv.gz", PACKAGE / "raw" / "soc-sign-bitcoinalpha.csv.gz")
shutil.copy2(ROOT / "data" / "soc-sign-bitcoinotc.csv.gz", PACKAGE / "raw" / "soc-sign-bitcoinotc.csv.gz")

# Copy processed & synthetic files
shutil.copy2(ROOT / "outputs" / "bitcoin_synthetic_enterprise.csv", PACKAGE / "processed" / "bitcoin_synthetic_enterprise.csv")
shutil.copy2(ROOT / "outputs" / "top20_recommendations.csv", PACKAGE / "processed" / "top20_recommendations.csv")
shutil.copy2(ROOT / "outputs" / "bitcoin_link_prediction.graphml", PACKAGE / "processed" / "bitcoin_link_prediction.graphml")
shutil.copy2(ROOT / "outputs" / "link_prediction_metrics.json", PACKAGE / "processed" / "link_prediction_metrics.json")
if (ROOT / "outputs" / "temporal_link_prediction_metrics.json").exists():
    shutil.copy2(ROOT / "outputs" / "temporal_link_prediction_metrics.json", PACKAGE / "processed" / "temporal_link_prediction_metrics.json")
if (ROOT / "outputs" / "trader_centrality_rankings.csv").exists():
    shutil.copy2(ROOT / "outputs" / "trader_centrality_rankings.csv", PACKAGE / "processed" / "trader_centrality_rankings.csv")

readme = """# Bitcoin Web-of-Trust Dataset Package (Empirical & Enterprise Synthetic)

## Overview
This dataset package provides both empirical and enterprise-scale network data for Link Prediction and Trust Partner Recommendation in cryptocurrency trading networks.

## Files
- `raw/soc-sign-bitcoinalpha.csv.gz`: Original Stanford SNAP Bitcoin Alpha trust network (3,783 users, 24,186 ratings).
- `raw/soc-sign-bitcoinotc.csv.gz`: Original Stanford SNAP Bitcoin OTC trust network (5,887 users, 35,592 ratings).
- `processed/bitcoin_synthetic_enterprise.csv`: Enterprise-scale synthetic trust network (25,000 nodes, 135,857 edges) generated using the Holme-Kim power-law clustering model calibrated to Bitcoin's empirical topology.
- `processed/top20_recommendations.csv`: Model-generated Top-20 recommended trust partners for sample target traders.
- `processed/bitcoin_link_prediction.graphml`: Formatted signed graph for Cytoscape analysis and network rendering.
- `processed/link_prediction_metrics.json`: Complete benchmark metrics (ROC-AUC, Precision@K, F1) across CN, Jaccard, Adamic-Adar, PA, and Ensemble models.
- `manifest.json`: Cryptographic SHA-256 verification hashes and dataset statistics.

## Citations
- Stanford SNAP Bitcoin Web-of-Trust: https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html
- Kumar et al. (2016), "Edge Weight Prediction in Weighted Signed Networks", IEEE ICDM.
"""
(PACKAGE / "README.md").write_text(readme, encoding="utf-8")

def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

files = [
    PACKAGE / "raw" / "soc-sign-bitcoinalpha.csv.gz",
    PACKAGE / "raw" / "soc-sign-bitcoinotc.csv.gz",
    PACKAGE / "processed" / "bitcoin_synthetic_enterprise.csv",
    PACKAGE / "processed" / "top20_recommendations.csv",
    PACKAGE / "processed" / "bitcoin_link_prediction.graphml",
    PACKAGE / "processed" / "link_prediction_metrics.json",
    PACKAGE / "processed" / "temporal_link_prediction_metrics.json",
    PACKAGE / "processed" / "trader_centrality_rankings.csv",
    PACKAGE / "README.md"
]

manifest = {
    "project": "Enterprise Trust Recommendation & Link Prediction in Bitcoin Web-of-Trust",
    "sha256": {str(p.relative_to(PACKAGE)): sha256(p) for p in files},
    "statistics": {
        "empirical_alpha_ratings": 24186,
        "empirical_otc_ratings": 35592,
        "empirical_combined_nodes": 9207,
        "empirical_combined_edges": 31050,
        "enterprise_synthetic_nodes": 25000,
        "enterprise_synthetic_edges": 135857
    }
}

(PACKAGE / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED) as z:
    for path in sorted(PACKAGE.rglob("*")):
        if path.is_file():
            z.write(path, path.relative_to(PACKAGE.parent))

# Also copy to legacy name for backward compatibility
shutil.copy2(ZIP, ROOT / "dataset_package" / "bitcoin_alpha_dataset_package.zip")
print(f"Dataset package created: {ZIP} ({ZIP.stat().st_size / (1024*1024):.2f} MB)")
