"""Generate a clean printable PDF of the Team Study Guide."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable

ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "reports" / "team_presentation_study_guide.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocTitle", fontSize=18, leading=22, textColor=colors.HexColor("#0F172A"), fontName="Helvetica-Bold", spaceAfter=6))
styles.add(ParagraphStyle(name="DocSub", fontSize=10, leading=14, textColor=colors.HexColor("#0D9488"), fontName="Helvetica-Bold", spaceAfter=10))
styles.add(ParagraphStyle(name="SecH1", fontSize=13, leading=16, textColor=colors.HexColor("#0F172A"), fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="SecH2", fontSize=10, leading=13, textColor=colors.HexColor("#0D9488"), fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=2, keepWithNext=True))
styles.add(ParagraphStyle(name="GuideBody", fontSize=8, leading=11.5, textColor=colors.HexColor("#1E293B"), spaceAfter=3))
styles.add(ParagraphStyle(name="GuideCallout", fontSize=8, leading=11.5, textColor=colors.HexColor("#0F172A"), backColor=colors.HexColor("#F8FAFC"), borderColor=colors.HexColor("#0D9488"), borderWidth=0.8, borderPadding=5, spaceBefore=4, spaceAfter=4))

doc = SimpleDocTemplate(str(OUT_PDF), pagesize=A4, rightMargin=16*mm, leftMargin=16*mm, topMargin=15*mm, bottomMargin=15*mm)
story = []

def p(text, style="GuideBody"):
    return Paragraph(text, styles[style])

story += [
    p("BITCOIN WEB-OF-TRUST: SNA APPLIED ASSESSMENT TASK", "DocSub"),
    p("Team Presentation & Viva Study Guide (3-Speaker Plan)", "DocTitle"),
    HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0D9488"), spaceBefore=2, spaceAfter=6),
    p("<b>The 60-Second Elevator Pitch:</b> In OTC cryptocurrency markets, anonymous traders face extreme fraud risk because trades are irreversible and have no escrow. We formulate trust recommendation as a topological link prediction task on the Bitcoin Web-of-Trust. Using four fundamental heuristics (Common Neighbors, Jaccard, Adamic-Adar, Preferential Attachment) and a normalized rank ensemble, our models predict future trading partners with 0.9505 ROC-AUC and 100% Precision@20, evaluated across 9,207 real traders (~60k ratings) and a 25,000-node enterprise synthetic network. 100% of recommended ties satisfy Heider's Structural Balance by completing (+, +, +) triads.", "GuideCallout"),
    Spacer(1, 3*mm),
    p("1. Who Presents What: 3-Speaker Slide Division across 14 Slides", "SecH1"),
    p("<b>SPEAKER 1: Slides 1 – 5 (Problem Definition, Data Engineering, Scale-Free Topology & 80/20 Split)</b><br/>"
      "• <i>Slide 1:</i> Introduce the team, project title, and structure.<br/>"
      "• <i>Slide 2:</i> Explain OTC counterparty risk, anonymous trading, ratings from -10 to +10, and why link prediction is the ideal formulation.<br/>"
      "• <i>Slide 3:</i> Explain that we combined Stanford SNAP Bitcoin Alpha (3,783 users) and Bitcoin OTC (5,887 users) into 9,207 real traders and ~60k ratings.<br/>"
      "• <i>Slide 4:</i> Present the log-log scale-free degree distribution fit (P(k) ~ k^(-2.1)) and explain why broker hubs drive Preferential Attachment accuracy.<br/>"
      "• <i>Slide 5:</i> Present the 25k-node enterprise synthetic scaling (Holme-Kim model), 80/20 train-test split, Minimum Spanning Tree protection, and balanced 50/50 negative sampling.", "GuideBody"),
    Spacer(1, 2*mm),
    p("<b>SPEAKER 2: Slides 6 – 9 (Link Prediction Algorithms & Mathematical Formulations)</b><br/>"
      "• <i>Slide 6:</i> Introduce the philosophy of topological heuristics and triadic closure (a friend of my friend is my friend).<br/>"
      "• <i>Slide 7:</i> Explain Common Neighbors (|Γ(u) ∩ Γ(v)|; 'mutual friends') and Jaccard (|Common| / |Union|; 'neighborhood overlap %').<br/>"
      "• <i>Slide 8:</i> Explain Adamic-Adar (log degree penalty; 'exclusive introductions'), Resource Allocation (linear degree penalty), and Preferential Attachment (deg_u × deg_v; 'market maker liquidity hub' analogy; 0.9505 AUC).<br/>"
      "• <i>Slide 9:</i> Present the Normalized Rank Ensemble Model combining 30% AA + 25% RA + 25% Jaccard + 10% CN + 10% PA.", "GuideBody"),
    Spacer(1, 2*mm),
    p("<b>SPEAKER 3: Slides 10 – 14 (Benchmark Results, Top-20 Demo, Community Roles & Viva)</b><br/>"
      "• <i>Slide 10:</i> Present the test scoreboard: Preferential Attachment (0.9505 AUC), Ensemble (0.9387 AUC), and 100% Precision@20 on local heuristics.<br/>"
      "• <i>Slide 11:</i> Present the Enterprise Scaling chart: 0.7539 AUC and 100% Precision@10 and @20 on 25k nodes.<br/>"
      "• <i>Slide 12:</i> Walk through the live Top-20 recommendations for Trader #1. Explain Community Roles (Intra-Cluster vs Inter-Cluster Bridge) and prove 100% (+, +, +) triad closure under Heider's Structural Balance Theory.<br/>"
      "• <i>Slide 13:</i> Showcase the interactive web UI and complete checklist of the 5 official course deliverables.<br/>"
      "• <i>Slide 14:</i> Deliver the viva defense summary and conclude the presentation.", "GuideBody"),
    PageBreak(),
    p("2. Key Numbers to Memorize for Viva", "SecH1"),
    p("• <b>Real Data:</b> 9,207 traders, 31,050 verified ties, ~60,000 ratings (Alpha + OTC combined).<br/>"
      "• <b>Enterprise Synthetic Data:</b> 25,000 nodes, 135,857 ties (Holme-Kim power-law clustering model).<br/>"
      "• <b>Train-Test Split:</b> 80% train / 20% test with Minimum Spanning Tree protection.<br/>"
      "• <b>Evaluation Size:</b> 3,647 positive test ties + 3,647 negative non-edges = 7,294 test instances.<br/>"
      "• <b>Top ROC-AUC:</b> 0.9505 (Preferential Attachment) and 0.9387 (Ensemble Model).<br/>"
      "• <b>Top-20 Precision:</b> 100.0% across PA, AA, and Common Neighbors.<br/>"
      "• <b>Structural Balance:</b> 100% of recommended links form balanced (+, +, +) triads.", "GuideCallout"),
    Spacer(1, 2*mm),
    p("3. Top 5 Viva Questions & Word-for-Word Answers", "SecH1"),
    p("<b>Q1: Why does Preferential Attachment have such a dominant ROC-AUC (0.9505)?</b><br/>"
      "<i>Answer:</i> Financial OTC networks are strongly scale-free (gamma ≈ 2.1). In cryptocurrency trading, participants route trades through established, reputable brokers who act as liquidity hubs. Because PA multiplies node degrees, it naturally captures this hub attraction, providing near-perfect global ranking.", "GuideBody"),
    p("<b>Q2: If PA has the highest AUC, why bother with Adamic-Adar or Common Neighbors?</b><br/>"
      "<i>Answer:</i> Preferential Attachment has zero community specificity—it just recommends the biggest hub to everyone. Adamic-Adar specifically looks at who your mutual connections are and penalizes hubs. It identifies exclusive, tight-knit community partners, achieving 100% Precision@10.", "GuideBody"),
    p("<b>Q3: Why was Spanning Tree protection mandatory in the 80/20 train-test split?</b><br/>"
      "<i>Answer:</i> In sparse scale-free networks, randomly deleting 20% of edges frequently disconnects peripheral nodes into isolated components. Isolated nodes have zero common neighbors, creating artificial false negatives. Retaining an MST in G_train ensures the graph remains fully connected.", "GuideBody"),
    p("<b>Q4: How does Heider's Structural Balance Theory strengthen the recommendations?</b><br/>"
      "<i>Answer:</i> In signed trust networks, cognitive tension occurs in unbalanced triads like (+, +, -) ('my friend trusts my enemy'). We verified that 100% of our top recommended links close (+, +, +) triads with mutual partners, ensuring newly introduced connections reinforce community stability.", "GuideBody"),
    p("<b>Q5: What are the primary deliverables of your project?</b><br/>"
      "<i>Answer:</i> 1. Source code & executed notebook (.ipynb); 2. Dataset package with SHA-256 manifest; 3. Visualizations (ROC curves, Precision@K bar charts, Cytoscape GraphML, HTML demo); 4. 8-page academic report (PDF); 5. 13-slide 3-speaker presentation deck (.pptx and .pdf); plus a local interactive web UI.", "GuideBody")
]

doc.build(story)
print(f"Team presentation study guide PDF built at: {OUT_PDF}")
