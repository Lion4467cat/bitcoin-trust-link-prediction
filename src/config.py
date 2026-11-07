"""Configuration and paths for Enterprise-Scale Bitcoin Link Prediction & Recommendation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUTS_DIR = ROOT / "outputs"
VISUALIZATIONS_DIR = ROOT / "visualizations"
REPORTS_DIR = ROOT / "reports"
SLIDES_DIR = ROOT / "slides"
DATASET_PKG_DIR = ROOT / "dataset_package"
NOTEBOOKS_DIR = ROOT / "notebooks"

# Raw Data Paths
ALPHA_PATH = DATA_DIR / "soc-sign-bitcoinalpha.csv.gz"
OTC_PATH = DATA_DIR / "soc-sign-bitcoinotc.csv.gz"

# Processed & Synthetic Output Paths
COMBINED_CSV = OUTPUTS_DIR / "bitcoin_combined_signed.csv"
SYNTHETIC_CSV = OUTPUTS_DIR / "bitcoin_synthetic_enterprise.csv"
GRAPHML_PATH = OUTPUTS_DIR / "bitcoin_link_prediction.graphml"
METRICS_JSON = OUTPUTS_DIR / "link_prediction_metrics.json"
TOP20_RECOMMENDATIONS_CSV = OUTPUTS_DIR / "top20_recommendations.csv"

# Global Random Seed for Exact Reproducibility
RANDOM_SEED = 2026

# Train / Test Splitting Parameters
TRAIN_RATIO = 0.80
TEST_RATIO = 0.20

# Enterprise Scale Synthetic Parameters
SYNTHETIC_NODES = 25000
SYNTHETIC_EDGES = 150000
