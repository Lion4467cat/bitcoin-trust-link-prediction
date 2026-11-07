# Bitcoin Web-of-Trust Dataset Package (Empirical & Enterprise Synthetic)

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
