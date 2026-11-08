# Team Presentation Study Guide & Master Handbook
## Trust & Reputation Link Prediction in Decentralized Crypto Trading Networks
**Course:** Social Network Analysis — Applied Assessment Task (SNA-AAT)  
**Primary Datasets:** SNAP Bitcoin Alpha ($3,783$ nodes, $24,186$ ratings) & SNAP Bitcoin OTC ($5,887$ nodes, $35,592$ ratings)  
**Unified Empirical Network:** $9,207$ unique traders, $31,050$ verified trust ties  
**Enterprise Scalability Benchmark:** $25,000$-node synthetic Holme-Kim power-law clustered trust network ($135,857$ ties)

---

## Table of Contents
1. [Part 1: Executive Elevator Pitch & 3-Speaker Delivery Plan](#part-1-executive-elevator-pitch--3-speaker-delivery-plan)
2. [Part 2: Complete Slide-by-Slide Verbatim Scripts & Visual Cues (Slides 1–14)](#part-2-complete-slide-by-slide-verbatim-scripts--visual-cues-slides-114)
3. [Part 3: Deep-Dive Mathematical & Algorithmic Reference Guide](#part-3-deep-dive-mathematical--algorithmic-reference-guide)
4. [Part 4: Complete Metrics, Datasets & Scoreboard Reference Tables](#part-4-complete-metrics-datasets--scoreboard-reference-tables)
5. [Part 5: Visual Guide to Explaining Every Figure & Chart](#part-5-visual-guide-to-explaining-every-figure--chart)
6. [Part 6: Step-by-Step Live Interactive Web Dashboard Walkthrough](#part-6-step-by-step-live-interactive-web-dashboard-walkthrough)
7. [Part 7: Comprehensive 20-Question Technical Q&A Bank](#part-7-comprehensive-20-question-technical-qa-bank)
8. [Part 8: Pre-Presentation Readiness Checklist](#part-8-pre-presentation-readiness-checklist)

---

## Part 1: Executive Elevator Pitch & 3-Speaker Delivery Plan

### 1.1 The 60-Second Project Elevator Pitch
> *"In decentralized over-the-counter (OTC) cryptocurrency markets, traders exchange assets directly with pseudonymous peers without a central clearinghouse or escrow guarantee, creating severe counterparty default and fraud risks. In this project, we model two real-world Web-of-Trust networks from Stanford SNAP—Bitcoin Alpha and Bitcoin OTC, totaling 59,778 timestamped ratings across 9,207 unique traders—and scale our pipeline to a 25,000-node enterprise benchmark. First, we prove that explicit distrust links (~9.3% of edges) must be purged before link prediction because two honest traders who both distrust the same scammer form a balanced $[+,-,-]$ triad ($T_2$), so keeping negative edges would trick Common Neighbors into recommending scammers. Second, we analyze the network's macro-topology, confirming a heavy-tailed scale-free degree distribution ($\gamma = 2.14$), strong disassortativity ($r = -0.1409$), a 19-core liquidity backbone of 108 anchor brokers, and 91.2% classic structural balance ($Z = +52.4$ vs. 1,000 sign-shuffled null networks). Third, using a connectivity-preserving 80/20 Minimum Spanning Tree split, a strict chronological 2010–2013 vs. 2014–2016 temporal split, and a 64-dimensional Truncated SVD spectral embedding comparison, we benchmark five topological link predictors and build a Normalized Rank Ensemble ($0.30\text{AA} + 0.25\text{RA} + 0.25\text{Jac} + 0.10\text{CN} + 0.10\text{PA}$). Our Ensemble achieves the #1 F1-score (0.8903), 0.9402 ROC-AUC, 100% Precision@50, and #1 overall AUC (0.7544) on the 25,000-node benchmark, while providing transparent 2-hop intermediary explanations in our live interactive D3.js explorer."*

### 1.2 Three-Speaker Role Division & Timing Plan (15–18 Minutes Total)

| Speaker | Assigned Slides | Core Domain Responsibility | Target Time | Hand-off Cue to Next Speaker |
| :--- | :---: | :--- | :---: | :--- |
| **Speaker 1** | **Slides 1 – 5** | **Problem, Datasets, Sign Filtering & Topology:** Counterparty risk in P2P crypto, SNAP Bitcoin Alpha/OTC + 25k synthetic scale, why negative edges are filtered (Heider Balance Theory), scale-free power law ($\gamma=2.14$), disassortativity ($r=-0.1409$), 19-core decomposition, and $Z$-score null-model validation. | **5.0 – 6.0 min** (~1 min/slide) | *"Now that we have established the scale-free, disassortative, and structurally balanced topology of the trust graph, I will hand over to Speaker 2 to explain our MST evaluation protocol and the mathematical mechanics of our link prediction heuristics."* |
| **Speaker 2** | **Slides 6 – 9** | **Methodology, Heuristics & Ensemble Architecture:** Connectivity-preserving 80/20 MST split, distance $\ge 2$ negative sampling, chronological 2010–2013 $\rightarrow$ 2014–2016 backtest, local neighborhood heuristics (CN, Jaccard, AA, RA), Preferential Attachment (PA), Normalized Rank Ensemble weights, and SVD-64 spectral comparison. | **5.0 – 6.0 min** (~1.25 min/slide) | *"Having formulated our six topological predictors, our weighted rank ensemble, and our SVD spectral baseline, I now pass the floor to Speaker 3 to present our empirical evaluation results, live recommendation case study, and system architecture."* |
| **Speaker 3** | **Slides 10 – 14** | **Empirical Results, Temporal/Scale Benchmarks & System Demo:** ROC-AUC & PR curves, Precision@K ($K=10\dots 100$), temporal and 25k enterprise scoreboards, Trader #1 Top-20 recommendations ego-network, live D3.js dashboard walkthrough, and overall architectural conclusions. | **5.0 – 6.0 min** (~1 min/slide + live demo) | *"That concludes our end-to-end presentation. We now welcome your questions and can demonstrate any trader query live in our interactive explorer."* |

---

## Part 2: Complete Slide-by-Slide Verbatim Scripts & Visual Cues (Slides 1–14)

### SPEAKER 1: Domain Motivation, Data Engineering & Network Topology (Slides 1–5)

---

#### Slide 1: Title Slide — Trust & Reputation Link Prediction in Decentralized Crypto Networks
- **On-Screen Layout:** Title banner, 4 KPI callout cards at bottom (`59,778` Empirical Ratings, `25,000` Enterprise Scale Nodes, `0.9505` Peak ROC-AUC, `1.000` Precision@50), and 3-Speaker roadmap badge.
- **Where to Point:** Sweep across the 4 metric badges at the bottom of the slide to anchor the scale and empirical rigor immediately.
- **Verbatim Speaking Script:**
  > *"Good morning/afternoon everyone. Today our team is presenting our Social Network Analysis project: Trust and Reputation Link Prediction in Decentralized Cryptocurrency Trading Networks. In peer-to-peer Bitcoin exchanges, traders transact without a central clearinghouse, relying entirely on a signed Web-of-Trust graph. Across our study, we analyze 59,778 real-world timestamped trust ratings from Stanford SNAP's Bitcoin Alpha and Bitcoin OTC datasets, scale our evaluation up to a 25,000-node enterprise benchmark, achieve up to 0.9505 ROC-AUC and 0.8903 F1-score, and deliver 100% Precision@50 for counterparty recommendations. Our presentation is organized into three parts: I will cover the problem formulation, signed edge filtering, and network topology; Speaker 2 will cover our MST evaluation design and link prediction algorithms; and Speaker 3 will present our quantitative evaluations, temporal and enterprise benchmarks, and live interactive recommendation engine."*
- **Key Takeaway to Emphasize:** We combine rigorous real-world SNAP datasets with a 25,000-node enterprise stress test and an explainable recommendation UI.

---

#### Slide 2: Problem Statement & Dataset Architecture
- **On-Screen Layout:** Left card details *Counterparty Risk in P2P Crypto Markets* and the 5-step end-to-end pipeline; Right card displays the **Dataset Summary Table** (`Bitcoin Alpha`, `Bitcoin OTC`, `Unified Empirical`, `Enterprise Scale`) and the **Key Architectural Design Choice** box at bottom-right.
- **Where to Point:** Point first to the left card's problem statement, then trace across the rows of the Dataset Summary Table on the right.
- **Verbatim Speaking Script:**
  > *"Let's begin with the core domain problem. On decentralized over-the-counter exchanges like Bitcoin Alpha and Bitcoin OTC, users trade cryptocurrency directly with pseudonymous peers. Because blockchain transactions are irreversible and there is no central escrow, a trader faces two opposing hazards: trading with an unknown counterparty risks outright fraud, while trading only with existing contacts severely restricts market liquidity. Therefore, we formulate counterparty discovery as a topological link prediction problem: given an existing network of verified positive trust ties $G=(V, E^+)$, can we rank unobserved pairs $(u,v) \notin E^+$ by their likelihood of forming a safe, mutually trustworthy trading relationship?*
  >
  > *Looking at the table on the right, we evaluate four network regimes. First, Bitcoin Alpha contains 3,783 traders and 24,186 directed ratings. Second, Bitcoin OTC contains 5,887 traders and 35,592 directed ratings. Third, our Unified Empirical Graph merges both platforms—offsetting OTC node IDs by +100,000 to preserve distinct platform identities—resulting in 9,207 unique traders and 31,050 undirected positive trust edges. Fourth, to prove enterprise scalability, we generate a 25,000-node, 135,857-edge Holme-Kim power-law cluster graph calibrated to match the empirical degree exponent and triangle clustering."*
- **Key Takeaway to Emphasize:** Link prediction solves the cold-start liquidity vs. fraud trade-off in decentralized markets across both real SNAP networks ($9,207$ nodes) and enterprise scale ($25,000$ nodes).

---

#### Slide 3: Edge Sign Distribution & Why Negative Links Are Filtered
- **On-Screen Layout:** Left card shows `edge_sign_distribution.png` (bar chart of positive vs. negative ties + rating histogram); Right card explains **Signed Graph Collapse & Triad Pollution** with the mathematical derivation.
- **Where to Point:** Point to the red negative bars on the left chart (`9.32%` in Alpha, `10.35%` in OTC), then point to the $[+,-,-]$ triad explanation on the right card.
- **Verbatim Speaking Script:**
  > *"Before running any link prediction algorithm, we must address a critical methodological question: what do we do with negative distrust ratings? Raw ratings in Bitcoin Alpha and OTC range from $-10$ (total scammer) to $+10$ (complete trust). As shown in the left chart, after collapsing bidirectional ratings between any pair $(u,v)$ via arithmetic mean $\bar{w}(u,v)$, 90.68% of collapsed ties in Bitcoin Alpha (12,769 edges) are strictly positive ($\bar{w} > 0$), while 9.32% (1,312 edges) are negative ($\bar{w} < 0$). Similarly, Bitcoin OTC has 89.65% positive ties.*
  >
  > *Why must we purge those ~9–10% negative edges before computing topological link predictors? Look at the right panel. Under Heider's Structural Balance Theory, if two honest traders $u$ and $v$ both get defrauded by the same scammer $z$, they both issue negative ratings: $e(u,z) = -1$ and $e(v,z) = -1$. If an unsigned algorithm like Common Neighbors, Adamic-Adar, or Resource Allocation is run on the raw graph without removing negative edges, it treats scammer $z$ as a valid shared neighbor! Worse still, if trader $u$ trusts honest broker $z$ ($+1$) and broker $z$ flags scammer $s$ ($-1$), keeping the negative edge creates a 2-hop path $u \to z \to s$, causing the recommender to suggest the scammer $s$ to honest trader $u$! By strictly filtering $E^+ = \{e \in E : \bar{w}(e) > 0\}$, every shared neighbor $z \in \Gamma(u) \cap \Gamma(v)$ is guaranteed to be a mutually trusted voucher."*
- **Key Takeaway to Emphasize:** Filtering negative edges prevents **Triad Pollution**, ensuring 2-hop paths represent genuine transitive trust rather than shared victimhood or scammer exposure.

---

#### Slide 4: Macro-Topology: Scale-Free Power-Law, Assortativity & K-Core
- **On-Screen Layout:** Left column stacks `degree_distribution_powerlaw.png` (top) and `degree_assortativity_mixing.png` (bottom); Right card presents **Three Fundamental Topological Signatures** ($P(k) \sim k^{-2.14}$, $r = -0.1409$, and $k_{\max} = 19$ core nucleus).
- **Where to Point:** Point to the red power-law fit line on the top-left log-log plot, the downward slope on the bottom-left assortativity plot, and the three numbered bullets on the right.
- **Verbatim Speaking Script:**
  > *"Once we extract the verified positive trust network of 9,207 nodes and 31,050 edges, we uncover three fundamental topological signatures that directly govern how link prediction algorithms behave.*
  >
  > *First, looking at the top-left log-log plot, the degree distribution follows a heavy-tailed scale-free power law $P(k) \sim k^{-\gamma}$ with maximum-likelihood exponent $\gamma = 2.14 \pm 0.08$ (and $\gamma = 2.10$ on our 25,000-node network). Over 70% of traders have fewer than 5 links, whereas top OTC liquidity brokers reach degrees of 785 (Trader #100035) and 507 (Trader #1). Because $\gamma \in (2, 3)$, the second moment $\langle k^2 \rangle$ diverges, meaning hubs act as massive topological magnets.*
  >
  > *Second, looking at the bottom-left plot, the network is strongly disassortative with Newman degree assortativity $r = -0.1409$. High-degree OTC market makers predominantly connect to low-degree retail traders rather than only trading with other hubs—forming a core-periphery star topology.*
  >
  > *Third, Iterative K-Core Decomposition reveals a maximal degeneracy of $k_{\max} = 19$ containing exactly 108 elite traders (and $k_{\max} = 24$ with 312 hubs in the 25k graph). Every trader in this 19-core maintains at least 19 mutually verified trust links with other members of the same core, forming the high-liquidity clearinghouse of the entire ecosystem. Meanwhile, Louvain community detection finds modularity $Q = 0.6401$, reflecting regional trading clusters."*
- **Key Takeaway to Emphasize:** The combination of scale-free hubs ($\gamma = 2.14$) and disassortative mixing ($r = -0.1409$) explains why Preferential Attachment is a strong global baseline, while high clustering ($C = 0.1720$, $47\times$ random Erdős-Rényi) enables local triadic closure.

---

#### Slide 5: Structural Balance Theory & Null-Model Statistical Proof
- **On-Screen Layout:** Left column stacks `structural_balance_triads.png` (top) and `balance_null_model.png` (bottom); Right card presents **Heider's Balance Theory & Z-Score Validation** with exact triad counts and formulas.
- **Where to Point:** Point to the green bars ($T_3$ and $T_2$) in the top-left triad chart, then point to the red vertical line at $Z = +52.4$ far to the right of the grey null histogram on the bottom-left chart.
- **Verbatim Speaking Script:**
  > *"To mathematically justify using triangle-closing heuristics ($CN, AA, RA, Jaccard$), we test whether the Bitcoin trust network obeys Heider's Structural Balance Theory across all 61,515 undirected signed triads.*
  >
  > *In the top-left chart, we classify every triangle into four canonical types: $T_3$ ($[+,+,+]$, mutual trust), $T_2$ ($[+,-,-]$, two honest traders mutually distrusting a common scammer), $T_1$ ($[+,+,-]$, a broker trusting two peers who distrust each other—structural tension!), and $T_0$ ($[-,-,-]$, mutual hostility). Across the unified network, 74.8% of triads are $T_3$ (46,013 triangles) and 16.4% are $T_2$ (10,088 triangles). Summing $T_3 + T_2$ gives 91.2% Classic Structural Balance ($56,101 / 61,515$), and adding $T_0$ (1.0%) yields 92.2% Weak Balance (Davis's clusterability). Only 7.8% of triangles reside in the conflicted $T_1$ state.*
  >
  > *However, a skeptic might ask: since ~90% of edges are positive, wouldn't random chance alone produce ~90% balanced triangles? To prove this is not an artifact of base rates, look at the bottom-left plot. We fix the exact graph topology and randomly permute the edge signs 1,000 times, preserving the exact positive/negative ratio. The null distribution centers at $\mu_{\text{null}} = 79.4\%$ with $\sigma_{\text{null}} = 0.22\%$. Our observed balance of 91.2% achieves a standardized score of $Z = +52.4$ ($p < 10^{-100}$). This proves that transitive trust closure is a statistically ironclad social law in crypto markets. I now pass to Speaker 2 to explain our methodology."*
- **Key Takeaway to Emphasize:** The $Z = +52.4$ null-model test proves beyond any statistical doubt that triangle closure is an active behavioral mechanism, not a byproduct of positive edge density.

---

### SPEAKER 2: Evaluation Protocol, Heuristics & Ensemble Architecture (Slides 6–9)

---

#### Slide 6: Leakage-Free Train/Test Splitting: MST + Temporal Backtest
- **On-Screen Layout:** Two equal-width cards: Left card details **Protocol A: Connectivity-Preserving 80/20 MST Split**; Right card details **Protocol B: Chronological Temporal Backtest (2010–2016)**.
- **Where to Point:** Point to the 4-step pipeline on the left card (`9,119` GCC nodes, `9,118` MST backbone edges, `14,590` train edges, `3,647` test positives + `3,647` distance $\ge 2$ negatives), then point to the chronological cutoff on the right card.
- **Verbatim Speaking Script:**
  > *"Thank you, Speaker 1. A common pitfall in link prediction research is naive random edge removal: if you randomly delete 20% of edges from a sparse power-law graph ($\gamma = 2.14$), you sever degree-1 and degree-2 leaf nodes from the Giant Connected Component, creating isolated vertices where path-based scores trivially collapse to zero.*
  >
  > *As shown in the left card (Protocol A), we solve this using a Connectivity-Preserving 80/20 Minimum Spanning Tree Split. First, we extract the Giant Connected Component of $G_{\text{train}} \cup G_{\text{test}}$ containing 9,119 nodes and 18,237 positive edges. Second, we extract a Minimum Spanning Tree of $N - 1 = 9,118$ edges and lock those backbone edges into the training set so the graph can never shatter. Third, from the remaining 9,119 non-tree cycle edges, we randomly hold out $3,647$ edges (exactly 20.0% of total edges) as positive test links $E_{\text{test}}^+$, leaving $14,590$ training edges (80.0%) over the exact same 9,119 connected nodes. Fourth, we sample an equal number ($3,647$) of true non-edges $(u,v) \notin E^+$ restricted to graph distance $d_{G_{\text{train}}}(u,v) \ge 2$, yielding a balanced 7,294-pair benchmark with zero data leakage.*
  >
  > *Furthermore, because static splits ignore edge creation timestamps, our right card (Protocol B) implements a strict Chronological Temporal Backtest: we train strictly on historical trust links formed during 2010–2013 and predict future links formed during 2014–2016 among active cohort nodes."*
- **Key Takeaway to Emphasize:** Locking the MST guarantees 100% node reachability in $G_{\text{train}}$, while Protocol B proves our models predict future links forward in time without temporal leakage.

---

#### Slide 7: Local Neighborhood Heuristics: CN, Jaccard, AA & RA
- **On-Screen Layout:** Four quadrant cards covering **1. Common Neighbors (CN)**, **2. Jaccard Coefficient (JC)**, **3. Adamic-Adar Index (AA)**, and **4. Resource Allocation (RA)** with exact formulas, complexities, and empirical insights.
- **Where to Point:** Walk through the 4 cards in a Z-pattern (top-left CN $\rightarrow$ top-right Jaccard $\rightarrow$ bottom-left AA $\rightarrow$ bottom-right RA), pointing specifically to the denominators.
- **Verbatim Speaking Script:**
  > *"Now let's examine the four local triadic-closure heuristics we benchmark on $G_{\text{train}}$, where $\Gamma(u)$ denotes the set of trusted neighbors of trader $u$.*
  >
  > *Top-left is Common Neighbors: $CN(u,v) = |\Gamma(u) \cap \Gamma(v)|$. It simply counts how many mutually trusted intermediaries $z$ connect $u$ and $v$. While fast ($O(\bar{k})$ per pair) and achieving 0.8335 AUC, it treats all intermediaries equally—whether $z$ is a giant public exchange with 700 links or a specialized private broker with 4 links.*
  >
  > *Top-right is the Jaccard Coefficient: $JC(u,v) = \frac{|\Gamma(u) \cap \Gamma(v)|}{|\Gamma(u) \cup \Gamma(v)|}$. It normalizes the shared overlap by the union size. Crucially, notice our empirical finding: in a disassortative network ($r = -0.1409$), when an elite OTC market maker (degree 500) transacts with a retail trader (degree 5), the denominator $|\Gamma(u) \cup \Gamma(v)| \approx 505$ crushes the Jaccard score toward zero! This causes Jaccard's Precision@10 to drop to 0.200.*
  >
  > *To properly discount high-degree hubs without penalizing the endpoints $u$ and $v$, look at the bottom two cards. Bottom-left is Adamic-Adar: $AA(u,v) = \sum_{z \in \Gamma(u)\cap\Gamma(v)} \frac{1}{\ln|\Gamma(z)|}$, which applies logarithmic decay to hub intermediaries. Bottom-right is Resource Allocation: $RA(u,v) = \sum_{z \in \Gamma(u)\cap\Gamma(v)} \frac{1}{|\Gamma(z)|}$, derived from physical network flow where each intermediary $z$ divides one unit of trust capacity equally among its $|\Gamma(z)|$ neighbors. Both AA and RA achieve 0.8366 AUC and 1.000 Precision@100."*
- **Key Takeaway to Emphasize:** AA ($\frac{1}{\ln k_z}$) and RA ($\frac{1}{k_z}$) discount noisy mega-hub intermediaries $z$, whereas Jaccard mistakenly penalizes the union degree of the endpoints $(u,v)$ themselves.

---

#### Slide 8: Global Scale-Free Baseline (PA) & Normalized Rank Ensemble
- **On-Screen Layout:** Left card details **5. Preferential Attachment (PA)** (`0.9505` AUC, `0.9522` AP) and why it excels globally vs. its structural blind spot; Right card details **6. Normalized Rank Ensemble Architecture** (`0.8903` #1 F1, `0.9402` AUC, `0.7544` #1 Enterprise AUC).
- **Where to Point:** Point to the $PA(u,v) = |\Gamma(u)|\cdot|\Gamma(v)|$ formula on the left card, then point to the explicit convex combination equation on the right card.
- **Verbatim Speaking Script:**
  > *"While CN, Jaccard, AA, and RA are local 2-hop neighborhood metrics, they share one structural limitation: if two traders $u$ and $v$ sit at graph distance $d(u,v) \ge 3$, their shared neighborhood $\Gamma(u) \cap \Gamma(v)$ is empty, so all four local heuristics output exactly zero.*
  >
  > *That brings us to our fifth predictor on the left card: Preferential Attachment, $PA(u,v) = |\Gamma(u)| \cdot |\Gamma(v)|$, rooted in the Barabási-Albert rich-get-richer model. Because our network has $\gamma = 2.14$, hub brokers participate in the vast majority of cross-cluster edges, giving PA the highest single-metric ROC-AUC of 0.9505 (and 0.8285 in temporal backtesting). However, PA is completely blind to local community structure: it assigns a massive score to any two hubs in totally unrelated regional markets even if they share zero mutual acquaintances!*
  >
  > *To unite local triadic precision with global scale-free recall, look at the right card: our Normalized Rank Ensemble. Because raw scores have incompatible scales—Jaccard lies in $[0,1]$ while PA reaches $3.9 \times 10^5$—direct linear addition would let PA drown out every other signal. Instead, we map each heuristic $m$ to its empirical percentile rank $\tilde{r}_m(u,v) \in [0,1]$ and compute the weighted combination:*
  > $$\text{Score}_{\text{Ens}}(u,v) = 0.30\,\tilde{r}_{AA} + 0.25\,\tilde{r}_{RA} + 0.25\,\tilde{r}_{Jac} + 0.10\,\tilde{r}_{CN} + 0.10\,\tilde{r}_{PA}$$
  > *Here, 90% of the weight anchors recommendations in verified 2-hop shared neighbors (led by AA and RA at 55%), while the 10% PA prior smoothly breaks ties and ranks long-range pairs. This achieves the #1 overall F1-score of 0.8903, 0.9402 AUC, 1.000 Precision@50, and #1 overall AUC (0.7544) on the 25,000-node enterprise benchmark."*
- **Key Takeaway to Emphasize:** Rank normalization resolves scale incompatibility ($[0,1]$ vs. $10^5$), and our $90\%$ local / $10\%$ global weighting yields the #1 F1-score ($0.8903$) and #1 Enterprise AUC ($0.7544$).

---

#### Slide 9: Representation Learning vs. Topological Heuristics (SVD-64)
- **On-Screen Layout:** Left card presents **Spectral Node Embeddings (Truncated SVD-64)** math, test metrics, and three reasons why topological heuristics win; Right card displays `topological_vs_embedding_comparison.png` (side-by-side bar chart of ROC-AUC, AP, F1, and P@100).
- **Where to Point:** Point to the Hadamard product formula $\mathbf{h}(u,v) = \mathbf{z}_u \odot \mathbf{z}_v$ on the left card, then point to the F1 (`0.8903` vs `0.4522`) and P@100 (`1.000` vs `0.580`) bars on the right chart.
- **Verbatim Speaking Script:**
  > *"A natural modern question is: how do our explicit topological heuristics compare against learned low-dimensional node embeddings? To test this rigorously, we implemented a 64-dimensional Spectral Embedding pipeline on $G_{\text{train}}$ using randomized Truncated SVD ($A_{\text{train}} \approx U_{64} \Sigma_{64} V_{64}^\top$, which is the closed-form linear objective of DeepWalk/Node2Vec matrix factorization). Each trader $u$ is embedded as $\mathbf{z}_u = U_{64}(u,:) \Sigma_{64}^{1/2} \in \mathbb{R}^{64}$, candidate pairs are represented via the Hadamard product $\mathbf{h}(u,v) = \mathbf{z}_u \odot \mathbf{z}_v$, and an $L_2$-regularized Logistic Regression classifier is trained strictly on training pairs.*
  >
  > *Looking at the chart on the right, SVD-64 + Logistic Regression achieves a competitive 0.9175 ROC-AUC and 0.9377 Average Precision. However, our Topological Ensemble and Preferential Attachment decisively outperform SVD-64 across every metric: Ensemble achieves 0.9402 AUC vs. 0.9175, nearly double the F1-score (0.8903 vs. 0.4522), and 0.800–1.000 Precision@100 vs. 0.580 for SVD-64.*
  >
  > *Why do explicit heuristics win here? First, rank-64 spectral truncation smooths out exact 2-hop triadic wedges in ultra-sparse regions ($\bar{k}=6.74$). Second, SVD runs 4.3× slower (1.80s vs. 0.42s). Third, and most importantly for financial compliance, a 64-float vector is a black box, whereas our Ensemble explicitly names the trusted intermediary $z$ vouching for the trade. I now hand over to Speaker 3 for our empirical evaluation and live system demo."*
- **Key Takeaway to Emphasize:** Topological heuristics beat SVD-64 spectral embeddings in AUC ($0.9402$ vs. $0.9175$), F1 ($0.8903$ vs. $0.4522$), runtime ($4.3\times$ faster), and auditability.

---

### SPEAKER 3: Empirical Results, Benchmarks & System Demo (Slides 10–14)

---

#### Slide 10: Comprehensive Evaluation: ROC-AUC & Precision-Recall Curves
- **On-Screen Layout:** Left panel shows `link_prediction_roc_curves.png` (ROC curves); Right panel shows `link_prediction_pr_curves.png` (PR curves); Bottom banner displays the full **Empirical Evaluation Summary Table** across all 7 models.
- **Where to Point:** Point to the top two curves (PA and Ensemble) on both plots, then highlight the **Ensemble** and **PA** rows in the bottom summary table.
- **Verbatim Speaking Script:**
  > *"Thank you, Speaker 2. Let's examine our primary quantitative evaluation on the 7,294-pair empirical test set ($3,647$ held-out positive trust ties vs. $3,647$ distance $\ge 2$ negative non-edges).*
  >
  > *Looking at the ROC curves on the left and Precision-Recall curves on the right, we observe three distinct performance tiers summarized in the bottom table:*
  > - *Tier 1 (Global + Hybrid Leaders): Preferential Attachment achieves the highest global ROC-AUC at 0.9505 and Average Precision at 0.9522 because it scores all 7,294 pairs including long-range cross-cluster links ($d \ge 3$). Close behind in AUC (0.9402) is our Normalized Rank Ensemble, which captures the #1 overall F1-score at 0.8903—beating PA (0.8864) and outperforming individual local heuristics (0.6667) by over +22.3 percentage points.*
  > - *Tier 2 (Learned Spectral Baseline): SVD-64 Hadamard + Logistic Regression reaches 0.9175 AUC and 0.9377 AP, but suffers from threshold sensitivity (F1 = 0.4522).*
  > - *Tier 3 (Pure 2-Hop Local Heuristics): Resource Allocation (0.8366 AUC, 0.8411 AP) and Adamic-Adar (0.8366 AUC, 0.8409 AP) outperform unweighted Common Neighbors (0.8335 AUC, 0.8304 AP) and Jaccard (0.8161 AUC, 0.7539 AP), confirming that hub-penalized triangle closure is superior to naive overlap counting."*
- **Key Takeaway to Emphasize:** PA leads global AUC ($0.9505$) due to long-range coverage, while the Normalized Rank Ensemble achieves the #1 F1-score ($0.8903$) by uniting local precision with global recall.

---

#### Slide 11: Top-K Recommendation Quality, Temporal Backtest & 25k Scale
- **On-Screen Layout:** Top-left shows `link_prediction_precision_at_k.png`; Bottom-left shows `temporal_link_prediction_comparison.png`; Right card presents **Three Multi-Regime Validation Findings** with the full cross-regime comparison table (`Empirical`, `Temporal`, `25k Enterprise`).
- **Where to Point:** Point to the flat `1.000` line across $K=10, 20, 50$ on the top-left Precision@K chart (and Jaccard's dip at the bottom), then point to the 3-regime table on the right card.
- **Verbatim Speaking Script:**
  > *"In a production OTC exchange, a trader does not inspect all 7,294 candidate pairs—they only look at the Top-K recommended counterparties on their dashboard. Therefore, Top-K ranking precision is our most critical operational metric.*
  >
  > *Looking at the top-left Precision@K chart, Common Neighbors, Adamic-Adar, Resource Allocation, and Preferential Attachment all achieve a perfect Precision@100 of 1.000, and our Ensemble achieves a perfect 1.000 at K=10, K=20, and K=50 (and 0.800 at K=100). By contrast, look at the purple curve at the bottom: Jaccard collapses to P@10 = 0.200 and P@20 = 0.150 because its union denominator penalizes high-degree hubs.*
  >
  > *Now look at the bottom-left chart and the multi-regime table on the right. First, under our strict Chronological Temporal Backtest (training on 2010–2013 to predict 2014–2016), despite substantial user churn over 6 years, PA achieves 0.8285 AUC and our Ensemble achieves 0.8150 AUC, 0.7581 F1, and 1.000 Precision@20. Second, on our 25,000-node, 135,857-edge Enterprise Benchmark, where increased triangle clustering makes pure degree products noisier (PA drops to 0.6926 AUC), our Normalized Rank Ensemble rises to #1 overall across every metric: 0.7544 ROC-AUC, 0.8004 Average Precision, 0.6907 F1, and 1.000 Precision@100!"*
- **Key Takeaway to Emphasize:** The Normalized Rank Ensemble is the most resilient model across all three evaluation regimes—achieving $1.000$ P@50 empirically, $1.000$ P@20 temporally, and #1 overall AUC ($0.7544$) at $25,000$-node enterprise scale.

---

#### Slide 12: Case Study: Explainable Top-20 Recommendations for Trader #1
- **On-Screen Layout:** Left panel shows `recommended_ego_network.png` (2-hop ego subgraph around Trader #1 with solid green predicted links to recommended peers); Right card shows the **Top-8 Recommended Counterparties Table for Trader #1** and the **Mathematical Traceability** box.
- **Where to Point:** Point to central blue node **Trader #1** on the left graph, trace the dashed orange links to grey mutual intermediaries, and follow the solid green predicted edges to green recommended nodes (e.g., `#72`, `#3`, `#173`). Then point to the worked formula for Trader #1 $\rightarrow$ Trader #3 at the bottom-right.
- **Verbatim Speaking Script:**
  > *"To show how these mathematical scores translate into actionable, human-verifiable decision support, let's examine our Top-20 recommendation case study for Anchor Trader #1 ($k=507$, PageRank $= 0.0110$, 19-core liquidity broker).*
  >
  > *In the left visualization, the blue central node is Trader #1, grey nodes are existing trusted intermediaries $z \in \Gamma(1)$, and green nodes are top unseen candidate counterparties $v \notin \Gamma(1)$ connected by solid green predicted links. Looking at the table on the right, our #1 recommendation is Trader #72 (Ensemble = 0.9964), backed by 66 mutually trusted intermediaries ($AA = 17.56$, $RA = 1.982$, $JC = 0.1185$). Close behind at Rank #2 is Trader #3 (Ensemble = 0.9951), supported by 65 shared intermediaries ($AA = 17.46$, $RA = 2.043$, $JC = 0.1161$).*
  >
  > *Notice an insightful comparison between Rank #1 (Trader #72) and Rank #2 (Trader #3): although Trader #72 has one more common neighbor (66 vs. 65) and slightly higher Adamic-Adar (17.56 vs. 17.46), Trader #3 achieves a higher Resource Allocation score (2.043 vs. 1.982) because its shared intermediaries have smaller average degrees ($\frac{1}{k_z}$ vs. $\frac{1}{\ln k_z}$). Most importantly, instead of showing an opaque probability, our system displays the exact 2-hop trust chain—for example, `Trader #1` $\leftrightarrow$ `Broker #7` ($k=112$) $\leftrightarrow$ `Candidate #3`—giving the user concrete social proof before executing an OTC trade."*
- **Key Takeaway to Emphasize:** Every recommendation is backed by explicit 2-hop intermediary chains ($1 \leftrightarrow z \leftrightarrow v$), turning link prediction into an auditable counterparty due-diligence tool.

---

#### Slide 13: Interactive System Architecture & Reproducible Deliverables
- **On-Screen Layout:** Left card details the **Interactive Web Application (`localhost:5000` / Standalone HTML)** across its 4 views and the **2-Hop Trust Chain Provenance Modal**; Right card lists the **End-to-End Reproducible Engineering Stack** (`run_link_prediction_pipeline.py`, `app.py`, `test_pipeline.py`, etc.).
- **Where to Point:** Point to the 4 numbered view modes on the left card, then point to the automated test suite (`pytest tests/test_pipeline.py`) on the right card.
- **Verbatim Speaking Script:**
  > *"Beyond static batch evaluation, we engineered a full-stack interactive Counterparty Recommendation & Graph Explorer available both via a live Flask REST API (`http://localhost:5000`) and as a zero-dependency standalone HTML application (`outputs/interactive_recommendation_demo.html`).*
  >
  > *As outlined on the left card, the dashboard provides four synchronized analytical workspaces: (1) an Interactive D3.js Force-Directed Ego-Network where users can select any top broker, toggle between Ensemble, AA, RA, CN, Jaccard, and PA rankings, and adjust Top-K density; (2) a Multi-Heuristic Score Inspector Table with real-time search and CSV export; (3) an Interactive Benchmark Gallery comparing ROC, PR, Temporal, SVD-64, and 25k Enterprise metrics; and (4) an Interactive Mathematical Sandbox where users can click any node or link to open our 2-Hop Trust Chain Provenance Modal, inspecting the exact intermediary breakdown $\frac{1}{\ln k_z}$ and $\frac{1}{k_z}$ live.*
  >
  > *On the right card, our entire repository is 100% reproducible via a single `make all` command and verified by an automated `pytest` test suite checking positive edge filtering, MST connectivity preservation, heuristic formulas, and output schema integrity."*
- **Key Takeaway to Emphasize:** Our deliverables combine a production-ready interactive D3.js/Flask decision-support system with a fully tested, one-command reproducible pipeline.

---

#### Slide 14: Conclusion, Architectural Synthesis & Future Directions
- **On-Screen Layout:** Two balanced cards: Left card summarizes **Core Empirical & Theoretical Takeaways** (4 numbered blocks); Right card details **Operational Deployment, Limitations & Future Scope** (4 blocks) + bottom summary banner.
- **Where to Point:** Summarize the 4 theoretical/empirical takeaways on the left, then highlight the future extensions (Dynamic Temporal GNNs, Sybil resistance) on the right.
- **Verbatim Speaking Script:**
  > *"To conclude our presentation on Slide 14, let's synthesize our four primary contributions on the left panel:*
  > 1. *Signed Preprocessing Prevents Triad Pollution: Filtering explicit distrust edges ($\bar{w} \le 0$) eliminates $[+,-,-]$ scammer-victim triads and validates 91.2% classic structural balance ($Z = +52.4$).*
  > 2. *Scale-Free Disassortative Topology Shapes Predictor Behavior: Heavy-tailed hubs ($\gamma = 2.14$) and disassortative mixing ($r = -0.1409$) explain why PA dominates global recall (0.9505 AUC), why Jaccard fails at Top-K (P@10 = 0.200), and why hub-penalized AA and RA achieve 1.000 P@100.*
  > 3. *Normalized Rank Ensemble Achieves Multi-Regime Dominance: Our rank-normalized ensemble ($0.30\text{AA} + 0.25\text{RA} + 0.25\text{Jac} + 0.10\text{CN} + 0.10\text{PA}$) delivers the #1 F1-score (0.8903), 1.000 P@50, and #1 overall AUC (0.7544) on the 25,000-node enterprise benchmark.*
  > 4. *Superiority Over Black-Box Embeddings: Explicit topological predictors beat 64-D SVD spectral embeddings in accuracy (0.9402 vs. 0.9175 AUC), F1 (0.8903 vs. 0.4522), runtime (4.3× faster), and 2-hop explainability.*
  >
  > *Looking ahead on the right panel, our incremental 2-hop adjacency indexing supports sub-millisecond real-time scoring ($O(\bar{k}^2)$) in decentralized P2P wallets, with natural future extensions to continuous-time Temporal Graph Networks (TGN) and Sybil-resistant collusion detection. Thank you—we are now happy to take your questions and show the live dashboard!"*
- **Key Takeaway to Emphasize:** End on a strong, decisive summary tying network physics ($\gamma=2.14, r=-0.1409, Z=+52.4$) directly to algorithmic design (Rank Ensemble) and practical OTC deployment.

---

## Part 3: Deep-Dive Mathematical & Algorithmic Reference Guide

Every team member should be comfortable writing or explaining these formulas on a whiteboard.

### 3.1 Master Formula & Complexity Table

Let $G_{\text{train}} = (V, E_{\text{train}}^+)$ be the undirected positive training graph, and let $\Gamma(u) = \{z \in V : (u,z) \in E_{\text{train}}^+\}$ denote the set of trusted neighbors of trader $u$, with degree $k_u = |\Gamma(u)|$.

| Predictor | Exact Mathematical Formula | Per-Pair Time Complexity | Score Range (Empirical) | Core Mechanism & Role in Ensemble |
| :--- | :--- | :---: | :---: | :--- |
| **1. Common Neighbors (CN)** | $$CN(u,v) = \|\Gamma(u) \cap \Gamma(v)\|$$ | $O(k_u + k_v)$ | $[0, 184]$ | Raw count of mutually trusted intermediaries $z$. Fast baseline ($10\%$ Ensemble weight). |
| **2. Jaccard Coefficient (JC)** | $$JC(u,v) = \frac{\|\Gamma(u) \cap \Gamma(v)\|}{\|\Gamma(u) \cup \Gamma(v)\|}$$ | $O(k_u + k_v)$ | $[0.0, 1.0]$ | Proportion of total combined neighborhood shared ($25\%$ Ensemble weight; penalizes hub-retail pairs when used alone). |
| **3. Adamic-Adar Index (AA)** | $$AA(u,v) = \sum_{z \in \Gamma(u) \cap \Gamma(v)} \frac{1}{\ln(\|\Gamma(z)\|)}$$ | $O(k_u + k_v)$ | $[0.0, 48.7]$ | Logarithmic penalty on hub intermediaries $z$. Best overall local discriminator ($30\%$ Ensemble weight — highest share). |
| **4. Resource Allocation (RA)** | $$RA(u,v) = \sum_{z \in \Gamma(u) \cap \Gamma(v)} \frac{1}{\|\Gamma(z)\|}$$ | $O(k_u + k_v)$ | $[0.0, 5.42]$ | Inverse linear penalty $\frac{1}{k_z}$ modeling conserved trust flow capacity ($25\%$ Ensemble weight). |
| **5. Preferential Attachment (PA)** | $$PA(u,v) = \|\Gamma(u)\| \cdot \|\Gamma(v)\|$$ | $O(1)$ lookup | $[1, 398{,}000]$ | Scale-free Barabási-Albert degree product; only heuristic that scores $d(u,v) \ge 3$ pairs ($10\%$ Ensemble tie-breaker). |
| **6. Normalized Rank Ensemble** | $$\text{Ens}(u,v) = \sum_{m} w_m \frac{\text{rank}_m(u,v)-1}{\|\mathcal{C}\|-1}$$ | $O(\|\mathcal{C}\|\log\|\mathcal{C}\|)$ | $[0.0, 1.0]$ | Scale-invariant copula aggregation ($0.30\text{AA} + 0.25\text{RA} + 0.25\text{Jac} + 0.10\text{CN} + 0.10\text{PA}$). |
| **7. Spectral SVD-64 Baseline** | $$A_{\text{train}} \approx U_{64}\Sigma_{64}V_{64}^\top, \quad \mathbf{h}(u,v) = \mathbf{z}_u \odot \mathbf{z}_v$$ | $O(d \cdot \|E\|)$ SVD | $[0.0, 1.0]$ (LogReg prob) | Low-rank global matrix factorization + $L_2$ Logistic Regression classifier. |

---

### 3.2 Step-by-Step Toy Numerical Example (Easy to Write on Whiteboard!)

Suppose we want to compute all 5 heuristic scores for candidate pair $(u, v)$ where:
- Trader $u$ has degree $k_u = |\Gamma(u)| = 10$
- Trader $v$ has degree $k_v = |\Gamma(v)| = 20$
- They share **2 common neighbors**: Intermediary $z_1$ (a niche specialist broker with degree $k_{z_1} = 3$) and Intermediary $z_2$ (a massive public hub with degree $k_{z_2} = 100$).

1. **Common Neighbors ($CN$):**
   $$CN(u,v) = |\{z_1, z_2\}| = \mathbf{2}$$
   *(Notice $z_1$ and $z_2$ contribute $1 + 1 = 2$ equally, ignoring that $z_2$ connects to 100 people.)*
2. **Jaccard Coefficient ($JC$):**
   $$|\Gamma(u) \cup \Gamma(v)| = k_u + k_v - CN(u,v) = 10 + 20 - 2 = 28$$
   $$JC(u,v) = \frac{2}{28} \approx \mathbf{0.0714}$$
3. **Adamic-Adar Index ($AA$):**
   $$AA(u,v) = \frac{1}{\ln(3)} + \frac{1}{\ln(100)} = \frac{1}{1.0986} + \frac{1}{4.6052} = 0.9102 + 0.2171 = \mathbf{1.1273}$$
   *(Specialist $z_1$ contributes $4.2\times$ more weight than mega-hub $z_2$!)*
4. **Resource Allocation Index ($RA$):**
   $$RA(u,v) = \frac{1}{3} + \frac{1}{100} = 0.3333 + 0.0100 = \mathbf{0.3433}$$
   *(Under linear flow splitting, specialist $z_1$ contributes $33.3\times$ more weight than mega-hub $z_2$!)*
5. **Preferential Attachment ($PA$):**
   $$PA(u,v) = k_u \times k_v = 10 \times 20 = \mathbf{200}$$

---

### 3.3 Real Empirical Calculation Trace: Anchor Trader #1 $\rightarrow$ Candidate Trader #3 (Rank #2)

From `outputs/top20_recommendations.csv` on the empirical Bitcoin trust graph:
- **Source Node:** Trader `#1` ($k_1 = 507$, PageRank $= 0.011005$, 19-core broker)
- **Target Candidate:** Trader `#3` ($k_3 = 118$, unseen in $G_{\text{train}}$, i.e., $(1,3) \notin E_{\text{train}}^+$)
- **Common Neighbors ($CN$):** $|\Gamma(1) \cap \Gamma(3)| = \mathbf{65}$ mutually trusted intermediaries.
- **Jaccard ($JC$):** Union size $|\Gamma(1) \cup \Gamma(3)| = 507 + 118 - 65 = 560 \implies JC(1,3) = \frac{65}{560} = \mathbf{0.116071}$.
- **Adamic-Adar ($AA$):** Summing $\frac{1}{\ln k_z}$ across all 65 shared brokers yields $AA(1,3) = \mathbf{17.4601}$.
- **Resource Allocation ($RA$):** Summing $\frac{1}{k_z}$ across all 65 shared brokers yields $RA(1,3) = \mathbf{2.0432}$.
- **Preferential Attachment ($PA$):** $PA(1,3) = 507 \times 118 = \mathbf{59,826}$.
- **Normalized Rank Ensemble Score:**
  $$\text{Score}_{\text{Ens}}(1,3) = 0.30(0.9968) + 0.25(0.9974) + 0.25(0.9912) + 0.10(0.9965) + 0.10(0.9930) = \mathbf{0.995131}$$

---

## Part 4: Complete Metrics, Datasets & Scoreboard Reference Tables

### 4.1 Dataset & Topological Invariants Master Table

| Metric / Property | Bitcoin Alpha | Bitcoin OTC | Unified Empirical Graph | Enterprise Scale Benchmark |
| :--- | :---: | :---: | :---: | :---: |
| **Raw Directed Edge Ratings** | $24,186$ | $35,592$ | $59,778$ | $135,857$ (undirected) |
| **Unique Traders ($|V|$)** | $3,783$ | $5,887$ | $9,207$ | $25,000$ |
| **Collapsed Undirected Ties** | $14,081$ | $17,012$ | $31,093$ | $135,857$ |
| **Positive Trust Ties ($|E^+|, \bar{w}>0$)** | $12,769$ ($90.68\%$) | $15,252$ ($89.65\%$) | $31,050$ (verified union) | $135,857$ ($100\%$) |
| **Negative Distrust Ties ($\bar{w}<0$)** | $1,312$ ($9.32\%$) | $1,760$ ($10.35\%$) | Purged pre-prediction | Purged / Positive-only |
| **Mean Trusted Degree ($\bar{k}$)** | $6.75$ | $5.18$ | $6.74$ | $10.87$ |
| **Maximum Hub Degree ($k_{\max}$)** | $491$ (Trader `#1`) | $785$ (Trader `#100035`) | $785$ (`#100035`) / $507$ (`#1`) | $612$ |
| **Power-Law Degree Exponent ($\gamma$)** | $2.18 \pm 0.09$ | $2.12 \pm 0.07$ | $2.14 \pm 0.08$ | $2.10 \pm 0.05$ |
| **Degree Assortativity ($r$)** | $-0.1685$ | $-0.1521$ | $-0.1409$ | $-0.1124$ |
| **Average Clustering Coefficient ($C$)** | $0.1766$ | $0.1692$ | $0.1720$ ($47\times C_{\text{ER}}$) | $0.1810$ |
| **Louvain Modularity ($Q$)** | $0.5840$ | $0.6190$ | $0.6401$ | $0.5942$ |
| **Maximal Degeneracy ($k_{\max}$-Core)** | $16$-core ($74$ nodes) | $19$-core ($108$ nodes) | $19$-core ($108$ nodes) | $24$-core ($312$ nodes) |
| **Classic Structural Balance ($T_3+T_2$)** | $91.6\%$ | $90.9\%$ | $91.2\%$ ($Z = +52.4$) | $92.2\%$ (Weak Balance) |

---

### 4.2 Complete Multi-Regime Link Prediction Scoreboard

| Predictor / Model | Empirical ROC-AUC | Empirical Avg Prec (AP) | Empirical F1-Score | Empirical P@10 / P@20 / P@50 / P@100 | Temporal Backtest AUC (2010–13 $\rightarrow$ 14–16) | Temporal Backtest P@20 | Enterprise 25k Nodes ROC-AUC | Enterprise 25k Nodes P@100 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Preferential Attachment (PA)** | **0.9505** (#1) | **0.9522** (#1) | 0.8864 | $1.00 / 1.00 / 1.00 / 1.00$ | **0.8285** (#1) | **1.000** | 0.6926 | **1.000** |
| **Normalized Rank Ensemble** | **0.9402** (#2) | 0.9118 | **0.8903** (#1) | $1.00 / 1.00 / 1.00 / 0.80$ | **0.8150** (#2) | **1.000** | **0.7544** (#1) | **1.000** |
| **SVD-64 Spectral + LogReg** | 0.9175 | 0.9377 | 0.4522 | $1.00 / 1.00 / 0.72 / 0.58$ | — | — | — | — |
| **Resource Allocation (RA)** | 0.8366 | 0.8411 | 0.6667 | $1.00 / 1.00 / 1.00 / 1.00$ | 0.7182 | **1.000** | 0.6439 | **1.000** |
| **Adamic-Adar Index (AA)** | 0.8366 | 0.8409 | 0.6667 | $1.00 / 1.00 / 1.00 / 1.00$ | 0.7183 | **1.000** | 0.6439 | **1.000** |
| **Common Neighbors (CN)** | 0.8335 | 0.8304 | 0.6667 | $1.00 / 1.00 / 1.00 / 1.00$ | 0.7156 | **1.000** | 0.6430 | **1.000** |
| **Jaccard Coefficient (JC)** | 0.8161 | 0.7539 | 0.6667 | $0.20 / 0.15 / 0.38 / 0.51$ | 0.6986 | 0.250 | 0.6424 | 0.720 |

---

### 4.3 Top-10 Counterparty Recommendations for Anchor Trader #1 ($k=507$)

| Rank | Candidate Trader ID | Candidate Degree ($k_v$) | Common Neighbors ($CN$) | Jaccard ($JC$) | Adamic-Adar ($AA$) | Resource Allocation ($RA$) | Preferential Attachment ($PA$) | Normalized Rank Ensemble |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **Trader `#72`** | $116$ | $66$ | $0.1185$ | $17.5612$ | $1.9818$ | $58,812$ | **0.9964** |
| **#2** | **Trader `#3`** | $118$ | $65$ | $0.1161$ | $17.4601$ | $2.0432$ | $59,826$ | **0.9951** |
| **#3** | **Trader `#173`** | $83$ | $48$ | $0.0886$ | $12.1645$ | $1.2361$ | $42,081$ | **0.9854** |
| **#4** | **Trader `#57`** | $79$ | $46$ | $0.0852$ | $11.6908$ | $1.1894$ | $40,053$ | **0.9831** |
| **#5** | **Trader `#135`** | $66$ | $40$ | $0.0750$ | $10.0912$ | $1.0125$ | $33,462$ | **0.9768** |
| **#6** | **Trader `#13`** | $122$ | $46$ | $0.0789$ | $11.4502$ | $1.0840$ | $61,854$ | **0.9742** |
| **#7** | **Trader `#58`** | $59$ | $37$ | $0.0700$ | $9.3140$ | $0.9412$ | $29,913$ | **0.9715** |
| **#8** | **Trader `#246`** | $54$ | $35$ | $0.0665$ | $8.8415$ | $0.8920$ | $27,378$ | **0.9689** |
| **#9** | **Trader `#154`** | $61$ | $36$ | $0.0677$ | $9.0211$ | $0.8814$ | $30,927$ | **0.9671** |
| **#10** | **Trader `#89`** | $72$ | $38$ | $0.0702$ | $9.4105$ | $0.8750$ | $36,504$ | **0.9658** |

---

## Part 5: Visual Guide to Explaining Every Figure & Chart

If an evaluator points to any figure in the slides or report and asks *"Walk me through what this plot shows"*, use this quick reference:

1. **`edge_sign_distribution.png` (Slide 3 / Report Fig. 1a):**
   - **Left Subplot:** Grouped bar chart comparing Positive Trust ($\bar{w}>0$, green) vs. Negative Distrust ($\bar{w}<0$, red) across Bitcoin Alpha ($90.68\%$ vs. $9.32\%$) and Bitcoin OTC ($89.65\%$ vs. $10.35\%$).
   - **Right Subplot:** Histogram of raw rating weights from $-10$ to $+10$. Shows a tall spike at $+1$ to $+3$ (routine successful trades), a secondary cluster at $+10$ (long-term partners), and a tail at $-10$ (confirmed scammers).
2. **`structural_balance_triads.png` (Slide 5 / Report Fig. 1b):**
   - **What it shows:** Bar chart of all $61,515$ signed triads across $T_3$ ($[+,+,+] = 74.8\%$), $T_2$ ($[+,-,-] = 16.4\%$), $T_1$ ($[+,+,-] = 7.8\%$), and $T_0$ ($[-,-,-] = 1.0\%$). Green bars ($T_3, T_2$) sum to $91.2\%$ classic Heider balance.
3. **`balance_null_model.png` (Slide 5 / Report Fig. 7b):**
   - **What it shows:** Grey histogram on the left is the null distribution of structural balance across $1,000$ sign-shuffled permutations ($\mu = 79.4\%, \sigma = 0.22\%$). Dashed red vertical line on the right is the observed empirical balance ($91.2\%$), separated by $52.4$ standard deviations ($Z = +52.4$).
4. **`degree_distribution_powerlaw.png` (Slide 4 / Report Fig. 2a):**
   - **What it shows:** Log-log scatter plot of degree $k$ (x-axis) vs. complementary cumulative/probability density $P(k)$ (y-axis), with a fitted power-law line $P(k) \sim k^{-2.14}$ in red. Confirms scale-free hub structure.
5. **`degree_assortativity_mixing.png` (Slide 4 / Report Fig. 2b):**
   - **What it shows:** Node degree $k$ (log x-axis) vs. average neighbor degree $\langle k_{\text{nn}}(k) \rangle$ (log y-axis). The clear downward slope ($r = -0.1409$) proves disassortative core-periphery mixing: small retail traders connect to high-degree hubs.
6. **`k_core_and_centrality_distribution.png` (Report Fig. 3):**
   - **What it shows:** Distribution of node coreness shells ($k=1$ periphery up to the $k_{\max}=19$ inner nucleus of $108$ elite brokers) alongside PageRank vs. Degree correlation.
7. **`link_prediction_roc_curves.png` & `link_prediction_pr_curves.png` (Slide 10 / Report Fig. 4a–4b):**
   - **What they show:** ROC (FPR vs. TPR) and Precision-Recall (Recall vs. Precision) curves on the $7,294$-pair MST test set. Notice how the local heuristics ($CN, AA, RA, JC$) plateau horizontally in TPR around $0.67$ once all $2$-hop pairs are exhausted (since they assign $0$ to $d \ge 3$ pairs), whereas $PA$ and the **Normalized Rank Ensemble** smoothly rank the remaining $d \ge 3$ pairs all the way to $(1.0, 1.0)$.
8. **`temporal_link_prediction_comparison.png` (Slide 11 / Report Fig. 5a):**
   - **What it shows:** Grouped bar chart comparing Static 80/20 MST AUC vs. Chronological Temporal Backtest AUC (2010–2013 train $\rightarrow$ 2014–2016 test). Demonstrates that PA ($0.8285$) and Ensemble ($0.8150$) generalize forward in time.
9. **`topological_vs_embedding_comparison.png` (Slide 9 / Report Fig. 5b):**
   - **What it shows:** Grouped bar comparison between our Topological Ensemble, PA, AA, and the learned 64-dimensional Spectral SVD + Logistic Regression baseline across AUC, AP, F1, and P@100.
10. **`link_prediction_precision_at_k.png` (Slide 11 / Report Fig. 6):**
    - **What it shows:** Precision@K curves for $K \in \{10, 20, 50, 100\}$. Highlights that CN, AA, RA, PA, and Ensemble maintain $1.000$ precision up to $K=50$, while Jaccard (purple line) fails at the top of the ranking ($P@10 = 0.200$).
11. **`recommended_ego_network.png` (Slide 12 / Report Fig. 7a):**
    - **What it shows:** Force-directed 2-hop ego-network centered on Anchor Trader `#1` (blue node), showing mutual intermediaries (grey nodes, dashed orange trust links) and Top-20 recommended counterparties (green nodes, solid green predicted links).

---

## Part 6: Step-by-Step Live Interactive Web Dashboard Walkthrough

During or immediately after **Slide 13 / Slide 14**, Speaker 3 can switch to the browser to demonstrate the live system in **60–90 seconds**.

### How to Launch Before the Presentation Starts
- **Option A (Full Live Server — Windows, macOS & Linux):**
  ```bash
  # On Windows: double-click run_ui_windows.bat OR run:
  .venv\Scripts\python.exe run.py serve

  # On Linux / macOS:
  .venv/bin/python run.py serve
  # Open http://localhost:5000 in browser
  ```
- **Option B (Zero-Dependency Offline Standalone HTML — Instant Fallback):**
  Open [`visualizations/interactive_recommendation_demo.html`](visualizations/interactive_recommendation_demo.html) directly in any browser (all data, physics, and interactive views are pre-bundled inside the HTML file so it works even without Wi-Fi or Python running).

### 4-Step Live Demo Script (60 Seconds)
1. **Step 1 — Dynamic Trader Query & Ego-Network Physics (15 sec):**
   - Select **Anchor Trader `#1`** (or switch the dropdown to **Trader `#7`**, **Trader `#13`**, or enter any trader ID in the live search bar).
   - Point out the central blue Anchor node, grey mutual intermediaries, and green recommended counterparties. Drag a green node (e.g., **Trader `#72`** or **Trader `#3`**) to show the real-time D3.js force simulation.
2. **Step 2 — Heuristic Switcher & Top-K Slider (15 sec):**
   - Switch the ranking algorithm dropdown from **Normalized Rank Ensemble** to **Adamic-Adar**, **Resource Allocation**, and then **Jaccard Coefficient**. Point out how the Top-K ranking table and link thickness dynamically update in real time.
3. **Step 3 — Click a Node/Link to Open the 2-Hop Trust Chain Provenance Modal (20 sec):**
   - Click directly on recommended **Trader `#3`** (or click its row in the recommendation table).
   - A modal pops up showing the **2-Hop Trust Chain Provenance Breakdown**: it lists the exact shared intermediaries $z \in \Gamma(1) \cap \Gamma(3)$ (such as Broker `#7`, `#10`, `#22`), displays each intermediary's degree $k_z$, and shows the exact per-intermediary contributions $\frac{1}{\ln k_z}$ (Adamic-Adar) and $\frac{1}{k_z}$ (Resource Allocation).
4. **Step 4 — Benchmark Gallery & Mathematical Sandbox Tabs (10 sec):**
   - Click the **Benchmark Gallery** tab to show the interactive ROC/PR/Temporal/Enterprise charts, and click the **Math Sandbox** tab where evaluators can adjust intermediary degrees with sliders to watch $CN, JC, AA, RA, PA$ update live.

---

## Part 7: Comprehensive 20-Question Technical Q&A Bank

Review these 20 questions and answers as a team. They are grouped by speaker domain so each member knows which questions to field first.

---

### Section A: Domain, Dataset & Topology Questions (Primary: Speaker 1)

#### Q1: Why did you remove the negative distrust edges (~9.3% in Alpha, ~10.35% in OTC) instead of keeping all edges in the graph?
- **Answer:** In a signed trust network, keeping negative edges corrupts unsigned topological link predictors through **Triad Pollution**. Specifically, under Heider's Structural Balance Theory, when two honest traders $u$ and $v$ both distrust the same scammer $z$, they form a balanced $[+,-,-]$ triad ($T_2$, which accounts for $16.4\%$ of all triangles in our dataset). If we do not remove negative edges, Common Neighbors, Adamic-Adar, and Resource Allocation treat scammer $z$ as a valid shared neighbor! Even worse, if trader $u$ trusts broker $z$ ($+1$) and broker $z$ distrusts scammer $s$ ($-1$), keeping the negative edge creates a 2-hop path $u \to z \to s$ that would recommend the scammer $s$ to trader $u$. Filtering strictly for $\bar{w}(u,v) > 0$ guarantees that every 2-hop wedge $u - z - v$ represents two positive trust endorsements.

#### Q2: How did you collapse directed, multi-edge ratings between the same pair of traders into an undirected signed graph?
- **Answer:** In the raw SNAP logs, trader $u$ can rate trader $v$ multiple times over time, and both $(u \to v)$ and $(v \to u)$ can exist with ratings in $[-10, +10]$. First, for any directed pair, we take the most recent timestamped rating to reflect their current bilateral standing. Second, between unordered pairs $\{u,v\}$, we compute the arithmetic mean weight $\bar{w}(u,v) = \frac{w(u \to v) + w(v \to u)}{2}$ (or the single directed rating if unidirectional). If $\bar{w}(u,v) > 0$, we retain $(u,v) \in E^+$; if $\bar{w}(u,v) \le 0$, we classify it as distrust/neutral and exclude it from positive link prediction.

#### Q3: When merging Bitcoin Alpha and Bitcoin OTC into the Unified Empirical Network, how did you handle node ID collisions?
- **Answer:** Both Bitcoin Alpha and Bitcoin OTC assign integer node IDs starting at `1`. While a few early adopters used both platforms, SNAP anonymized user IDs independently per platform without a cross-platform identity key. To preserve the exact topological integrity of both marketplaces within a unified multi-component benchmark without falsely merging unrelated users who happened to share the same integer ID, we offset Bitcoin OTC node IDs by $+100,000$ (while retaining cross-validated anchor links), yielding $9,207$ unique trader vertices and $31,050$ positive trust ties.

#### Q4: What does the power-law exponent $\gamma = 2.14$ tell us mathematically about the Bitcoin trust network?
- **Answer:** A scale-free network follows $P(k) \sim k^{-\gamma}$. When $2 < \gamma < 3$ (specifically $\gamma = 2.14 \pm 0.08$ empirically and $\gamma = 2.10$ in our 25k graph), the first moment (mean degree $\langle k \rangle = 6.74$) is finite, but the second moment $\langle k^2 \rangle = \int k^2 P(k)\,dk$ diverges as $N \to \infty$. Mathematically, this means degree variance is extreme: a tiny fraction of OTC market-maker hubs (like Trader `#100035` with $k=785$ and Trader `#1` with $k=507$) mediate a massive fraction of shortest paths, creating an ultra-compact "small world" where hubs act as gravitational attractors for Preferential Attachment.

#### Q5: What does negative degree assortativity ($r = -0.1409$) mean in plain English, and why is it unusual for social networks?
- **Answer:** Most friendship or academic co-authorship networks have *positive* assortativity ($r > 0$): popular people connect to other popular people. By contrast, financial OTC trading networks exhibit *negative* degree assortativity ($r = -0.1409$, disassortative mixing): high-degree liquidity brokers (market makers) predominantly trade with dozens of low-degree retail traders ($k \le 5$), while retail traders rarely trade directly with other retail traders. This creates a core-periphery hub-and-spoke market structure.

#### Q6: How does K-Core decomposition ($k_{\max}=19$) differ from simply ranking nodes by degree?
- **Answer:** Degree centrality only counts a node's immediate neighbors: a star node connected to 500 degree-1 leaf nodes has degree 500, but if you peel away degree-1 nodes, that star collapses into the 1-core! By contrast, Iterative K-Core Peeling recursively removes all nodes with degree $< k$ until only nodes with at least $k$ neighbors *within the remaining subgraph* survive. Finding a $19$-core of $108$ nodes proves that these $108$ elite brokers are not isolated stars—each one maintains at least $19$ mutually verified trust connections with other members of that same inner clearinghouse nucleus.

#### Q7: Why wasn't counting $91.2\%$ balanced triads ($T_3 + T_2$) sufficient on its own? Why did you run the $1,000$-permutation null model ($Z = +52.4$)?
- **Answer:** Because $p \approx 90\%$ of edges in the network are positive, even a completely random assignment of $+$ and $-$ signs onto triangles would generate $p^3 \approx (0.9)^3 = 72.9\%$ all-positive $T_3$ triangles and $3p(1-p)^2 \approx 2.7\%$ $T_2$ triangles by pure base-rate probability! By fixing the exact triangle topology and randomly shuffling the sign vector $1,000$ times, we measured the exact null expectation ($\mu_{\text{null}} = 79.4\%, \sigma_{\text{null}} = 0.22\%$). Our observed $91.2\%$ balance sits $52.4$ standard deviations above the null mean ($Z = +52.4, p < 10^{-100}$), proving that traders actively close positive triangles and avoid conflicted $T_1$ ($[+,+,-]$) relationships.

---

### Section B: Evaluation Split, Heuristics & Mathematical Questions (Primary: Speaker 2)

#### Q8: Why did you lock a Minimum Spanning Tree (MST) into the training set during the 80/20 edge split?
- **Answer:** In a heavy-tailed graph ($\gamma = 2.14$) where over $70\%$ of nodes have degree $\le 5$, deleting $20\%$ of edges uniformly at random frequently severs low-degree leaf nodes from the Giant Connected Component ($9,119$ nodes). Once a node $u$ becomes isolated in $G_{\text{train}}$ ($k_u = 0$), every topological heuristic ($CN, JC, AA, RA, PA$) outputs $0$ for all test edges incident to $u$, artificially distorting evaluation. By extracting a Minimum Spanning Tree of $N - 1 = 9,118$ edges first and locking it into $E_{\text{train}}^+$, we guarantee $100\%$ node reachability across all $9,119$ nodes while still holding out $3,647$ non-tree cycle edges ($20.0\%$) for testing.

#### Q9: Could locking the MST into the training set introduce structural bias, and how did you verify that your findings don't depend on the MST split?
- **Answer:** That is a great methodological question. Because MST edges form a spanning tree backbone while held-out test edges are cycle-closing chords, one might wonder if cycle edges favor triadic closure. That is why we implemented **Protocol B (Chronological Temporal Backtesting)**, which uses *zero* MST locking: we split strictly by timestamp ($2010\text{–}2013$ training vs. $2014\text{–}2016$ testing). Under the chronological split, the exact same model hierarchy holds—PA ($0.8285$ AUC) and our Normalized Rank Ensemble ($0.8150$ AUC, $1.000$ P@20) remain #1 and #2, proving our results are robust across both static and temporal splitting schemes.

#### Q10: How did you sample negative test edges, and why did you restrict them to graph distance $d_{G_{\text{train}}}(u,v) \ge 2$?
- **Answer:** A positive test edge $(u,v) \in E_{\text{test}}^+$ has been removed from $G_{\text{train}}$, so in $G_{\text{train}}$ its endpoints $(u,v)$ are non-adjacent, meaning their shortest-path distance in $G_{\text{train}}$ is at least $2$ ($d_{G_{\text{train}}}(u,v) \ge 2$). Therefore, to construct a fair, leakage-free binary classification benchmark of $3,647$ positives and $3,647$ negatives ($7,294$ total pairs), we uniformly sample negative pairs $(u,v) \notin E^+$ from $V \times V$ that are also non-adjacent in $G_{\text{train}}$ ($d_{G_{\text{train}}}(u,v) \ge 2$), ensuring zero overlap with training or test positives.

#### Q11: Why did the Jaccard Coefficient perform so poorly on Top-K Precision ($P@10 = 0.200$, $P@20 = 0.150$) when CN, AA, and RA all achieved $1.000$?
- **Answer:** Look at Jaccard's denominator: $JC(u,v) = \frac{|\Gamma(u) \cap \Gamma(v)|}{|\Gamma(u) \cup \Gamma(v)|}$. Suppose two peripheral traders $a$ and $b$ each have only $k_a = k_b = 2$ neighbors, and they share those exact $2$ neighbors. Their Jaccard score is $\frac{2}{2} = 1.000$ (the maximum possible score!), even though a 2-node overlap in a sparse periphery is statistically noisy. Conversely, when Anchor Trader `#1` ($k=507$) shares $66$ trusted brokers with Trader `#72` ($k=116$), their union size is $507 + 116 - 66 = 557$, pushing their Jaccard score down to $66 / 557 = 0.1185$! Thus, Jaccard ranks tiny peripheral overlaps at the top of the list (causing false positives at $K=10, 20$) while pushing heavily vetted hub-broker pairs down.

#### Q12: What is the exact mathematical difference between Adamic-Adar (AA) and Resource Allocation (RA), and when does RA diverge from AA?
- **Answer:** Both discount shared intermediaries $z \in \Gamma(u) \cap \Gamma(v)$ by their degree $k_z = |\Gamma(z)|$, but Adamic-Adar uses inverse *logarithmic* scaling ($\frac{1}{\ln k_z}$) whereas Resource Allocation uses inverse *linear* scaling ($\frac{1}{k_z}$). For example, compare a specialist intermediary ($k_z = 3$) vs. a mega-hub ($k_z = 500$):
  - Under **AA**, the ratio of their weights is $\frac{\ln 500}{\ln 3} = \frac{6.21}{1.10} \approx 5.6\times$.
  - Under **RA**, the ratio of their weights is $\frac{500}{3} \approx 166.7\times$.
  Therefore, RA penalizes mega-hubs almost $30\times$ more aggressively than AA. We see this directly in our Trader `#1` case study: Trader `#72` ($66$ shared neighbors) beats Trader `#3` ($65$ shared neighbors) on AA ($17.56$ vs. $17.46$), but Trader `#3` beats Trader `#72` on RA ($2.043$ vs. $1.982$) because Trader `#3`'s shared intermediaries have lower degrees.

#### Q13: Why do CN, Jaccard, AA, and RA all have the exact same F1-score ($0.6667$) on the empirical test set?
- **Answer:** In the empirical test set, roughly $50\%$ of the held-out positive test edges close a 2-hop wedge ($|\Gamma(u) \cap \Gamma(v)| \ge 1$, so $d_{G_{\text{train}}}(u,v) = 2$), while the remaining positive test edges span $d_{G_{\text{train}}}(u,v) \ge 3$ where $|\Gamma(u) \cap \Gamma(v)| = 0$. Meanwhile, because the graph is sparse ($\bar{k} = 6.74$ across $9,119$ nodes), almost $99\%$ of randomly sampled negative non-edges lie at distance $d \ge 3$ and also have $|\Gamma(u) \cap \Gamma(v)| = 0$. Consequently, for *any* purely 2-hop heuristic ($CN, JC, AA, RA$), the optimal F1 threshold simply separates pairs with $\text{Score} > 0$ (i.e., $CN \ge 1$) from pairs with $\text{Score} = 0$, yielding the exact same binary partition at the F1 peak ($\text{F1} = 0.6667$), even though their continuous ranking orderings (AUC and Precision@K) differ!

#### Q14: Why did you use Percentile Rank Normalization in the Ensemble instead of Min-Max Scaling or Z-Score Standardization?
- **Answer:** In a scale-free graph ($\gamma = 2.14$), heuristic score distributions have extreme power-law skewness. For instance, Preferential Attachment spans $[1, 398{,}000]$ with a massive right tail, whereas Jaccard spans $[0, 1]$. If we applied Min-Max scaling $\frac{x - x_{\min}}{x_{\max} - x_{\min}}$, the single outlier pair with $PA = 398,000$ would compress $99\%$ of all other pairs into $[0.0, 0.01]$. Similarly, Z-score standardization is distorted by heavy-tailed variance. Converting each heuristic $m$ to its empirical percentile rank $\tilde{r}_m(u,v) \in [0,1]$ (a non-parametric copula transform) maps every heuristic onto a uniform $[0,1]$ distribution, making our convex weights ($0.30, 0.25, 0.25, 0.10, 0.10$) mathematically well-conditioned and completely immune to outlier distortion.

#### Q15: How did you choose the Ensemble weights ($0.30\text{AA} + 0.25\text{RA} + 0.25\text{Jac} + 0.10\text{CN} + 0.10\text{PA}$)?
- **Answer:** The weights are structured by structural function:
  1. **$55\%$ Hub-Penalized Triadic Closure ($0.30\text{AA} + 0.25\text{RA}$):** AA and RA are our strongest local discriminators (both $0.8366$ AUC, $1.000$ P@100), so they receive the majority vote.
  2. **$35\%$ Neighborhood Overlap & Density ($0.25\text{Jac} + 0.10\text{CN}$):** Once converted to percentile ranks and anchored by AA/RA, Jaccard's relative neighborhood overlap and CN's raw count help differentiate medium-degree local clusters.
  3. **$10\%$ Global Scale-Free Prior ($0.10\text{PA}$):** Gives the ensemble a non-zero tie-breaker for long-range pairs ($d \ge 3$) where all four local metrics are zero, boosting global F1 to `#1` ($0.8903$) without letting hub degree products override verified 2-hop trust chains at the top of the recommendation list.

---

### Section C: SVD Baseline, Enterprise Scale & System Architecture Questions (Primary: Speaker 3)

#### Q16: Why did Preferential Attachment get the highest AUC on the 9,207-node empirical network ($0.9505$), whereas the Normalized Rank Ensemble beat PA on the 25,000-node Enterprise network ($0.7544$ vs. $0.6926$)?
- **Answer:** On the sparser empirical graph ($\bar{k} = 6.74$), around half of test edges span distance $d \ge 3$ where local 2-hop heuristics output zero, giving PA a massive global recall advantage across the bottom half of the ROC curve. However, on the 25,000-node Enterprise Holme-Kim network ($135,857$ edges, $\bar{k} = 10.87$, clustering $C = 0.1810$), local triangle density is higher and there are $312$ hubs in the 24-core across multiple distinct communities. Because PA blindly multiplies hub degrees across unrelated communities, it generates many high-scoring false positives on the 25k graph (dropping to $0.6926$ AUC), whereas our Normalized Rank Ensemble leverages 2-hop triadic precision to achieve the `#1` AUC ($0.7544$) and `#1` AP ($0.8004$).

#### Q17: Why did your topological heuristics outperform the 64-dimensional Truncated SVD spectral embedding baseline ($0.9402$ vs. $0.9175$ AUC, and $0.8903$ vs. $0.4522$ F1)?
- **Answer:** Three reasons:
  1. **Rank-64 Spectral Smoothing:** Truncated SVD approximates $A_{\text{train}}$ using only the top $64$ global eigenvectors. In a sparse graph ($\bar{k}=6.74$), low-rank spectral projection smooths over sharp local 2-hop wedges among low- and medium-degree nodes.
  2. **Threshold Calibration under Degree Skew:** The Logistic Regression classifier trained on Hadamard products $\mathbf{z}_u \odot \mathbf{z}_v$ assigns conservative probabilities to moderate-degree pairs, hurting its F1-score ($0.4522$) at the standard decision boundary.
  3. **Zero-Shot Explainability & Speed:** Topological heuristics require zero training parameters, run $4.3\times$ faster ($0.42\text{s}$ vs. $1.80\text{s}$), and provide exact 2-hop intermediary names rather than an opaque 64-float vector.

#### Q18: How did you generate the 25,000-node Enterprise Benchmark, and why use a Holme-Kim model instead of Erdős-Rényi or standard Barabási-Albert?
- **Answer:** An Erdős-Rényi random graph has a Poisson degree distribution (no hubs) and near-zero clustering ($C \approx \bar{k}/N \approx 0.0004$). A standard Barabási-Albert preferential attachment graph produces scale-free hubs ($\gamma \approx 3$), but still has very low triangle clustering ($C \to 0$ as $N \to \infty$), which fails to mimic real social trust networks ($C = 0.1720$). The **Holme-Kim Power-Law Cluster Model** alternates between a Barabási-Albert preferential attachment step and a *triadic closure step* (connecting a new node to a neighbor of its newly attached hub with probability $p_t$). This simultaneously reproduces both the heavy-tailed degree distribution ($\gamma = 2.10$) and the high triangle clustering ($C = 0.1810$) of real crypto trust networks at $25,000$-node scale.

#### Q19: What is the computational complexity of generating Top-20 recommendations for a single trader in your live web app, and can it run in real time?
- **Answer:** In production, we do *not* need to score all $O(N^2)$ pairs across the entire network when a single trader $u$ opens their dashboard. We only need to traverse trader $u$'s 2-hop neighborhood $\bigcup_{z \in \Gamma(u)} \Gamma(z)$, which takes $O(k_u \cdot \bar{k})$ operations (roughly $500 \times 7 \approx 3,500$ operations even for a top hub, or $< 1\text{ millisecond}$ in Python/C++), plus a fast top-hub lookup for the $10\%$ PA tie-breaker. In addition, when a new rating is recorded on-chain, updating the adjacency sets $\Gamma(u)$ and $\Gamma(v)$ takes $O(1)$ time, avoiding any model retraining.

#### Q20: How could a malicious attacker try to game your link prediction engine (e.g., a Sybil attack), and how would you defend against it?
- **Answer:** In a **Sybil / Collusion Attack**, an attacker creates fake accounts $s_1, \dots, s_m$ that all issue positive ratings to a malicious target account $v$, trying to inflate $v$'s degree $k_v$ (to game Preferential Attachment) or create fake common neighbors. Notice that our **Normalized Rank Ensemble** already provides strong natural defense against naive Sybil rings: because our $90\%$ local weight requires shared intermediaries $z \in \Gamma(u) \cap \Gamma(v)$, a Sybil node $s_i$ only counts if the *honest querying trader $u$ already explicitly trusted $s_i$*! If $u$ never trusted the Sybil ring, $s_i \notin \Gamma(u)$, so $CN, JC, AA, RA$ are completely unaffected. To further harden the $10\%$ PA component, we can replace raw degree $k_v$ with **TrustRank / Personalized PageRank** seeded from the verified $19$-core anchor brokers.

---

## Part 8: Pre-Presentation Readiness Checklist

- [ ] **Slide Deck Open & Checked:** Open [`slides/link_prediction_presentation.pdf`](slides/link_prediction_presentation.pdf) or [`slides/link_prediction_presentation.pptx`](slides/link_prediction_presentation.pptx) in full-screen presentation mode (14 slides, 16:9 widescreen).
- [ ] **Formal Report Ready for Reference:** Have [`reports/link_prediction_report.pdf`](reports/link_prediction_report.pdf) (8 pages) and [`reports/team_presentation_study_guide.pdf`](reports/team_presentation_study_guide.pdf) open in a secondary tab.
- [ ] **Live Interactive Dashboard Running:**
  - Start `python run.py serve` (`http://localhost:5000`, or `run_ui_windows.bat` on Windows) **OR** open [`visualizations/interactive_recommendation_demo.html`](visualizations/interactive_recommendation_demo.html) in a browser tab zoomed to `100%`.
  - Pre-select **Trader `#1`** and test clicking **`🔍 Audit`** on **Trader `#3`** so the **2-Hop Trust Chain Provenance Modal** opens smoothly during the demo.
- [ ] **Speaker Hand-Offs Practiced:**
  - **Speaker 1:** Slides 1–5 (~5.5 min) $\rightarrow$ hands off after the $Z = +52.4$ null-model proof.
  - **Speaker 2:** Slides 6–9 (~5.5 min) $\rightarrow$ hands off after the SVD-64 spectral comparison.
  - **Speaker 3:** Slides 10–14 + 60-second live demo (~6 min).
