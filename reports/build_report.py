"""Build the final student project report as a polished PDF."""
from pathlib import Path
import json
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table,
                                TableStyle, PageBreak, KeepTogether)
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "structural_balance_report.pdf"
SUMMARY = json.loads((ROOT / "outputs" / "summary.json").read_text())
NAVY = colors.HexColor("#18343D")
TEAL = colors.HexColor("#17806D")
RUST = colors.HexColor("#C8504B")
PALE = colors.HexColor("#EDF3F3")
INK = colors.HexColor("#27383D")
MUTED = colors.HexColor("#5B6B70")
regular_font = Path("/usr/share/fonts/liberation/LiberationSans-Regular.ttf")
bold_font = Path("/usr/share/fonts/liberation/LiberationSans-Bold.ttf")
if regular_font.exists() and bold_font.exists():
    pdfmetrics.registerFont(TTFont("ProjectSans", str(regular_font)))
    pdfmetrics.registerFont(TTFont("ProjectSans-Bold", str(bold_font)))
    pdfmetrics.registerFontFamily("ProjectSans", normal="ProjectSans", bold="ProjectSans-Bold",
                                  italic="ProjectSans", boldItalic="ProjectSans-Bold")
    FONT_REGULAR, FONT_BOLD = "ProjectSans", "ProjectSans-Bold"
else:
    FONT_REGULAR, FONT_BOLD = "Helvetica", "Helvetica-Bold"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName=FONT_BOLD,
    fontSize=27, leading=33, textColor=NAVY, alignment=TA_LEFT, spaceAfter=10))
styles.add(ParagraphStyle(name="CoverSub", parent=styles["Normal"], fontName=FONT_REGULAR, fontSize=13, leading=19,
    textColor=MUTED, spaceAfter=10))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName=FONT_BOLD,
    fontSize=18, leading=23, textColor=NAVY, spaceBefore=3, spaceAfter=9, keepWithNext=True))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName=FONT_BOLD,
    fontSize=12, leading=16, textColor=TEAL, spaceBefore=8, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName=FONT_REGULAR, fontSize=9.3, leading=14,
    textColor=INK, spaceAfter=7, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontName=FONT_REGULAR, fontSize=8, leading=11,
    textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="TableHead", parent=styles["BodyText"], fontName=FONT_BOLD,
    fontSize=8, leading=10, textColor=colors.white))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontName=FONT_BOLD,
    fontSize=11, leading=16, textColor=NAVY, backColor=PALE, borderColor=TEAL,
    borderWidth=1, borderPadding=9, spaceBefore=10, spaceAfter=10))
styles.add(ParagraphStyle(name="CenterSmall", parent=styles["Smallx"], alignment=TA_CENTER))

def p(text, style="Bodyx"):
    return Paragraph(text, styles[style])

def img(name, width=166*mm):
    path = ROOT / "visualizations" / name
    with PILImage.open(path) as source:
        image_width, image_height = source.size
    return Image(str(path), width=width, height=width * image_height / image_width, kind="direct")

def table(data, widths, header=True, font=8.5):
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), .45, colors.HexColor("#D5DEDF")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("FONTNAME", (0, 0), (-1, -1), FONT_REGULAR),
        ("FONTSIZE", (0, 0), (-1, -1), font),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
    ]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), NAVY),
                     ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                     ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD)]
        for row in range(1, len(data)):
            if row % 2 == 0:
                commands.append(("BACKGROUND", (0, row), (-1, row), PALE))
    t.setStyle(TableStyle(commands))
    return t

def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page > 1:
        canvas.setStrokeColor(colors.HexColor("#D5DEDF"))
        canvas.setLineWidth(.5)
        canvas.line(22*mm, h-16*mm, w-22*mm, h-16*mm)
        canvas.setFont(FONT_REGULAR, 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(22*mm, h-12*mm, "STRUCTURAL BALANCE IN THE BITCOIN ALPHA TRUST NETWORK")
    canvas.setStrokeColor(colors.HexColor("#D5DEDF"))
    canvas.line(22*mm, 14*mm, w-22*mm, 14*mm)
    canvas.setFont(FONT_REGULAR, 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(22*mm, 9*mm, "Social Network Analysis project")
    canvas.drawRightString(w-22*mm, 9*mm, f"{doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=22*mm, leftMargin=22*mm,
                        topMargin=23*mm, bottomMargin=21*mm, title="Structural Balance in the Bitcoin Alpha Trust Network",
                        author="Student Project")
story = []

# Cover
story += [Spacer(1, 25*mm), p("SOCIAL NETWORK ANALYSIS  |  COURSE SUBMISSION", "Smallx"), Spacer(1, 9*mm),
          p("Structural Balance in the Bitcoin Alpha Trust Network", "CoverTitle"),
          p("An empirical analysis of positive and negative trust relationships", "CoverSub"),
          Spacer(1, 7*mm),
          p(f"{SUMMARY['balanced_triangle_fraction']:.1%} of closed triads are balanced in the undirected signed projection. The observed share exceeds the 95% range from a sign-shuffle null model.", "Callout"),
          Spacer(1, 16*mm),
          table([[p("Submitted by", "Smallx"), p("USN", "Smallx"), p("Submitted to", "Smallx")],
                 [p("______________________", "Bodyx"), p("______________", "Bodyx"), p("Course Instructor", "Bodyx")]],
                [61*mm, 48*mm, 47*mm], header=False),
          Spacer(1, 25*mm),
          p("Dataset: Stanford SNAP Bitcoin Alpha web-of-trust ratings", "Bodyx"),
          p("Analysis: NetworkX, pandas, NumPy, and a fixed-topology sign permutation test", "Bodyx"),
          p("Course: Social Network Analysis", "Bodyx"),
          PageBreak()]

# Summary and question
story += [p("Abstract", "H1x"),
          p(f"This study examines structural balance in the Bitcoin Alpha online trust network. Users rate other users from -10 (distrust) to +10 (trust). To apply the classical triad balance rule to these directed ratings, the analysis averages available ratings for each unordered user pair and removes exact-zero means as neutral. The projected graph contains {SUMMARY['users_in_projection']:,} users, {SUMMARY['signed_ties']:,} signed ties, and {SUMMARY['triangles']:,} closed triads.", "Bodyx"),
          p(f"Of those triangles, {SUMMARY['balanced_triangles']:,} ({SUMMARY['balanced_triangle_fraction']:.2%}) have a positive product of edge signs and are therefore balanced. Across {SUMMARY['permutations']:,} permutations that shuffle signs across the fixed graph while preserving the global sign counts, the mean balanced fraction is {SUMMARY['null_mean']:.2%} and the central 95% interval is {SUMMARY['null_ci_low']:.2%}-{SUMMARY['null_ci_high']:.2%}. No permutation reached the observed fraction. With the plus-one correction, the one-sided permutation p-value is {SUMMARY['permutation_p_upper']:.3f}.", "Bodyx"),
          p("Research question", "H2x"),
          p("Do positive and negative trust ties form balanced closed triads more often than expected when the observed topology and overall counts of positive and negative ties are held fixed?", "Callout"),
          p("Study objectives", "H2x"),
          p("1. Prepare a clear node and edge model for the signed trust data.<br/>2. Describe the projected graph and the distribution of positive and negative ties.<br/>3. Measure triadic structural balance using the sign-product rule.<br/>4. Compare the observed balance with a reproducible sign-shuffle null model.", "Bodyx"),
          p("Course alignment", "H2x"),
          p("The analysis directly applies Unit 2's positive and negative relationships and structural balance, supported by Unit 1's network data and graph theory. It treats ratings as social ties rather than as recommendations or friendship links.", "Bodyx"),
          PageBreak()]

# Model and data
story += [p("Data and network model", "H1x"),
          p(f"The raw SNAP file contains {SUMMARY['raw_ratings']:,} directed rating records and {SUMMARY['directed_users']:,} user IDs. Each record identifies a rater, a ratee, an integer rating from -10 to +10, and a Unix timestamp. The rating period runs from 2010 to 2015 based on the timestamps in the file. SNAP describes this dataset as a trust-weighted signed directed network.", "Bodyx"),
          table([[p("Element", "TableHead"), p("Model", "TableHead"), p("Interpretation", "TableHead")],
                 [p("Node", "Bodyx"), p("Bitcoin Alpha user ID", "Bodyx"), p("A user who rates another user", "Bodyx")],
                 [p("Raw directed edge", "Bodyx"), p("Rater to ratee", "Bodyx"), p("Rating from -10 to +10", "Bodyx")],
                 [p("Projected signed tie", "Bodyx"), p("Unordered user pair", "Bodyx"), p("Sign of the mean available rating(s)", "Bodyx")]],
                [39*mm, 55*mm, 62*mm]),
          Spacer(1, 7*mm), p("Preparation and projection", "H2x"),
          p(f"The source file was checked for missing fields, rating range, repeated directed pairs, self-ties, and user count. No missing fields, repeated directed pairs, or self-ties were found, and the observed ratings fall within SNAP's documented range. For structural balance, ratings are grouped by unordered pair and averaged. This yields {SUMMARY['undirected_pairs_before_neutral_removal']:,} unordered pairs; {SUMMARY['neutral_pairs_removed']:,} have a mean of exactly zero and are excluded as neutral. The remaining {SUMMARY['signed_ties']:,} ties comprise {SUMMARY['positive_ties']:,} positive ties and {SUMMARY['negative_ties']:,} negative ties. Users remain in the graph even if neutral ties leave them isolated.", "Bodyx"),
          p("The projection is a deliberate modeling choice. Averaging reciprocal ratings makes the network undirected, as required by the triad balance test, but it hides directional disagreement. The project reports this limitation instead of treating the projected ties as original reciprocal relationships.", "Bodyx"),
          p("Graph summary", "H2x"),
          table([[p("Measure", "TableHead"), p("Value", "TableHead"), p("Measure", "TableHead"), p("Value", "TableHead")],
                 [p("Users", "Bodyx"), p(f"{SUMMARY['users_in_projection']:,}", "Bodyx"), p("Signed ties", "Bodyx"), p(f"{SUMMARY['signed_ties']:,}", "Bodyx")],
                 [p("Density", "Bodyx"), p(f"{SUMMARY['density']:.4f}", "Bodyx"), p("Mean degree", "Bodyx"), p(f"{SUMMARY['mean_degree']:.2f}", "Bodyx")],
                 [p("Components", "Bodyx"), p(f"{SUMMARY['connected_components']}", "Bodyx"), p("Largest component", "Bodyx"), p(f"{SUMMARY['largest_component_nodes']:,} users ({SUMMARY['largest_component_fraction']:.2%})", "Bodyx")]],
                [34*mm, 36*mm, 38*mm, 48*mm]), PageBreak()]

# Methods
story += [p("Structural balance method", "H1x"),
          p("A closed triad is a set of three users with all three pairwise ties present. Assign each tie sign +1 or -1. The triad is balanced when the product of its three signs is positive. A triad with three positive ties is balanced; a triad with one positive and two negative ties is also balanced. A triad with an odd number of negative ties has a negative sign product and is unbalanced.", "Bodyx"),
          img("structural_balance_triads.png", 160*mm), Spacer(1, 3*mm),
          p("Figure 1. Actual balanced and unbalanced triads sampled from the projected Bitcoin Alpha graph. Green solid edges are positive; red dashed edges are negative.", "CenterSmall"),
          p("Null model", "H2x"),
          p(f"To compare the observed balance with a null model, the project holds the undirected graph fixed and randomly permutes its edge signs. Each of {SUMMARY['permutations']:,} permutations preserves the network topology and the exact global counts of positive and negative ties. For each shuffled graph, the balanced fraction is recalculated over the same {SUMMARY['triangles']:,} triangles. The random seed is {SUMMARY['random_seed']}. The upper-tail permutation p-value uses the plus-one correction: (1 + count of null scores at least as large as observed) / (1 + number of permutations).", "Bodyx"),
          p("This null isolates global sign arrangement given fixed topology and global sign counts. It does not preserve node-specific positive/negative tendencies, signed edge weights, or time order. The p-value should be interpreted relative to those assumptions.", "Bodyx"),
          p("The calculations use NetworkX for graph construction, connected components, degree, clustering and triangles; pandas and NumPy for data preparation and permutation calculations; and Matplotlib for visualizations. The script `src/analyze.py` fixes the random seed and writes machine-readable summaries and all figures.", "Bodyx"),
          PageBreak()]

# Results
story += [p("Results", "H1x"), img("edge_sign_distribution.png", 150*mm),
          p("Figure 2. Sign distribution after bilateral aggregation and removal of exact-zero pairs.", "CenterSmall"),
          p(f"Positive ties account for {SUMMARY['positive_tie_fraction']:.2%} of the non-neutral projected edges. The projected network contains {SUMMARY['connected_components']} connected components, with {SUMMARY['isolates']} isolates; the largest component includes {SUMMARY['largest_component_nodes']:,} of {SUMMARY['users_in_projection']:,} users. The mean degree is {SUMMARY['mean_degree']:.2f} and the density is {SUMMARY['density']:.5f}, so the graph is sparse.", "Bodyx"),
          table([[p("Triad outcome", "TableHead"), p("Count", "TableHead"), p("Share", "TableHead")],
                 [p("Balanced", "Bodyx"), p(f"{SUMMARY['balanced_triangles']:,}", "Bodyx"), p(f"{SUMMARY['balanced_triangle_fraction']:.2%}", "Bodyx")],
                 [p("Unbalanced", "Bodyx"), p(f"{SUMMARY['unbalanced_triangles']:,}", "Bodyx"), p(f"{SUMMARY['unbalanced_triangles']/SUMMARY['triangles']:.2%}", "Bodyx")],
                 [p("Total closed triads", "Bodyx"), p(f"{SUMMARY['triangles']:,}", "Bodyx"), p("100.00%", "Bodyx")]],
                [66*mm, 45*mm, 55*mm]),
          Spacer(1, 6*mm), p("Sign-shuffle comparison", "H2x"),
          img("balance_null_model.png", 160*mm),
          p(f"Figure 3. Distribution of balanced-triad fractions from {SUMMARY['permutations']:,} fixed-topology sign permutations. Observed balance is {SUMMARY['balanced_triangle_fraction']:.2%}; the permutation mean is {SUMMARY['null_mean']:.2%}; and the 95% interval is {SUMMARY['null_ci_low']:.2%}-{SUMMARY['null_ci_high']:.2%}.", "CenterSmall"),
          Spacer(1, 7*mm),
          p(f"Interpretation: the observed share is {(SUMMARY['balanced_triangle_fraction']-SUMMARY['null_mean'])*100:.2f} percentage points above the null mean. No shuffled graph reached the observed value. With {SUMMARY['permutations']:,} permutations, the plus-one p-value is {SUMMARY['permutation_p_upper']:.3f}, the smallest value this run can report. This conclusion applies to the specified sign-shuffle null.", "Callout"),
          PageBreak()]

# Interpretation, limitations, references
story += [p("Interpretation and limitations", "H1x"),
          p(f"The observed balanced-triad fraction is {(SUMMARY['balanced_triangle_fraction']-SUMMARY['null_mean'])*100:.2f} percentage points above the sign-shuffle mean. None of {SUMMARY['permutations']:,} shuffled networks reaches the observed fraction, giving a plus-one p-value of {SUMMARY['permutation_p_upper']:.3f}. Under the selected null model, the global positive-tie majority and the graph's topology do not fully explain the observed triadic sign pattern. The finding is consistent with local structural balance in the observed trust network.", "Bodyx"),
          p(f"This result does not imply that {SUMMARY['balanced_triangle_fraction']:.1%} of all user relationships are harmonious. It describes closed triads only. Open triples are not included, and the balance of each triad does not establish a global partition of all users into two internally positive groups.", "Bodyx"),
          p("Local signed network", "H2x"), img("signed_ego_network.png", 143*mm),
          p("Figure 4. One user's immediate neighborhood. Green solid lines indicate positive ties; red dashed lines indicate negative ties. User IDs are anonymous dataset identifiers.", "CenterSmall"),
          PageBreak(),
          p("Limitations", "H2x"),
          p(f"The undirected projection averages available ratings and can erase asymmetric trust. Removing exact-zero means is another modeling decision. The null model retains global sign counts but not node-level rating tendencies, weights, or chronology. Triads overlap and share edges, so they are not independent observations; the permutation procedure keeps the network fixed while randomizing signs, but conclusions still depend on this null. The historical dataset describes platform ratings from 2010-2015 and should not be generalized to current users or other communities.", "Bodyx"),
          p("Conclusion", "H2x"),
          p(f"The Bitcoin Alpha signed trust network provides a direct case study for the syllabus topic of structural balance. The projected network has {SUMMARY['triangles']:,} closed triads, of which {SUMMARY['balanced_triangle_fraction']:.2%} are balanced. This exceeds the sign-shuffle reference range ({SUMMARY['null_ci_low']:.2%}-{SUMMARY['null_ci_high']:.2%}) under a null that preserves topology and global sign totals. The evidence supports a non-random triadic sign arrangement under the chosen assumptions, while the directed-to-undirected projection and null-model scope limit interpretation.", "Bodyx"),
          p("References", "H2x"),
          p("Kumar, S., Spezzano, F., Subrahmanian, V. S., & Faloutsos, C. (2016). “Edge Weight Prediction in Weighted Signed Networks.” IEEE International Conference on Data Mining, pp. 221-230. <link href='https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html' color='#17806D'>Dataset page and required citation</link>.", "Smallx"),
          p("Stanford Network Analysis Project (SNAP). Bitcoin Alpha trust weighted signed network, dataset description and data format. <link href='https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html' color='#17806D'>https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html</link>.", "Smallx")]

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(OUT)
