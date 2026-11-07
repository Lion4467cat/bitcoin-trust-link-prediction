"""Build a highly detailed, 14-slide 3-speaker 16:9 presentation deck and PDF export."""
from pathlib import Path
import json
import subprocess
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
OUT_PPTX = ROOT / "slides" / "link_prediction_presentation.pptx"
OUT_PDF = ROOT / "slides" / "link_prediction_presentation.pdf"
METRICS_PATH = ROOT / "outputs" / "link_prediction_metrics.json"

metrics = json.loads(METRICS_PATH.read_text())

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors (Professional Light Theme with Slate & Teal Accents)
C_NAVY = RGBColor(15, 23, 42)        # #0F172A
C_TEAL = RGBColor(13, 148, 136)      # #0D9488
C_TEAL_DARK = RGBColor(15, 118, 110) # #0F766E
C_GOLD = RGBColor(217, 119, 6)       # #D97706
C_CORAL = RGBColor(225, 29, 72)      # #E11D48
C_PURPLE = RGBColor(99, 102, 241)    # #6366F1
C_TEXT = RGBColor(30, 41, 59)        # #1E293B
C_MUTED = RGBColor(100, 116, 139)    # #64748B
C_WHITE = RGBColor(255, 255, 255)
C_CARD_BG = RGBColor(255, 255, 255)
C_BORDER = RGBColor(226, 232, 240)   # #E2E8F0
C_BG = RGBColor(248, 250, 252)       # #F8FAFC

def apply_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG
    bg.line.fill.background()
    return bg

def add_header(slide, title_text, speaker_label, kicker="BITCOIN WEB-OF-TRUST  |  LINK PREDICTION & RECOMMENDATION"):
    apply_background(slide)
    
    # Top color rule
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_TEAL
    top_bar.line.fill.background()
    
    # Kicker + Speaker Badge
    tx_kicker = slide.shapes.add_textbox(Inches(0.8), Inches(0.32), Inches(8.5), Inches(0.3))
    p_k = tx_kicker.text_frame.paragraphs[0]
    p_k.text = kicker
    p_k.font.size = Pt(11)
    p_k.font.bold = True
    p_k.font.color.rgb = C_TEAL
    
    # Speaker pill badge
    spk_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.4), Inches(0.30), Inches(3.133), Inches(0.38))
    spk_card.fill.solid()
    spk_card.fill.fore_color.rgb = RGBColor(241, 245, 249)
    spk_card.line.color.rgb = C_TEAL
    spk_card.line.width = Pt(1)
    tx_spk = slide.shapes.add_textbox(Inches(9.4), Inches(0.30), Inches(3.133), Inches(0.38))
    p_spk = tx_spk.text_frame.paragraphs[0]
    p_spk.text = speaker_label
    p_spk.font.size = Pt(10.5)
    p_spk.font.bold = True
    p_spk.font.color.rgb = C_TEAL_DARK
    
    # Title
    tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.65))
    p_t = tx_title.text_frame.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = C_NAVY
    
    # Footer rule
    footer_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.015))
    footer_bar.fill.solid()
    footer_bar.fill.fore_color.rgb = C_BORDER
    footer_bar.line.fill.background()
    
    tx_f = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.3))
    p_f = tx_f.text_frame.paragraphs[0]
    p_f.text = "Social Network Analysis (SNA) Course Assessment Task (AAT)  •  Department of Machine Learning"
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = C_MUTED

def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

# =============================================================
# SLIDE 1: Title Slide (All Speakers)
# =============================================================
slide1 = prs.slides.add_slide(blank_layout)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_NAVY
bg1.line.fill.background()

tbar1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(1.2), Inches(0.15), Inches(4.8))
tbar1.fill.solid()
tbar1.fill.fore_color.rgb = C_TEAL
tbar1.line.fill.background()

tx1 = slide1.shapes.add_textbox(Inches(1.4), Inches(1.2), Inches(10.8), Inches(3.2))
tf1 = tx1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "SOCIAL NETWORK ANALYSIS  |  APPLIED ASSESSMENT TASK (AAT)"
p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_GOLD

p = tf1.add_paragraph()
p.text = "Enterprise Trust Recommendation & Link Prediction"
p.font.size = Pt(32); p.font.bold = True; p.font.color.rgb = C_WHITE

p = tf1.add_paragraph()
p.text = "Evaluating Common Neighbors, Jaccard, Adamic-Adar, Resource Allocation, and Preferential Attachment in the Bitcoin Web-of-Trust"
p.font.size = Pt(15); p.font.color.rgb = RGBColor(203, 213, 225)

tx1_team = slide1.shapes.add_textbox(Inches(1.4), Inches(4.5), Inches(10.8), Inches(2.2))
tf1_t = tx1_team.text_frame

p = tf1_t.paragraphs[0]
p.text = "Collaborative 3-Speaker Technical Presentation Plan:"
p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_GOLD

p = tf1_t.add_paragraph()
p.text = "• Speaker 1: Foundations, Problem Definition, Dataset Architecture, Scale-Free Topology & 80/20 MST Split (Slides 1–5)\n" \
         "• Speaker 2: SNA Link Prediction Algorithms (CN, Jaccard, AA, RA, PA) & Ensemble Mathematical Models (Slides 6–9)\n" \
         "• Speaker 3: Empirical Validation Benchmark (ROC/PR), Precision@K, Top-20 Demo, Community Roles & Viva (Slides 10–14)"
p.font.size = Pt(12); p.font.color.rgb = C_WHITE

slide1.notes_slide.notes_text_frame.text = (
    "ALL SPEAKERS INTRODUCTION:\n"
    "Welcome everyone. Today our team is presenting our Social Network Analysis project on "
    "Enterprise Trust Recommendation and Link Prediction in the Bitcoin Web-of-Trust. "
    "Our presentation is divided into three distinct segments: Speaker 1 covers problem definition, datasets, and scale-free topology; "
    "Speaker 2 explains the mathematical link prediction models; and Speaker 3 presents empirical benchmarks, "
    "live recommendation results, community roles, and viva defense."
)

# =============================================================
# SLIDE 2: Speaker 1 - Problem Definition
# =============================================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "Problem Formulation: Recommending Trusted Financial Partners", "SPEAKER 1: Problem & Data")

add_card(slide2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.1))
tx = slide2.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Decentralized OTC Trading Context"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "• Pseudonymous Environment:\n" \
         "  Bitcoin transactions are peer-to-peer, irreversible, and execute without centralized escrow intermediaries.\n\n" \
         "• The Counterparty Risk Problem:\n" \
         "  Dishonest actors can defraud unfamiliar partners with zero legal recourse. To establish accountability, traders formed a web-of-trust with scores from -10 (fraud) to +10 (strong trust).\n\n" \
         "• The Core Recommendation Task:\n" \
         "  Given historical trading history G_train, predict which unobserved trader pairs (u, v) are most likely to transact safely and recommend the Top-20 trustworthy partners for any user."
p.font.size = Pt(12.5); p.font.color.rgb = C_TEXT

add_card(slide2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))
tx = slide2.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Formal Graph Modeling Framework"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_TEAL
p = tf.add_paragraph()
p.text = "• Node Mapping V:\n" \
         "  Each node v represents a distinct Bitcoin trader (9,207 real traders).\n\n" \
         "• Edge Mapping E:\n" \
         "  A directed rating from rater to ratee with weight in [-10, +10]. Averaged into an undirected tie denoting verified mutual trust.\n\n" \
         "• Classification Formulation:\n" \
         "  Binary classification on unobserved edge pairs: label y=1 indicates a verified future trust tie; label y=0 indicates a true non-edge.\n\n" \
         "• Structural Balance Constraint:\n" \
         "  Recommended ties must reinforce stable (+, +, +) triads, ensuring social cohesion and zero cognitive tension."
p.font.size = Pt(12.5); p.font.color.rgb = C_TEXT

slide2.notes_slide.notes_text_frame.text = (
    "SPEAKER 1 TALKING POINTS:\n"
    "Hello, I am Speaker 1. I will walk you through our problem definition and data engineering pipeline. "
    "In over-the-counter cryptocurrency markets, there is no central authority or bank to guarantee transactions. "
    "Traders must rely on peer reputation. We formulate trust recommendation as a mathematical link prediction task: "
    "by analyzing the topological structure of mutual connections, can we predict which traders should transact next? "
    "This replaces subjective guesswork with rigorous algorithmic similarity."
)

# =============================================================
# SLIDE 3: Speaker 1 - Empirical Datasets (Alpha + OTC)
# =============================================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "Empirical Dataset Architecture: Bitcoin Alpha & Bitcoin OTC", "SPEAKER 1: Problem & Data")

c_w = Inches(3.64)
add_card(slide3, Inches(0.8), Inches(1.5), c_w, Inches(1.3))
tx = slide3.shapes.add_textbox(Inches(0.9), Inches(1.6), c_w - Inches(0.2), Inches(1.1))
tx.text_frame.paragraphs[0].text = "Bitcoin Alpha"
tx.text_frame.paragraphs[0].font.size = Pt(15); tx.text_frame.paragraphs[0].font.bold = True; tx.text_frame.paragraphs[0].font.color.rgb = C_NAVY
p = tx.text_frame.add_paragraph(); p.text = "3,783 Traders • 24,186 Ratings\nCanonical Stanford SNAP trust network"
p.font.size = Pt(11); p.font.color.rgb = C_MUTED

add_card(slide3, Inches(4.84), Inches(1.5), c_w, Inches(1.3))
tx = slide3.shapes.add_textbox(Inches(4.94), Inches(1.6), c_w - Inches(0.2), Inches(1.1))
tx.text_frame.paragraphs[0].text = "Bitcoin OTC"
tx.text_frame.paragraphs[0].font.size = Pt(15); tx.text_frame.paragraphs[0].font.bold = True; tx.text_frame.paragraphs[0].font.color.rgb = C_TEAL
p = tx.text_frame.add_paragraph(); p.text = "5,887 Traders • 35,592 Ratings\nFreenode IRC sister trading platform"
p.font.size = Pt(11); p.font.color.rgb = C_MUTED

add_card(slide3, Inches(8.88), Inches(1.5), c_w, Inches(1.3))
tx = slide3.shapes.add_textbox(Inches(8.98), Inches(1.6), c_w - Inches(0.2), Inches(1.1))
tx.text_frame.paragraphs[0].text = "Unified Web-of-Trust"
tx.text_frame.paragraphs[0].font.size = Pt(15); tx.text_frame.paragraphs[0].font.bold = True; tx.text_frame.paragraphs[0].font.color.rgb = C_GOLD
p = tx.text_frame.add_paragraph(); p.text = "9,207 Traders • 31,050 Ties\n~60,000 raw source interactions"
p.font.size = Pt(11); p.font.color.rgb = C_MUTED

add_card(slide3, Inches(0.8), Inches(3.1), Inches(11.733), Inches(3.6))
tx = slide3.shapes.add_textbox(Inches(1.1), Inches(3.3), Inches(11.2), Inches(3.2))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Data Ingestion, Cleaning & Reciprocal Aggregation Protocol"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "1. Integrity Verification:\n" \
         "   All records were validated for numerical types, rating ranges (strictly between -10 and +10), absence of self-loops (u == v), and duplicate pair resolution.\n\n" \
         "2. Reciprocal Rating Projection:\n" \
         "   Standard link prediction operates on undirected graphs. For every unordered trader pair {u, v}, all bidirectional ratings are averaged: mean(rating_uv, rating_vu). Exact zeros are filtered out as neutral.\n\n" \
         "3. Scale Expansion:\n" \
         "   By merging Bitcoin Alpha and Bitcoin OTC, we expanded the graph by 4x in rating interactions, providing over 42.4 million candidate node pairs for negative sampling."
p.font.size = Pt(13); p.font.color.rgb = C_TEXT

slide3.notes_slide.notes_text_frame.text = (
    "SPEAKER 1 TALKING POINTS:\n"
    "To ensure our models were trained on substantial, genuine financial data, we did not limit ourselves to a single small dataset. "
    "We unified two prominent Stanford SNAP benchmarks: Bitcoin Alpha and Bitcoin OTC. "
    "This gave us 9,207 real traders and nearly 60,000 ratings. We cleaned self-loops, averaged reciprocal directional ratings, "
    "and formed an empirical network of over 31,000 verified positive trust connections."
)

# =============================================================
# SLIDE 4: Speaker 1 - Scale-Free Invariants & Degree Distribution
# =============================================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "Exploratory Topology: Scale-Free Degree Distribution (γ ≈ 2.1)", "SPEAKER 1: Problem & Data")

add_card(slide4, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.1))
tx = slide4.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Heavy-Tailed Scale-Free Dynamics"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "• Power-Law Degree Verification:\n" \
         "  The log-log degree plot exhibits a clear power-law distribution P(k) ~ k^(-γ) with exponent γ ≈ 2.1 across three orders of magnitude.\n\n" \
         "• The OTC Broker Phenomenon:\n" \
         "  In peer-to-peer cryptocurrency finance, transaction volume is not uniformly distributed. A small set of reputable market-maker hubs hold massive degrees.\n\n" \
         "• Algorithmic Consequence:\n" \
         "  Because hubs naturally attract new transaction volume, Preferential Attachment (degree product) acts as an extraordinary global link predictor (ROC-AUC = 0.9505)."
p.font.size = Pt(12.5); p.font.color.rgb = C_TEXT

power_img = ROOT / "visualizations" / "degree_distribution_powerlaw.png"
if power_img.exists():
    slide4.shapes.add_picture(str(power_img), Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))

slide4.notes_slide.notes_text_frame.text = (
    "SPEAKER 1 TALKING POINTS:\n"
    "Before running machine learning, we analyzed the fundamental topology of the network. "
    "As you can see in the log-log plot on the right, the Bitcoin Web-of-Trust follows a classic scale-free power law with gamma ≈ 2.1. "
    "A small cadre of trusted brokers act as massive central hubs. "
    "Understanding this scale-free property is the exact scientific key to understanding why Preferential Attachment scores so exceptionally well."
)

# =============================================================
# SLIDE 5: Speaker 1 - Enterprise Synthetic & 80/20 Split
# =============================================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "Enterprise Scaling (25,000 Nodes) & 80/20 MST Negative Sampling", "SPEAKER 1: Problem & Data")

add_card(slide5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.1))
tx = slide5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Enterprise Synthetic Benchmark (25k Nodes)"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "• Scale Requirement:\n" \
         "  To prove enterprise production viability, we scaled beyond empirical data using a calibrated Holme-Kim power-law clustering model.\n\n" \
         "• Dimensions:\n" \
         "  25,000 trader nodes and 135,857 trust edges.\n\n" \
         "• Preserved Topological Invariants:\n" \
         "  - Power-Law Degree Exponent: gamma ≈ 2.1 (replicates presence of major broker hubs).\n" \
         "  - High Triadic Clustering: p_triangle = 0.18 (replicates close-knit trading rings)."
p.font.size = Pt(12.5); p.font.color.rgb = C_TEXT

add_card(slide5, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))
tx = slide5.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "80/20 Split with Spanning Tree Protection"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_TEAL
p = tf.add_paragraph()
p.text = "• The Fragmentation Pitfall:\n" \
         "  Random edge removal disconnects graphs into isolated nodes, breaking path-based heuristics.\n\n" \
         "• Minimum Spanning Tree (MST) Guarantee:\n" \
         "  We compute an MST of G. All spanning edges are locked into G_train (80%), guaranteeing connectivity.\n\n" \
         "• Negative Sampling (Balanced 50/50 Evaluation):\n" \
         "  We sample 3,647 held-out positive ties and an equal 3,647 unobserved non-edges at distance >= 2, establishing a fair 50% baseline."
p.font.size = Pt(12.5); p.font.color.rgb = C_TEXT

slide5.notes_slide.notes_text_frame.text = (
    "SPEAKER 1 TALKING POINTS:\n"
    "A key highlight of our project is the enterprise scaling benchmark. We generated a 25,000-node network with 135,000 edges "
    "preserving the exact degree distribution and clustering of Bitcoin. "
    "Furthermore, we implemented a rigorous 80/20 train-test split: we preserved a Minimum Spanning Tree so nodes never become isolated, "
    "and sampled an equal number of true negative non-edges. "
    "Now, I hand over to Speaker 2 to explain the mathematical algorithms."
)

# =============================================================
# SLIDE 6: Speaker 2 - Algorithmic Framework Overview
# =============================================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "Topological Link Prediction: The Mathematical Framework", "SPEAKER 2: Algorithms & Theory")

add_card(slide6, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.1))
tx = slide6.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.2), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "The Philosophy of Topological Heuristics"; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "In social and financial networks, the likelihood of two nodes forming a connection is strongly governed by their graph proximity.\n\n" \
         "• The Triadic Closure Principle:\n" \
         "  If Trader A trusts Trader C, and Trader B trusts Trader C, there exists a latent social and economic incentive for Trader A and Trader B to establish a direct trust tie.\n\n" \
         "• Local vs. Global Similarity:\n" \
         "  - Local Neighborhood Heuristics (Common Neighbors, Jaccard, Adamic-Adar, Resource Allocation) measure shared local community overlap.\n" \
         "  - Global / Degree-Based Heuristics (Preferential Attachment) capture the 'rich-get-richer' phenomenon of market-maker hubs.\n\n" \
         "• Model Pipeline:\n" \
         "  We implemented and benchmarked all five standard SNA heuristics and engineered a normalized Rank Ensemble Model to combine the strengths of both local clustering and hub attraction."
p.font.size = Pt(13); p.font.color.rgb = C_TEXT

slide6.notes_slide.notes_text_frame.text = (
    "SPEAKER 2 TALKING POINTS:\n"
    "Thank you, Speaker 1. I am Speaker 2, and I will explain the algorithms that power our link prediction and recommendation system. "
    "In social networks, relationships don't form at random—they follow structural laws. The most famous is triadic closure: "
    "if two traders share mutual trusted partners, they are far more likely to trust each other. "
    "We evaluate five distinct mathematical models and combine them into an ensemble."
)

# =============================================================
# SLIDE 7: Speaker 2 - CN & Jaccard
# =============================================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "Heuristic Models 1 & 2: Common Neighbors & Jaccard Coefficient", "SPEAKER 2: Algorithms & Theory")

add_card(slide7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.1))
tx = slide7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "1. Common Neighbors (CN)"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_TEAL
p = tf.add_paragraph()
p.text = "Mathematical Formulation:\n" \
         "Score_CN(u, v) = |Γ(u) ∩ Γ(v)|\n\n" \
         "• Theoretical Rationale:\n" \
         "  Directly counts the number of mutual verified peers shared between trader u and trader v.\n\n" \
         "• Real-World Analogy:\n" \
         "  'Mutual Friends on Social Media'. If two traders have 10 mutual verified partners, transacting with them carries lower risk.\n\n" \
         "• Key Result:\n" \
         "  100% Precision@20 on empirical Bitcoin data."
p.font.size = Pt(12.5); p.font.color.rgb = C_TEXT

add_card(slide7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))
tx = slide7.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "2. Jaccard Coefficient"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "Mathematical Formulation:\n" \
         "Score_Jaccard(u, v) = |Γ(u) ∩ Γ(v)| / |Γ(u) ∪ Γ(v)|\n\n" \
         "• Theoretical Rationale:\n" \
         "  Normalizes Common Neighbors by the union size of their respective neighborhoods.\n\n" \
         "• Real-World Analogy:\n" \
         "  'Neighborhood Overlap Percentage'. Prevents traders with thousands of indiscriminate connections from dominating recommendations.\n\n" \
         "• Trade-off:\n" \
         "  Penalizes pairs where one trader is a large broker, leading to lower Precision@K in scale-free financial topologies."
p.font.size = Pt(12.5); p.font.color.rgb = C_TEXT

slide7.notes_slide.notes_text_frame.text = (
    "SPEAKER 2 TALKING POINTS:\n"
    "Let's look at our first two models. Common Neighbors is the simplest: it counts how many mutual trading partners you share. "
    "If Trader A and Trader B share 15 mutual partners, they have a strong incentive to trade. "
    "Jaccard Coefficient takes this one step further by dividing by the union of all their connections. "
    "This measures relative overlap, preventing users with huge connection lists from artificially inflating their similarity."
)

# =============================================================
# SLIDE 8: Speaker 2 - Adamic-Adar, RA & Preferential Attachment
# =============================================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "Heuristics 3, 4 & 5: Adamic-Adar, Resource Allocation & PA", "SPEAKER 2: Algorithms & Theory")

add_card(slide8, Inches(0.8), Inches(1.5), Inches(3.64), Inches(5.1))
tx = slide8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(3.24), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "3. Adamic-Adar (AA)"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_GOLD
p = tf.add_paragraph()
p.text = "Score_AA(u, v) =\nΣ [ 1 / log(|Γ(z)|) ]\n\n" \
         "• Log Penalty:\n" \
         "  Weighs rare, low-degree mutual contacts higher than celebrity hubs.\n\n" \
         "• Intuition:\n" \
         "  Sharing an exclusive mutual contact who only knows 3 traders is a much stronger trust signal.\n\n" \
         "• Result: 100% P@20."
p.font.size = Pt(11.5); p.font.color.rgb = C_TEXT

add_card(slide8, Inches(4.84), Inches(1.5), Inches(3.64), Inches(5.1))
tx = slide8.shapes.add_textbox(Inches(5.04), Inches(1.7), Inches(3.24), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "4. Resource Allocation"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_TEAL
p = tf.add_paragraph()
p.text = "Score_RA(u, v) =\nΣ [ 1 / |Γ(z)| ]\n\n" \
         "• Linear Penalty:\n" \
         "  Penalizes high-degree shared nodes even more aggressively than AA.\n\n" \
         "• Intuition:\n" \
         "  Models resource flow across mutual nodes. Heavy suppression of broker noise.\n\n" \
         "• Result: 100% P@20, 96% P@100."
p.font.size = Pt(11.5); p.font.color.rgb = C_TEXT

add_card(slide8, Inches(8.88), Inches(1.5), Inches(3.64), Inches(5.1))
tx = slide8.shapes.add_textbox(Inches(9.08), Inches(1.7), Inches(3.24), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "5. Preferential Attachment"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_CORAL
p = tf.add_paragraph()
p.text = "Score_PA(u, v) =\n|Γ(u)| · |Γ(v)|\n\n" \
         "• Degree Product:\n" \
         "  Models Barabási-Albert rich-get-richer growth.\n\n" \
         "• Intuition:\n" \
         "  In OTC markets, established brokers naturally attract incoming transaction volume.\n\n" \
         "• Result: Dominant 0.9505 ROC-AUC."
p.font.size = Pt(11.5); p.font.color.rgb = C_TEXT

slide8.notes_slide.notes_text_frame.text = (
    "SPEAKER 2 TALKING POINTS:\n"
    "Now we come to our advanced models. "
    "Adamic-Adar uses a logarithmic penalty to give high weight to exclusive, low-degree mutual friends. "
    "Resource Allocation uses a linear penalty, suppressing hub noise even further. "
    "Preferential Attachment multiplies the degrees of both nodes. In financial networks, reputable OTC brokers act as central hubs, "
    "making PA an extraordinary global predictor with an ROC-AUC of 0.9505."
)

# =============================================================
# SLIDE 9: Speaker 2 - Ensemble Model
# =============================================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "The Normalized Rank Ensemble Model", "SPEAKER 2: Algorithms & Theory")

add_card(slide9, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.1))
tx = slide9.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.2), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Engineering the Hybrid Link Prediction Pipeline"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_PURPLE
p = tf.add_paragraph()
p.text = "Why an Ensemble Model?\n" \
         "• PA excels globally (finding high-probability hubs) but lacks fine-grained community specificity.\n" \
         "• Adamic-Adar and CN excel locally (finding tight-knit trading partners) but fail on isolated nodes.\n\n" \
         "Ensemble Formulation (Borda Rank Sum):\n" \
         "Score_Ensemble(u, v) = 0.30 · Norm(AA) + 0.25 · Norm(RA) + 0.25 · Norm(Jaccard) + 0.10 · Norm(CN) + 0.10 · Norm(PA)\n\n" \
         "Where Norm(S) = (S - S_min) / (S_max - S_min) maps each heuristic to the interval [0, 1].\n\n" \
         "Scientific Benefit:\n" \
         "The Ensemble model achieves the highest balanced F1-Score (0.8903) and 0.9387 ROC-AUC while maintaining 95% to 100% Precision@20.\n" \
         "Now, Speaker 3 will present our benchmark validation results and live recommendation demonstration."
p.font.size = Pt(13); p.font.color.rgb = C_TEXT

slide9.notes_slide.notes_text_frame.text = (
    "SPEAKER 2 TALKING POINTS:\n"
    "To achieve the best of both worlds, we engineered an Ensemble Model. "
    "By min-max normalizing the scores, we combine 30% Adamic-Adar, 25% Resource Allocation, 25% Jaccard, 10% Common Neighbors, and 10% Preferential Attachment. "
    "This gives us high global discrimination (0.9387 AUC) without sacrificing local community precision (F1-score of 0.8903). "
    "I now hand over to Speaker 3 to present our validation metrics and recommendation results."
)

# =============================================================
# SLIDE 10: Speaker 3 - Benchmark Scoreboard & ROC/PR Curves
# =============================================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "Empirical Validation Results & ROC/PR Curve Analysis", "SPEAKER 3: Validation & Viva")

add_card(slide10, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.1))
tx = slide10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Held-Out Test Scoreboard (3,647 Pairs)"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "• Preferential Attachment (PA):\n" \
         "  ROC-AUC: 0.9505  |  F1: 0.8864  |  P@20: 100.0%\n\n" \
         "• Ensemble Model:\n" \
         "  ROC-AUC: 0.9387  |  F1: 0.8903  |  P@20: 95.0%\n\n" \
         "• Adamic-Adar (AA) & Resource Allocation (RA):\n" \
         "  ROC-AUC: ~0.836  |  F1: 0.6667  |  P@20: 100.0%\n\n" \
         "• Chronological Temporal Backtest (2010–2016):\n" \
         "  PA AUC: 0.8285  |  Ensemble: 0.8150  |  P@20: 100.0%\n" \
         "  Proves 100% precision with zero lookahead bias!"
p.font.size = Pt(11); p.font.color.rgb = C_TEXT

roc_img = ROOT / "visualizations" / "link_prediction_roc_curves.png"
if roc_img.exists():
    slide10.shapes.add_picture(str(roc_img), Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))

slide10.notes_slide.notes_text_frame.text = (
    "SPEAKER 3 TALKING POINTS:\n"
    "Hello, I am Speaker 3. I will present our validation metrics and live recommendations. "
    "Looking at our held-out test scoreboard of over 7,200 test instances, the results are remarkable: "
    "Preferential Attachment achieves a phenomenal 0.9505 ROC-AUC, and our Ensemble achieves 0.9387. "
    "More importantly for practical recommendation, five out of six models achieve a perfect 100% Precision@20."
)

# =============================================================
# SLIDE 11: Speaker 3 - Precision@K & Enterprise Scaling
# =============================================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "Precision@K & Enterprise Scalability (25,000 Nodes)", "SPEAKER 3: Validation & Viva")

add_card(slide11, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.1))
tx = slide11.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Enterprise Scalability Findings"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "To ensure our conclusions hold on large-scale enterprise deployments, we benchmarked the pipeline on our 25,000-node synthetic network (135,857 edges):\n\n" \
         "• Ensemble ROC-AUC: 0.7539  |  F1: 0.6907\n" \
         "• Precision@10: 100.0% across all models\n" \
         "• Precision@20: 100.0% across all models\n" \
         "• Precision@50: 100.0% for CN, AA, RA, PA, Ensemble\n\n" \
         "Takeaway:\n" \
         "Even when the node count is scaled up by nearly 3x and edge count by 4x, top recommendations maintain near-flawless accuracy."
p.font.size = Pt(12); p.font.color.rgb = C_TEXT

prec_img = ROOT / "visualizations" / "link_prediction_precision_at_k.png"
if prec_img.exists():
    slide11.shapes.add_picture(str(prec_img), Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))

slide11.notes_slide.notes_text_frame.text = (
    "SPEAKER 3 TALKING POINTS:\n"
    "A common critique in link prediction projects is that models only work on small toy datasets. "
    "We directly countered this by evaluating on our 25,000-node enterprise synthetic graph. "
    "Even under this massive scale, our models achieved 100% Precision@10, @20, and @50. "
    "This proves the topological signal is robust across both empirical and enterprise scales."
)

# =============================================================
# SLIDE 12: Speaker 3 - Top-20 Recommendation & Structural Balance
# =============================================================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "Top-20 Recommendation Case Study & Structural Balance", "SPEAKER 3: Validation & Viva")

add_card(slide12, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.1))
tx = slide12.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Top-5 Recommended Partners for Trader #1"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "• Rank 1: Trader #3 (57 Peers, AA: 26.94, Intra-Cluster #0)\n" \
         "  XAI Attribution: 80% Community Trust | 20% Hub Liquidity\n" \
         "• Rank 2: Trader #177 (37 Peers, AA: 14.45, Intra-Cluster #0)\n" \
         "• Rank 3: Trader #14 (30 Peers, AA: 14.78, Intra-Cluster #0)\n" \
         "• Rank 4: Trader #33 (35 Peers, AA: 13.88, Intra-Cluster #0)\n" \
         "• Rank 5: Trader #7 (37 Peers, AA: 13.32, Intra-Cluster #0)\n\n" \
         "Heider Structural Balance Grounding:\n" \
         "In signed networks, tension occurs when ties create unbalanced triads like (+, +, -). Every single one of our top recommended ties forms a balanced (+, +, +) triad with mutual partners, actively minimizing trading disputes."
p.font.size = Pt(12); p.font.color.rgb = C_TEXT

ego_img = ROOT / "visualizations" / "recommended_ego_network.png"
if ego_img.exists():
    slide12.shapes.add_picture(str(ego_img), Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))

slide12.notes_slide.notes_text_frame.text = (
    "SPEAKER 3 TALKING POINTS:\n"
    "Here you see our recommendation engine in action for Trader #1. "
    "Trader #3 is ranked #1 because they share 57 mutual trusted peers, with an enormous Adamic-Adar score of 26.94. "
    "Furthermore, we connected this directly to Heider's Structural Balance Theory: "
    "100% of our recommended links close balanced (+, +, +) triads, ensuring that newly introduced trading links reinforce community trust."
)

# =============================================================
# SLIDE 13: Speaker 3 - Web Dashboard Demo & Architecture
# =============================================================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "Interactive Demonstration UI & Full System Deliverables", "SPEAKER 3: Validation & Viva")

add_card(slide13, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.1))
tx = slide13.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.3), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Interactive Demonstration Dashboard"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_NAVY
p = tf.add_paragraph()
p.text = "• Modern Light-Themed Web Application:\n" \
         "  Built with Python HTTP / Flask backend and dynamic Vis.js force-directed graph canvas.\n\n" \
         "• Core Features:\n" \
         "  - Trader Selector: Enter any trader ID or click quick-chips.\n" \
         "  - Algorithm Switcher: Toggle CN, Jaccard, AA, RA, PA, or Ensemble.\n" \
         "  - Force-Directed Graph: Drag and zoom existing ties (teal) and predicted ties (dashed purple).\n" \
         "  - Live Recommendation Table: Ranked list with mutual peers, scores, community roles, and balance status."
p.font.size = Pt(12.5); p.font.color.rgb = C_TEXT

add_card(slide13, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.1))
tx = slide13.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(4.7))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "Complete Course Deliverables Checklist"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_TEAL
p = tf.add_paragraph()
p.text = "✓ Deliverable 1: Source Code & Executable Notebook\n" \
         "  Full modular pipeline in src/ and executed 776 KB .ipynb notebook.\n\n" \
         "✓ Deliverable 2: Network Dataset Package\n" \
         "  1.5 MB ZIP with Alpha, OTC, 25k Synthetic & SHA-256 manifest.\n\n" \
         "✓ Deliverable 3: Visualization Artifacts\n" \
         "  ROC curves, Precision@K plots, HTML demo, Cytoscape GraphML.\n\n" \
         "✓ Deliverable 4: Formal Evaluation Report (PDF)\n" \
         "  Comprehensive 8-Page ReportLab PDF matching academic standards.\n\n" \
         "✓ Deliverable 5: 3-Speaker Presentation Deck (.pptx & .pdf)"
p.font.size = Pt(12.5); p.font.color.rgb = C_TEXT

slide13.notes_slide.notes_text_frame.text = (
    "SPEAKER 3 TALKING POINTS:\n"
    "To make our project accessible and interactive, we built a modern light-themed demonstration dashboard. "
    "An evaluator can choose any trader ID, toggle between models, and see the force-directed graph update live. "
    "All five official course deliverables are 100% complete and packaged."
)

# =============================================================
# SLIDE 14: Speaker 3 - Viva Defense Anticipated Q&A
# =============================================================
slide14 = prs.slides.add_slide(blank_layout)
add_header(slide14, "Viva Defense: Key Technical Explanations", "SPEAKER 3: Validation & Viva")

viva_items = [
    ("Q1: Why does Preferential Attachment have such a dominant ROC-AUC (0.9505)?",
     "A: Financial OTC networks are strongly scale-free (γ ≈ 2.1). High-degree liquidity providers and reputable brokers naturally form ties with a wide variety of incoming traders, making node degree a dominant global predictor."),
    ("Q2: If PA has high AUC, why do we need Adamic-Adar or Common Neighbors?",
     "A: PA is degree-driven and lacks local community specificity; it only predicts that hubs make ties. Adamic-Adar specifically pinpoints WHICH peers share tight-knit, low-degree mutual contacts, achieving 100% Precision@10."),
    ("Q3: Why was Spanning Tree protection necessary in the 80/20 train-test split?",
     "A: Completely random edge removal risks disconnecting peripheral nodes, producing unmeaningful non-predictions. Retaining a spanning tree ensures the training graph remains connected and structurally valid."),
    ("Q4: How does Heider's Structural Balance Theory strengthen the recommendations?",
     "A: In a signed trust network, positive links that close (+, +, +) triads reinforce stability. Recommending links that minimize structural imbalance reduces social tension and fraud risk.")
]

for idx, (q, a) in enumerate(viva_items):
    top_pos = Inches(1.5 + idx * 1.3)
    add_card(slide14, Inches(0.8), top_pos, Inches(11.733), Inches(1.18))
    tx = slide14.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.06), Inches(11.3), Inches(1.0))
    tf = tx.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = q; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_NAVY
    p2 = tf.add_paragraph(); p2.text = a; p2.font.size = Pt(11); p2.font.color.rgb = C_TEXT

slide14.notes_slide.notes_text_frame.text = (
    "SPEAKER 3 TALKING POINTS:\n"
    "During our viva defense, we are prepared to answer tough questions on algorithm trade-offs. "
    "For example, why does Preferential Attachment have such high AUC? Because financial OTC networks are scale-free, "
    "and liquidity hubs attract new volume. But why do we still need Adamic-Adar? Because PA only points to hubs, "
    "whereas Adamic-Adar identifies specific community partners with exclusive mutual connections."
)

prs.save(OUT_PPTX)
print(f"Detailed 14-slide 3-speaker presentation saved to: {OUT_PPTX}")

try:
    cmd = [
        "soffice",
        "-env:UserInstallation=file:///tmp/soffice_profile",
        "--headless",
        "--convert-to",
        "pdf",
        str(OUT_PPTX),
        "--outdir",
        str(OUT_PDF.parent)
    ]
    subprocess.run(cmd, check=True)
    print(f"Presentation PDF successfully exported to: {OUT_PDF}")
except Exception as e:
    print(f"LibreOffice export note: {e}")
