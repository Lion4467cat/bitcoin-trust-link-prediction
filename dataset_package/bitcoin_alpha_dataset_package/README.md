# Bitcoin Alpha trust network data package

## Files

- `raw/soc-sign-bitcoinalpha.csv.gz`: original SNAP file. Each record is `source,target,rating,time`; source is the rater, target is the ratee, ratings range from -10 to +10, and time is a Unix timestamp.
- `processed/signed_edge_list.csv`: one non-neutral undirected tie per unordered user pair, with signed mean rating, sign, count of source records, and time bounds.
- `processed/undirected_pair_aggregation.csv`: all 14,124 unordered pairs, including the 43 exact-zero neutral means excluded from the signed graph.
- `processed/bitcoin_alpha_signed.graphml`: the complete undirected signed graph for Cytoscape or other GraphML tools. Edge attributes include `sign`, `weight`, and `rating_count`.
- `manifest.json`: SHA-256 hashes and dataset statistics.

## Projection rule

Structural balance is evaluated on an undirected signed graph. We average all source ratings for each unordered pair. A positive mean yields sign +1, a negative mean yields sign -1, and an exact zero mean is retained as neutral in the audit file but omitted from the signed edge list. The graph retains all 3,783 source user IDs, including users who become isolates after neutral ties are removed.

## Source and citation

Stanford Network Analysis Project (SNAP), Bitcoin Alpha trust weighted signed network: https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html

Kumar, S., Spezzano, F., Subrahmanian, V. S., & Faloutsos, C. (2016). “Edge Weight Prediction in Weighted Signed Networks.” IEEE International Conference on Data Mining, pp. 221-230. Please cite the paper and check the SNAP source page for usage terms before redistribution.
