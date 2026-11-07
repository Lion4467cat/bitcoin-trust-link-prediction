import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";
import { pathToFileURL } from "node:url";

const ROOT = process.env.SNA_AAT_PROJECT_ROOT ?? path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const SKILL_DIR = "/home/tinkerer/.codex/plugins/cache/openai-primary-runtime/presentations/26.1030.10813/skills/presentations";
const RUNTIME_PYTHON = "/home/tinkerer/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const FINAL_OUT = path.join(ROOT, "slides", "structural_balance_presentation.pptx");
const STAGING = path.join(ROOT, ".build", "presentation");
const VALIDATION = path.join(ROOT, ".build", "presentation-validation");
const FONT = "Arial";
const C = { ink: "#18343D", text: "#31484F", muted: "#667A80", teal: "#17806D", rust: "#C8504B", gold: "#D7A84A", pale: "#EDF3F3", white: "#FFFFFF", bg: "#FBFCFC", grid: "#D9E2E3" };
const SUMMARY = JSON.parse(await fs.readFile(path.join(ROOT, "outputs", "summary.json"), "utf8"));
const fmt = value => Number(value).toLocaleString("en-US");
const pct = (value, digits = 2) => `${(100 * value).toFixed(digits)}%`;

await fs.mkdir(STAGING, { recursive: true });
await fs.mkdir(VALIDATION, { recursive: true });
await fs.mkdir(path.dirname(FINAL_OUT), { recursive: true });
const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const imageCache = new Map();
for (const asset of ["signed_ego_network.png", "structural_balance_triads.png"]) {
  imageCache.set(asset, new Uint8Array(await fs.readFile(path.join(ROOT, "visualizations", asset))));
}

function text(slide, value, x, y, w, h, opts = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name: opts.name,
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  shape.text = value;
  shape.text.style = {
    typeface: FONT,
    fontSize: opts.size ?? 24,
    color: opts.color ?? C.text,
    bold: opts.bold ?? false,
    alignment: opts.align ?? "left",
    verticalAlignment: opts.valign ?? "top",
    wrap: "square",
    autoFit: "shrinkText",
    insets: 0,
  };
  return shape;
}

function rect(slide, x, y, w, h, color, name) {
  return slide.shapes.add({ geometry: "rect", name, position: { left: x, top: y, width: w, height: h }, fill: color, line: { style: "solid", fill: "none", width: 0 } });
}

function image(slide, name, x, y, w, h, alt) {
  return slide.images.add({ blob: imageCache.get(name), contentType: "image/png", alt, fit: "contain", position: { left: x, top: y, width: w, height: h } });
}

function base(title, index, kicker = "BITCOIN ALPHA TRUST NETWORK") {
  const slide = presentation.slides.add();
  slide.background.fill = C.bg;
  rect(slide, 0, 0, 1280, 8, C.teal, `top-rule-${index}`);
  text(slide, kicker, 70, 33, 650, 24, { size: 14, color: C.muted, bold: true });
  if (title) text(slide, title, 70, 76, 1135, 60, { size: 42, color: C.ink, bold: true, name: `slide-title-${index}` });
  rect(slide, 70, 668, 1140, 1, C.grid, `footer-rule-${index}`);
  text(slide, "SNA COURSE PROJECT  |  STRUCTURAL BALANCE", 70, 680, 700, 20, { size: 13, color: C.muted });
  text(slide, String(index).padStart(2, "0"), 1155, 680, 55, 20, { size: 13, color: C.muted, align: "right" });
  return slide;
}

function notes(slide, body) {
  slide.speakerNotes.text = body;
}

// 1. Title and main result
{
  const slide = base("", 1, "SOCIAL NETWORK ANALYSIS  |  COURSE PROJECT");
  text(slide, "Structural Balance\nin the Bitcoin Alpha\nTrust Network", 70, 115, 700, 230, { size: 59, color: C.ink, bold: true, name: "project-title" });
  text(slide, "Positive and negative trust relationships in a signed social network", 74, 365, 640, 54, { size: 23, color: C.muted });
  rect(slide, 820, 115, 5, 360, C.teal, "result-accent");
  text(slide, pct(SUMMARY.balanced_triangle_fraction), 865, 140, 340, 100, { size: 76, color: C.teal, bold: true, name: "headline-result" });
  text(slide, "of observed closed triads\nare structurally balanced", 867, 250, 325, 74, { size: 25, color: C.ink, bold: true });
  text(slide, `Compared with ${pct(SUMMARY.null_mean)} under a fixed-topology sign shuffle`, 867, 350, 320, 72, { size: 19, color: C.text });
  text(slide, "Submitted by: ____________________     USN: ______________", 74, 560, 800, 26, { size: 16, color: C.muted });
  text(slide, "Submitted to: Course Instructor  |  Social Network Analysis", 74, 594, 800, 24, { size: 16, color: C.muted });
  notes(slide, "Introduce the study question: do trust and distrust ties form balanced triads more often than the same graph would under random reassignment of its signs? State that the headline is based on an undirected projection of the directed ratings. Source: Stanford SNAP Bitcoin Alpha dataset, https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html");
}

// 2. Dataset and node/edge mapping
{
  const slide = base("Users rate trust from -10 to +10", 2);
  text(slide, fmt(SUMMARY.users_in_projection), 70, 165, 245, 76, { size: 54, color: C.ink, bold: true });
  text(slide, "user nodes", 74, 241, 230, 30, { size: 20, color: C.muted });
  text(slide, fmt(SUMMARY.raw_ratings), 345, 165, 270, 76, { size: 54, color: C.ink, bold: true });
  text(slide, "directed ratings", 350, 241, 260, 30, { size: 20, color: C.muted });
  text(slide, "Each rating is a signed relationship from the rater to the ratee. Positive values express trust; negative values express distrust.", 70, 310, 510, 122, { size: 22, color: C.text });
  image(slide, "signed_ego_network.png", 635, 155, 575, 420, "Bitcoin Alpha ego network with positive and negative ties");
  text(slide, "One local neighborhood. Green lines are positive, red dashed lines are negative.", 635, 582, 575, 32, { size: 15, color: C.muted, align: "center" });
  notes(slide, "The original SNAP records are directed ratings with source, target, rating, and timestamp. The local image is an ego network around user ID 759, selected for a readable neighborhood display; the identifier is anonymous and has no inferred real-world identity. Dataset source and citation: Kumar et al. (2016), https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html");
}

// 3. Projection method
{
  const slide = base("Structural balance needs an undirected signed graph", 3);
  text(slide, "To evaluate balance, reciprocal ratings are averaged for each unordered user pair.", 70, 155, 1100, 44, { size: 24, color: C.text });
  text(slide, "01", 84, 245, 85, 58, { size: 22, color: C.teal, bold: true });
  text(slide, fmt(SUMMARY.raw_ratings), 84, 292, 320, 70, { size: 51, color: C.ink, bold: true });
  text(slide, "directed ratings", 88, 370, 300, 35, { size: 20, color: C.muted });
  rect(slide, 425, 265, 1, 160, C.grid);
  text(slide, "02", 475, 245, 85, 58, { size: 22, color: C.teal, bold: true });
  text(slide, fmt(SUMMARY.undirected_pairs_before_neutral_removal), 475, 292, 320, 70, { size: 51, color: C.ink, bold: true });
  text(slide, "unordered pairs", 480, 370, 300, 35, { size: 20, color: C.muted });
  rect(slide, 825, 265, 1, 160, C.grid);
  text(slide, "03", 875, 245, 85, 58, { size: 22, color: C.teal, bold: true });
  text(slide, fmt(SUMMARY.signed_ties), 875, 292, 320, 70, { size: 51, color: C.ink, bold: true });
  text(slide, "non-neutral signed ties", 880, 370, 320, 35, { size: 20, color: C.muted });
  text(slide, `${fmt(SUMMARY.neutral_pairs_removed)} zero-mean pairs are excluded as neutral. The projection can hide disagreement between reciprocal ratings.`, 85, 485, 1080, 78, { size: 21, color: C.text });
  text(slide, `${fmt(SUMMARY.positive_ties)} positive ties     ${fmt(SUMMARY.negative_ties)} negative ties`, 85, 578, 1050, 35, { size: 20, color: C.rust, bold: true });
  notes(slide, `Explain the projection choice. Classical structural balance is evaluated on undirected signed ties, so ratings between user pairs are averaged. A positive mean gives sign +1; a negative mean gives sign -1; exact zero is neutral and excluded from the signed graph. The graph keeps all ${fmt(SUMMARY.users_in_projection)} source users, including those who become isolated. This is a modeling assumption and one of the study limitations.`);
}

// 4. Structural balance rule
{
  const slide = base("A triad is balanced when its sign product is positive", 4);
  text(slide, "For each closed triad, multiply the three edge signs.", 70, 153, 1070, 40, { size: 24, color: C.text });
  image(slide, "structural_balance_triads.png", 95, 230, 1090, 330, "Observed examples of balanced and unbalanced signed triads");
  rect(slide, 175, 590, 28, 6, C.teal);
  text(slide, "Product +1: balanced", 215, 577, 360, 32, { size: 20, color: C.ink, bold: true });
  rect(slide, 675, 590, 28, 6, C.rust);
  text(slide, "Product -1: unbalanced", 715, 577, 410, 32, { size: 20, color: C.ink, bold: true });
  notes(slide, "The left example is all positive. The right example has two positive ties and one negative tie. Both have a positive product and are balanced. An odd number of negative edges gives a negative product and an unbalanced triad. The pictured triads are examples from the observed network. Structural balance is the positive/negative relationship topic in Unit 2 of the course syllabus.");
}

// 5. Network profile with native editable chart
{
  const slide = base("Positive trust dominates the projected ties", 5);
  const chart = slide.charts.add("bar", {
    position: { left: 75, top: 160, width: 690, height: 405 },
    categories: ["Positive trust", "Negative trust"],
    series: [{ name: "Undirected ties", values: [SUMMARY.positive_ties, SUMMARY.negative_ties], fill: C.teal,
      points: [{ idx: 0, fill: C.teal }, { idx: 1, fill: C.rust }] }],
    hasLegend: false,
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 95 },
    dataLabels: { showValue: true, position: "outEnd", textStyle: { fontSize: 16, bold: true, fill: C.ink } },
    xAxis: { textStyle: { fontSize: 15, fill: C.ink }, line: { style: "solid", fill: C.grid, width: 1 }, majorGridlines: null },
    yAxis: { title: { text: "Undirected ties", textStyle: { fontSize: 14, fill: C.muted } }, textStyle: { fontSize: 13, fill: C.muted }, majorGridlines: { style: "solid", fill: C.grid, width: 1 } },
    chartFill: C.bg, chartLine: { style: "solid", fill: "none", width: 0 }, plotAreaFill: C.bg, plotAreaLine: { style: "solid", fill: "none", width: 0 },
  });
  const { applyPresentationChartFont } = await import(pathToFileURL(path.join(SKILL_DIR, "container_tools/artifact_tool_utils.mjs")).href);
  applyPresentationChartFont(chart, { fontFamily: FONT });
  text(slide, pct(SUMMARY.positive_tie_fraction), 835, 205, 350, 70, { size: 52, color: C.teal, bold: true });
  text(slide, "of non-neutral ties\nare positive", 840, 282, 330, 76, { size: 25, color: C.ink, bold: true });
  text(slide, fmt(SUMMARY.signed_ties), 840, 395, 300, 58, { size: 44, color: C.ink, bold: true });
  text(slide, "signed ties in the projection", 844, 454, 330, 42, { size: 18, color: C.muted });
  text(slide, `The graph is sparse: density ${SUMMARY.density.toFixed(5)}. Its largest component contains ${pct(SUMMARY.largest_component_fraction)} of users.`, 840, 520, 335, 82, { size: 18, color: C.text });
  notes(slide, `The chart is an editable PowerPoint chart. It shows ${fmt(SUMMARY.positive_ties)} positive ties and ${fmt(SUMMARY.negative_ties)} negative ties, a ${pct(SUMMARY.positive_tie_fraction)} positive share. Density is ${SUMMARY.density.toFixed(6)}. There are ${SUMMARY.connected_components} connected components; the largest has ${fmt(SUMMARY.largest_component_nodes)} of ${fmt(SUMMARY.users_in_projection)} users (${pct(SUMMARY.largest_component_fraction)}). Source: analysis of the SNAP dataset, https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html`);
}

// 6. Null model results with editable histogram bars
{
  const slide = base("Observed balance exceeds the sign-shuffle range", 6);
  const raw = (await fs.readFile(path.join(ROOT, "outputs", "null_model_scores.csv"), "utf8")).trim().split(/\r?\n/).slice(1).map(Number);
  const min = Math.floor(Math.min(...raw) * 100) / 100;
  const max = Math.ceil(Math.max(...raw) * 100) / 100;
  const binCount = 12, width = (max - min) / binCount;
  const counts = Array(binCount).fill(0);
  for (const value of raw) counts[Math.max(0, Math.min(binCount - 1, Math.floor((value - min) / width)))] += 1;
  const categories = counts.map((_, i) => `${(min + i * width).toFixed(3)}`);
  const chart = slide.charts.add("bar", {
    position: { left: 70, top: 166, width: 760, height: 425 },
    categories,
    series: [{ name: "Permutations", values: counts, fill: "#91AFB5" }],
    hasLegend: false,
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 45 },
    xAxis: { title: { text: "Balanced-triad fraction", textStyle: { fontSize: 14, fill: C.muted } }, textStyle: { fontSize: 11, fill: C.muted }, line: { style: "solid", fill: C.grid, width: 1 }, majorGridlines: null },
    yAxis: { title: { text: "Permutations", textStyle: { fontSize: 14, fill: C.muted } }, textStyle: { fontSize: 12, fill: C.muted }, majorGridlines: { style: "solid", fill: C.grid, width: 1 } },
    chartFill: C.bg, chartLine: { style: "solid", fill: "none", width: 0 }, plotAreaFill: C.bg, plotAreaLine: { style: "solid", fill: "none", width: 0 },
  });
  const { applyPresentationChartFont } = await import(pathToFileURL(path.join(SKILL_DIR, "container_tools/artifact_tool_utils.mjs")).href);
  applyPresentationChartFont(chart, { fontFamily: FONT });
  rect(slide, 876, 197, 4, 330, C.rust, "observed-marker");
  text(slide, "OBSERVED", 910, 190, 230, 26, { size: 14, color: C.rust, bold: true });
  text(slide, pct(SUMMARY.balanced_triangle_fraction), 905, 225, 285, 58, { size: 46, color: C.rust, bold: true });
  text(slide, "Null mean", 910, 322, 210, 28, { size: 18, color: C.muted });
  text(slide, pct(SUMMARY.null_mean), 910, 351, 220, 44, { size: 33, color: C.ink, bold: true });
  text(slide, "95% null interval", 910, 418, 250, 28, { size: 18, color: C.muted });
  text(slide, `${pct(SUMMARY.null_ci_low)}-${pct(SUMMARY.null_ci_high)}`, 910, 448, 280, 40, { size: 24, color: C.ink, bold: true });
  text(slide, `${fmt(SUMMARY.permutations)} sign permutations\nPlus-one p = ${SUMMARY.permutation_p_upper.toFixed(3)}`, 910, 516, 260, 55, { size: 18, color: C.text });
  notes(slide, `The editable column chart shows the distribution of ${fmt(SUMMARY.permutations)} null fractions. Each permutation shuffles the observed edge signs over the same fixed graph, preserving the total counts of positive and negative ties. The observed fraction is ${pct(SUMMARY.balanced_triangle_fraction, 4)}, compared with a null mean of ${pct(SUMMARY.null_mean, 4)} and a 95% central interval of ${pct(SUMMARY.null_ci_low, 4)}-${pct(SUMMARY.null_ci_high, 4)}. No permutation reached the observation. The plus-one upper-tail permutation p-value is ${SUMMARY.permutation_p_upper.toFixed(3)}, the smallest reportable value at ${fmt(SUMMARY.permutations)} permutations. This null does not preserve per-node sign tendencies, edge weights, or time order.`);
}

// 7. Interpretation and limitations
{
  const slide = base("The result describes local triads, not every relationship", 7);
  text(slide, fmt(SUMMARY.balanced_triangles), 70, 165, 330, 64, { size: 50, color: C.teal, bold: true });
  text(slide, "balanced triads", 74, 231, 300, 34, { size: 21, color: C.muted });
  text(slide, fmt(SUMMARY.unbalanced_triangles), 440, 165, 285, 64, { size: 50, color: C.rust, bold: true });
  text(slide, "unbalanced triads", 445, 231, 320, 34, { size: 21, color: C.muted });
  text(slide, `The observed balance rate is ${((SUMMARY.balanced_triangle_fraction - SUMMARY.null_mean) * 100).toFixed(2)} percentage points above the null mean. Under this null, signs are arranged into more balanced closed triads than random reassignment would produce.`, 70, 315, 1090, 92, { size: 23, color: C.ink });
  rect(slide, 70, 445, 4, 140, C.gold);
  text(slide, "Interpret with care", 95, 442, 420, 34, { size: 21, color: C.ink, bold: true });
  text(slide, "Averaging reciprocal ratings can hide disagreement. The null keeps overall sign counts, but not each user's sign pattern. The data are historical and do not describe current platform behavior.", 95, 488, 1080, 86, { size: 19, color: C.text });
  notes(slide, `Clarify that ${pct(SUMMARY.balanced_triangle_fraction)} applies only to closed triads in this projected network. It does not mean that most users are harmonious or that the graph has a global two-faction structure. There are ${fmt(SUMMARY.unbalanced_triangles)} unbalanced observed triangles. Results depend on the directed-to-undirected averaging rule and on the null model. The data timestamps span 2010-2015.`);
}

// 8. Conclusion and study scope
{
  const slide = base("Conclusion and study scope", 8);
  text(slide, "Conclusion", 70, 158, 270, 34, { size: 22, color: C.teal, bold: true });
  text(slide, `Bitcoin Alpha has ${pct(SUMMARY.balanced_triangle_fraction)} balanced closed triads, above the ${pct(SUMMARY.null_mean)} mean under the fixed-topology sign shuffle.`, 70, 200, 1080, 84, { size: 31, color: C.ink, bold: true });
  text(slide, "Interpretation boundary", 70, 340, 450, 34, { size: 22, color: C.teal, bold: true });
  text(slide, `The ${pct(SUMMARY.balanced_triangle_fraction)} result describes closed triads in an undirected projection. The null preserves graph topology and total sign counts, but not each user's sign tendencies. The analysis does not establish causality or a global two-faction structure.`, 70, 386, 1080, 112, { size: 21, color: C.text });
  text(slide, "Data and citation", 70, 560, 260, 30, { size: 18, color: C.muted, bold: true });
  text(slide, "Kumar et al. (2016), Edge Weight Prediction in Weighted Signed Networks.\nSNAP dataset: snap.stanford.edu/data/soc-sign-bitcoinalpha.html", 70, 597, 1100, 48, { size: 16, color: C.muted });
  notes(slide, `The study finds ${pct(SUMMARY.balanced_triangle_fraction)} of observed closed triads are balanced versus a null mean of ${pct(SUMMARY.null_mean)}; none of ${fmt(SUMMARY.permutations)} sign shuffles reached the observed rate. The p-value tests an upper-tail null probability for the stated permutation setup; it is not a probability that structural balance theory is true. The analysis is limited by the directed-to-undirected averaging rule and by a null that preserves only global sign totals. Cite the SNAP data page and Kumar et al. (2016): https://snap.stanford.edu/data/soc-sign-bitcoinalpha.html`);
}

async function writeBlob(filePath, blob) {
  await fs.writeFile(filePath, new Uint8Array(await blob.arrayBuffer()));
}

for (const [i, slide] of presentation.slides.items.entries()) {
  await writeBlob(path.join(STAGING, `preview-${String(i + 1).padStart(2, "0")}.png`), await presentation.export({ slide, format: "png", scale: 1 }));
}
const candidatePath = path.join(STAGING, "candidate.pptx");
const validatedPath = path.join(STAGING, `validated-${Date.now()}.pptx`);
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);
const { finalizePresentation } = await import(pathToFileURL(path.join(SKILL_DIR, "container_tools/artifact_tool_utils.mjs")).href);
const finalResult = await finalizePresentation({
  explicitTotalSlideCount: 8,
  requiredNativeChartOwnerSlides: [5, 6],
  requiredNativeTableOwnerSlides: [],
  materializeLiteralChartWorkbooks: true,
  workspaceDir: ROOT,
  candidatePath,
  finalPath: validatedPath,
  pythonExecutable: RUNTIME_PYTHON,
  integrityValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: ["--expected-slide-size-emu", "12192000,6858000", "--validate-bullet-geometry", "--validate-heading-fit"],
  fontPolicy: { basis: "design", families: [FONT] },
  verifyArtifactToolImport: true,
  receiptPath: path.join(VALIDATION, `receipt-${Date.now()}.json`),
});
await fs.copyFile(validatedPath, FINAL_OUT);
console.log(JSON.stringify({ ...finalResult, deliveredPath: FINAL_OUT }, null, 2));
