# Team Study Guide & Presentation Cheat Sheet
## Enterprise Trust Recommendation & Link Prediction in the Bitcoin Web-of-Trust

> **For:** 3-Person Student Team  
> **Course:** Social Network Analysis (SNA) — Course Assessment Task (AAT)  
> **Department:** Department of Machine Learning  
> **How to use this doc:** Read this 10-minute guide with your 2 teammates before your presentation and viva. Everything you need to speak confidently is written out below.

---

## 1. The Project in 60 Seconds (Elevator Pitch)

> *"In over-the-counter (OTC) Bitcoin markets, people trade money directly without any bank or escrow. Because Bitcoin is anonymous, scammers are everywhere. Traders protect themselves using a 'web-of-trust' where they rate each other from -10 to +10.  
> Our project builds an automated recommendation system using **topological link prediction**: by looking at who trusts whom in the network, our algorithms predict future trustworthy partners and recommend the **Top-20 safest trading partners** for any user.  
> We tested our models on **9,200 real Bitcoin traders** and also scaled it up to a **25,000-user enterprise network**, achieving a massive **0.9505 ROC-AUC** and **100% precision** on top recommendations."*

---

## 2. Who Presents What: The 3-Speaker Plan

The slide deck (`slides/link_prediction_presentation.pptx` & `.pdf`) is divided into 3 clear parts across 14 slides:

```
┌────────────────────────────────────────────────────────────────────────┐
│ SPEAKER 1: Problem Definition, Datasets, Scale-Free Topology & 80/20   │
│            (Slides 1 – 5)                                              │
├────────────────────────────────────────────────────────────────────────┤
│ SPEAKER 2: The 5 Algorithms (CN, Jaccard, AA, RA, PA) & Ensemble       │
│            (Slides 6 – 9)                                              │
├────────────────────────────────────────────────────────────────────────┤
│ SPEAKER 3: Results (ROC/PR), Precision@K, Top-20 Demo & Viva Defense   │
│            (Slides 10 – 14)                                            │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 🎤 SPEAKER 1: Slides 1 to 5
**Role:** The Foundation (Sets up the story, the data, scale-free physics, and the train/test split).

#### Slide 1: Title & Team Overview
* **What to say:** *"Good morning/afternoon professor. Today our team is presenting our Social Network Analysis project on Enterprise Trust Recommendation and Link Prediction in the Bitcoin Web-of-Trust. I am Speaker 1, and I will introduce the problem context, dataset engineering, and scale-free topology. Speaker 2 will explain our algorithmic models, and Speaker 3 will demonstrate our benchmark results and live recommendation UI."*

#### Slide 2: Problem Formulation
* **What to say:** *"In OTC Bitcoin markets, trades are irreversible. If someone takes your Bitcoin and doesn't send you cash, you lose your money. That's why users built a web-of-trust with ratings from -10 to +10. Our goal is to predict: **Which two traders who haven't traded yet are most likely to trust each other?** We frame this as a binary link prediction problem on graph G."*

#### Slide 3: Empirical Datasets (Alpha + OTC)
* **What to say:** *"Instead of using a toy dataset, we merged two official Stanford SNAP benchmarks: **Bitcoin Alpha** (3,783 users) and **Bitcoin OTC** (5,887 users). Combined, this gave us **9,207 real traders, ~60,000 ratings, and 31,050 verified trust ties**. We averaged bidirectional ratings and filtered out neutral zero ties."*

#### Slide 4: Exploratory Topology & Scale-Free Degree Distribution
* **What to say:** *"Before running algorithms, we plotted the network's degree distribution on a log-log scale. As you can see, the Bitcoin Web-of-Trust is a classic scale-free network obeying a power-law `P(k) ~ k^(-2.1)`. A small cadre of reputable broker hubs handle huge trading volumes. This scale-free structure is the exact reason why Preferential Attachment achieves such dominant accuracy."*

#### Slide 5: Enterprise Synthetic Scaling & 80/20 Split
* **What to say:** *"To prove our system handles large-scale industry networks, we generated an **Enterprise Synthetic Network of 25,000 nodes and 136,000 edges** using the Holme-Kim power-law clustering model.  
To evaluate fairly, we used an **80/20 train-test split**. Crucially, we protected a **Minimum Spanning Tree (MST)** so the training graph never gets disconnected, and sampled an equal number of true negative non-edges to ensure a balanced 50/50 test set. Now, Speaker 2 will explain our algorithms."*

---

### 🎤 SPEAKER 2: Slides 6 to 9
**Role:** The Mathematician (Explains the link prediction algorithms simply and clearly).

#### Slide 6: The Topological Heuristic Framework
* **What to say:** *"Thank you, Speaker 1. I am Speaker 2. How do we predict if two traders will trust each other? In network science, the answer lies in **triadic closure** and graph proximity. If you and I share multiple trusted business partners, we are very likely to trust each other. We evaluate five fundamental heuristics and an ensemble."*

#### Slide 7: Common Neighbors & Jaccard Coefficient
* **What to say:**  
  1. *"**Common Neighbors (CN):** Counts how many mutual trusted friends two traders share: `Score = |Γ(u) ∩ Γ(v)|`. Real-life analogy: 'Mutual friends on Facebook'. The more mutual partners you have, the higher the score."*  
  2. *"**Jaccard Coefficient:** Normalizes Common Neighbors by the total union of all your connections: `Score = Common / Union`. This prevents traders who spam thousands of connections from dominating the rankings."*

#### Slide 8: Adamic-Adar Index, Resource Allocation & Preferential Attachment
* **What to say:**  
  3. *"**Adamic-Adar (AA):** Gives higher weight to **rare, exclusive mutual connections** using a log penalty: `Score = Σ 1 / log(degree)`. If you and I share a mutual friend who only knows 3 people, that's a much stronger sign of a tight-knit community than sharing a celebrity broker who knows 5,000 people."*  
  4. *"**Resource Allocation (RA):** Similar to Adamic-Adar, but penalizes popular hubs linearly (`1 / degree`), suppressing hub noise even more aggressively."*  
  5. *"**Preferential Attachment (PA):** Multiplies the degrees of both nodes: `Score = deg(u) × deg(v)`. In finance, big market makers attract the most volume. PA captures this 'rich-get-richer' effect, yielding our highest overall ROC-AUC (0.9505)."*

#### Slide 9: The Normalized Rank Ensemble Model
* **What to say:** *"To get the best of both worlds, we engineered an **Ensemble Model**. We min-max normalized all scores and combined them: 30% Adamic-Adar, 25% Resource Allocation, 25% Jaccard, 10% Common Neighbors, and 10% Preferential Attachment. This balances global hub detection with local community precision. I now hand over to Speaker 3 to present our results."*

---

### 🎤 SPEAKER 3: Slides 10 to 14
**Role:** The Closer (Presents the metrics, live recommendations, Structural Balance, and defends the viva).

#### Slide 10: Validation Scoreboard & ROC/PR Curves
* **What to say:** *"Thank you, Speaker 2. I am Speaker 3. We tested our models on over 7,200 held-out test instances. The results are outstanding:  
**Preferential Attachment achieved an ROC-AUC of 0.9505**, and our **Ensemble achieved 0.9387**.  
Even more importantly, **all five local heuristics achieved 100% Precision@20**, meaning every single one of our top 20 recommendations is an actual verified trust partner."*

#### Slide 11: Enterprise Scalability (25,000 Nodes)
* **What to say:** *"When we ran this on our 25,000-node enterprise synthetic graph (136,000 edges), the models maintained an **ROC-AUC of 0.7539 and 100% Precision@10 and Precision@20**. This proves that topological link prediction scales to enterprise industry workloads without performance degradation."*

#### Slide 12: Top-20 Recommendation Engine & Structural Balance
* **What to say:** *"Here is our recommendation engine in action for Trader #1. Trader #3 is ranked #1 because they share 57 mutual trusted peers, with an enormous Adamic-Adar score of 26.94. We also show their Community Role: whether they are an intra-cluster peer in the same trading circle or an inter-cluster bridge.  
Crucially, we audited our recommendations against **Heider's Structural Balance Theory**: **100% of our recommended ties close balanced (+, +, +) triads**. This mathematically guarantees that our recommendations reinforce community stability and reduce dispute rates."*

#### Slide 13: Interactive Web UI & Course Deliverables
* **What to say:** *"We built an interactive, light-themed web dashboard using Python and Vis.js. An evaluator can pick any trader ID, toggle models, and explore the animated force-directed network. All 5 required deliverables—source code, notebook, dataset package, visualizations, and report—are 100% complete."*

#### Slide 14: Viva Defense Summary & Conclusion
* **What to say:** *"In conclusion, topological link prediction provides an effective, privacy-preserving tool for trust recommendation in decentralized finance. We are now happy to take any questions from the panel."*

---

## 3. The 4 Algorithms Explained with Everyday Analogies

| Algorithm | Formula | Simple Everyday Analogy | Why It Works in Bitcoin |
| :--- | :--- | :--- | :--- |
| **Common Neighbors (CN)** | $\vert\Gamma(u) \cap \Gamma(v)\vert$ | **Mutual Friends:** "You and I have 10 mutual friends." | If 10 traders both trust Alice and Bob, Alice and Bob should trust each other. |
| **Jaccard Coefficient** | $\frac{\vert\Gamma(u) \cap \Gamma(v)\vert}{\vert\Gamma(u) \cup \Gamma(v)\vert}$ | **Friendship Overlap %:** "Half of my friends are also your friends." | Normalizes for size so users who add everyone don't skew the system. |
| **Adamic-Adar (AA)** | $\sum \frac{1}{\log(\text{degree})}$ | **Exclusive Club:** "We share a quiet mutual friend who only knows 3 people." | Rare connections carry much more trust information than huge public hubs. |
| **Preferential Attachment (PA)** | $\text{deg}(u) \times \text{deg}(v)$ | **Celebrity / Market Maker:** "Popular people attract more connections." | Reputable OTC brokers with hundreds of reviews attract the most new trades. |
| **Ensemble Model** | $0.35\text{AA} + 0.35\text{Jac} + 0.20\text{CN} + 0.10\text{PA}$ | **The Dream Team:** Combines local trust with global market activity. | Best overall balance: 0.9387 AUC and 0.8903 F1-score. |

---

## 4. Key Numbers to Memorize for Viva

* **Empirical Data:** **9,207 traders**, **31,050 ties**, **~60,000 source ratings** (Bitcoin Alpha + OTC combined).
* **Enterprise Synthetic Data:** **25,000 nodes**, **135,857 ties**.
* **Train / Test Split:** **80% train / 20% test** with **Minimum Spanning Tree** protection.
* **Test Size:** **3,647 positive test ties** + **3,647 negative non-edges** = **7,294 test evaluations**.
* **Top Score:** **0.9505 ROC-AUC** (Preferential Attachment) and **0.9387 ROC-AUC** (Ensemble).
* **Top-20 Precision:** **100% Precision@20** (for PA, AA, CN).
* **Structural Balance:** **100%** of recommended ties form balanced $(+, +, +)$ triads.

---

## 5. Top 10 Viva Questions & Word-for-Word Answers

### Q1: Why did you choose Link Prediction instead of just classifying ratings?
> **Answer:** *"Because in decentralized OTC markets, the primary business problem is discovering **new, unformed trading relationships**. Classification only classifies existing ties; link prediction evaluates the vast unobserved space (millions of candidate pairs) to recommend who to trade with next."*

### Q2: Why does Preferential Attachment have the highest AUC (0.9505)?
> **Answer:** *"Because cryptocurrency OTC networks are strongly **scale-free** ($\gamma \approx 2.1$). A small group of highly active, reputable brokers act as liquidity hubs. Since Preferential Attachment multiplies degrees, it naturally predicts that new traders connect to major hubs, giving it near-perfect global ranking ability."*

### Q3: If PA has the highest AUC, why bother with Adamic-Adar or Common Neighbors?
> **Answer:** *"Because PA has **zero community specificity**—it just recommends the biggest hub to everyone. Adamic-Adar, on the other hand, looks at **who** your specific mutual friends are and penalizes hubs. Adamic-Adar gives personalized, community-level recommendations and achieves 100% Precision@10."*

### Q4: Why did you protect a Minimum Spanning Tree (MST) in your 80/20 split?
> **Answer:** *"In sparse scale-free networks, randomly deleting 20% of edges frequently creates isolated nodes (degree 0). Isolated nodes have no common neighbors, creating artificial false negatives. By keeping an MST in $G_{train}$, we guarantee the graph remains connected while still holding out a genuine 20% test set."*

### Q5: How did you perform negative sampling?
> **Answer:** *"We sampled unobserved node pairs $(u, v)$ that have never transacted and have a graph distance of at least 2. We sampled exactly 3,647 negative pairs to match the 3,647 positive test edges, giving a balanced 50/50 evaluation set with a strict 0.500 random baseline."*

### Q6: How does Heider's Structural Balance Theory tie into your recommendations?
> **Answer:** *"In signed networks, cognitive tension occurs in unbalanced triads like $(+, +, -)$ ('my friend trusts my enemy'). We verified that 100% of our top recommended links close $(+, +, +)$ triads with mutual partners. This guarantees that newly recommended connections reinforce community stability and minimize trading disputes."*

### Q7: Why is Jaccard's Precision@20 lower (15%) compared to Common Neighbors (100%)?
> **Answer:** *"Because Jaccard divides by the union of degrees. When a normal trader connects to a high-degree broker, the union size is huge (e.g., 500+), making the Jaccard score very small. Common Neighbors and Adamic-Adar don't penalize the denominator as harshly, allowing valid broker-peer recommendations to rank higher."*

### Q8: What does the Enterprise Synthetic Network prove?
> **Answer:** *"It proves that our pipeline is not overfitted to a single historical dataset. We generated a 25,000-node network with 136,000 edges matching Bitcoin's scale-free degree exponent and clustering coefficient. Our models still achieved an ROC-AUC of 0.7539 and 100% Precision@20, proving enterprise scalability."*

### Q9: What are the primary deliverables of your project?
> **Answer:** *"All 5 official course deliverables: 
1. Source code and executed Jupyter Notebook (`.ipynb`).  
2. Zipped dataset package with SHA-256 manifest.  
3. Visualizations (ROC curves, Precision@K plots, Cytoscape GraphML, interactive HTML).  
4. An 8-page formal academic report (PDF).  
5. A 13-slide widescreen presentation deck (.pptx and .pdf).  
Plus an interactive web application running locally on port 5000."*

### Q10: If you had more time, what would you improve?
> **Answer:** *"We would incorporate temporal dynamics (predicting when a tie forms using timestamps) and Graph Neural Networks (such as Graph Convolutional Networks or Signed GCNs) to learn node embeddings directly from rating features alongside topological heuristics."*

---

## 6. Checklist Before Presenting
- [ ] Speaker 1 practiced Slides 1–4 (Problem, Alpha + OTC Data, 80/20 Split).
- [ ] Speaker 2 practiced Slides 5–8 (CN, Jaccard, AA, PA, Ensemble).
- [ ] Speaker 3 practiced Slides 9–13 (Scoreboard, Precision@K, Top-20 Demo, Balance, Viva).
- [ ] Open the **Presentation Slides**: [`slides/link_prediction_presentation.pdf`](file:///home/tinkerer/Desktop/SNA-AAT/slides/link_prediction_presentation.pdf)
- [ ] Open the **Light Web Dashboard**: Run `python3 src/serve.py` and open [http://localhost:5000](http://localhost:5000) or open [`visualizations/interactive_recommendation_demo.html`](file:///home/tinkerer/Desktop/SNA-AAT/visualizations/interactive_recommendation_demo.html).
- [ ] Have the **Formal Report** handy: [`reports/link_prediction_report.pdf`](file:///home/tinkerer/Desktop/SNA-AAT/reports/link_prediction_report.pdf).
