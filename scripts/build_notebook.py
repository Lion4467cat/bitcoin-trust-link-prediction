"""Create and execute the project notebook."""
from pathlib import Path
import base64
import contextlib
import io
import nbformat
import pandas as pd
from IPython.display import Image
from IPython import display as ip_display_module

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "bitcoin_alpha_structural_balance.ipynb"

cells = [
    nbformat.v4.new_markdown_cell("""# Structural Balance in the Bitcoin Alpha Trust Network

**Course project in Social Network Analysis**  
**Syllabus alignment:** positive and negative relationships, structural balance, graph theory, and network data.

This notebook asks whether positive and negative trust ties form balanced triads more often than expected when the same network topology and overall sign counts are retained but signs are randomly reassigned.

**Main finding:** 85.64% of 21,677 closed triads are balanced in the undirected signed projection. Across 1,000 sign permutations, the mean is 76.94%, and none reaches the observed value. This is evidence of sign organization relative to the stated null model, not a causal claim."""),
    nbformat.v4.new_markdown_cell("""## 1. Data and network model

The SNAP file records `source, target, rating, time`. The source user rates the target on a scale from -10 (distrust) to +10 (trust). For structural balance, this project needs an undirected signed graph. It groups records by unordered user pair and averages reciprocal ratings. A positive mean produces a positive tie, a negative mean produces a negative tie, and an exact zero is marked neutral and omitted. This projection is stated explicitly because reciprocal trust can be asymmetric."""),
    nbformat.v4.new_code_cell("""from pathlib import Path
import json
import sys
import pandas as pd
from IPython.display import Image, display

ROOT = next(p for p in (Path.cwd(), *Path.cwd().parents) if (p / "src" / "analyze.py").exists())
sys.path.insert(0, str(ROOT / "src"))
import analyze

raw, aggregated_pairs, G = analyze.load_data()
print(f"Raw ratings: {len(raw):,}")
print(f"Distinct users: {G.number_of_nodes():,}")
print(f"Unordered pairs before neutral removal: {len(aggregated_pairs):,}")
print(f"Neutral pairs removed: {(aggregated_pairs['sign'] == 0).sum():,}")
print(f"Signed graph ties: {G.number_of_edges():,}")
display(raw.head())"""),
    nbformat.v4.new_markdown_cell("""## 2. Structural balance rule

For a closed triad, multiply the three edge signs. A positive product means the triad is balanced. Thus three positive ties are balanced, and a triad with one positive tie and two negative ties is also balanced. A negative product means the triad is unbalanced. The test includes every triangle in the projected graph."""),
    nbformat.v4.new_code_cell("""triangle_triples, edge_pairs = analyze.triangle_edge_indices(G)
import numpy as np
edge_signs = np.asarray([G[u][v]["sign"] for u, v in edge_pairs], dtype=np.int8)
triangle_edges = np.asarray(triangle_triples, dtype=np.int32)
triangle_products = np.prod(edge_signs[triangle_edges], axis=1)
observed_fraction = float(np.mean(triangle_products > 0))
print(f"Closed triads: {len(triangle_edges):,}")
print(f"Balanced triads: {int(np.sum(triangle_products > 0)):,} ({observed_fraction:.2%})")
print(f"Unbalanced triads: {int(np.sum(triangle_products < 0)):,} ({np.mean(triangle_products < 0):.2%})")"""),
    nbformat.v4.new_markdown_cell("""## 3. Sign-shuffle null model

The null model holds the undirected graph fixed and randomly shuffles its observed edge signs. Each permutation therefore preserves the topology and the total numbers of positive and negative ties. It does not preserve each user's own balance of positive and negative ties. We use 1,000 permutations with a fixed random seed. The one-sided plus-one permutation p-value is `(1 + number of null scores >= observed) / (1 + number of permutations)`."""),
    nbformat.v4.new_code_cell("""# Reproduce the full pipeline and write all figures and machine-readable results.
analyze.main(verbose=False)
summary = json.loads((ROOT / "outputs" / "summary.json").read_text(encoding="utf-8"))
result_table = pd.DataFrame([
    ("Users", f\"{summary['users_in_projection']:,}\"),
    ("Signed ties", f\"{summary['signed_ties']:,}\"),
    ("Positive ties", f\"{summary['positive_ties']:,} ({summary['positive_tie_fraction']:.1%})\"),
    ("Negative ties", f\"{summary['negative_ties']:,} ({summary['negative_tie_fraction']:.1%})\"),
    ("Closed triads", f\"{summary['triangles']:,}\"),
    ("Balanced triads", f\"{summary['balanced_triangles']:,} ({summary['balanced_triangle_fraction']:.2%})\"),
    ("Null mean", f\"{summary['null_mean']:.2%}\"),
    ("Null 95% interval", f\"{summary['null_ci_low']:.2%} to {summary['null_ci_high']:.2%}\"),
    ("Permutation p-value", f\"{summary['permutation_p_upper']:.3f}\"),
], columns=["Measure", "Result"])
display(result_table)"""),
    nbformat.v4.new_code_cell("""display(Image(filename=str(ROOT / "visualizations" / "edge_sign_distribution.png")))
display(Image(filename=str(ROOT / "visualizations" / "structural_balance_triads.png")))
display(Image(filename=str(ROOT / "visualizations" / "balance_null_model.png")))
display(Image(filename=str(ROOT / "visualizations" / "signed_ego_network.png")))"""),
    nbformat.v4.new_markdown_cell("""## 4. Interpretation

The observed balanced-triad share is about 8.7 percentage points above the sign-shuffle mean. The topology and the overall positive/negative tie counts alone do not explain the observed fraction under this null. Signs are arranged in ways that produce more balanced closed triads.

The undirected graph is sparse and dominated by positive ties. These features matter: with about 90.7% positive ties, many triangles will be balanced even under random assignment. That is why the comparison uses a null model rather than interpreting 85.6% in isolation.

## 5. Limitations

- Averaging both directions creates one undirected tie and can hide disagreement between users.
- Exact zero means are excluded, so results depend on the projection rule.
- The sign-shuffle null preserves total sign counts but not node-level sign tendencies, edge weights, or time order.
- Triads are dependent because they share edges; the permutation test handles the fixed graph dependence under the chosen null but does not make triangles independent observations.
- User IDs are anonymous dataset identifiers. The analysis cannot infer real-world identities, motives, or current platform behavior.
- The data are historical, spanning 2010-2015 based on the supplied timestamps.

## 6. Reproducibility and references

Run `python src/analyze.py` from the project root, or execute this notebook. The analysis uses seed 2026 and 1,000 permutations. See `README.md` for the environment setup and `data/README.md` for the original data source.

Kumar, S., Spezzano, F., Subrahmanian, V. S., & Faloutsos, C. (2016). “Edge Weight Prediction in Weighted Signed Networks.” IEEE International Conference on Data Mining. Dataset: [Stanford SNAP Bitcoin Alpha page](https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html)."""),
]

nb = nbformat.v4.new_notebook(cells=cells)
nb.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
nb.metadata.language_info = {"name": "python"}
OUT.parent.mkdir(parents=True, exist_ok=True)

active_outputs = []

def display(value):
    if isinstance(value, pd.DataFrame):
        active_outputs.append(nbformat.v4.new_output("display_data", data={"text/html": value.to_html(index=False), "text/plain": value.to_string(index=False)}, metadata={}))
        return
    if isinstance(value, Image):
        path = Path(value.filename)
        active_outputs.append(nbformat.v4.new_output("display_data", data={"image/png": base64.b64encode(path.read_bytes()).decode("ascii")}, metadata={}))
        return
    active_outputs.append(nbformat.v4.new_output("display_data", data={"text/plain": repr(value)}, metadata={}))

ip_display_module.display = display

namespace = {"display": display}
execution_count = 0
for cell in nb.cells:
    if cell.cell_type != "code":
        continue
    execution_count += 1
    stdout = io.StringIO()
    cell.outputs = []
    cell.execution_count = execution_count
    active_outputs.clear()
    with contextlib.redirect_stdout(stdout):
        exec(compile(cell.source, f"notebook-cell-{execution_count}", "exec"), namespace)
    cell.outputs.extend(active_outputs)
    if stdout.getvalue():
        cell.outputs.append(nbformat.v4.new_output("stream", name="stdout", text=stdout.getvalue()))
nbformat.write(nb, OUT)
print(OUT)
