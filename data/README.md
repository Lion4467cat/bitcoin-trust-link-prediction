# Bitcoin Alpha raw dataset

`soc-sign-bitcoinalpha.csv.gz` is the compressed data file distributed by the Stanford Network Analysis Project (SNAP).

Each CSV row has four fields: `source,target,rating,time`. Source is the rater, target is the ratee, rating ranges from -10 (distrust) to +10 (trust), and time is a Unix timestamp. SNAP reports 3,783 users and 24,186 directed ratings, with 93% positive ratings.

Source: <https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html>

Please cite Kumar et al. (2016), “Edge Weight Prediction in Weighted Signed Networks,” IEEE ICDM, when using this dataset. The dataset is supplied unchanged. The processed undirected projection and its construction notes are in `outputs/` and `dataset_package/`.
