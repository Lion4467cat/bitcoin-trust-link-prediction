#!/usr/bin/env python3
"""
Cross-platform CLI runner for Windows, macOS, and Linux.
Allows teammates without GNU `make` (especially on Windows) to run any project target:

Usage:
  python run.py serve        # Launch interactive web dashboard at http://localhost:5000
  python run.py test         # Run the 16 automated unit & integration tests
  python run.py pipeline     # Run the end-to-end link prediction pipeline
  python run.py report       # Rebuild the 8-page academic report PDF
  python run.py slides       # Rebuild the 14-slide presentation deck (.pptx & .pdf)
  python run.py study-guide  # Rebuild the 6-page team presentation study guide PDF
  python run.py build-all    # Rebuild all deliverables and run tests
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_step(args: list[str], desc: str) -> None:
    print(f"\n=== {desc} ===")
    env = os.environ.copy()
    env.setdefault("MPLCONFIGDIR", tempfile.gettempdir())
    env.setdefault("PYTHONUTF8", "1")
    subprocess.run([sys.executable, *args], cwd=str(ROOT), env=env, check=True)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "help"

    if cmd == "serve":
        port = sys.argv[2] if len(sys.argv) > 2 else "5000"
        run_step(["src/serve.py", port], f"Starting Interactive Web Dashboard on http://localhost:{port}")
    elif cmd == "test":
        run_step(["-m", "pytest", "tests/test_pipeline.py"], "Running Automated Test Suite (16 Tests)")
    elif cmd == "pipeline":
        run_step(["src/run_pipeline.py"], "Running Master Link Prediction Pipeline")
    elif cmd == "temporal":
        run_step(["src/temporal_evaluation.py"], "Running Chronological Temporal Backtest (2010-2016)")
    elif cmd == "assort":
        run_step(["scripts/plot_assortativity.py"], "Plotting Degree Assortativity Mixing")
    elif cmd == "centrality":
        run_step(["scripts/compute_k_core_centralities.py"], "Computing K-Core Decomposition & Centralities")
    elif cmd == "embeddings":
        run_step(["src/embedding_baseline.py"], "Running Spectral SVD-64 Embedding Baseline")
    elif cmd == "report":
        run_step(["reports/build_link_prediction_report.py"], "Building 8-Page Academic Report PDF")
    elif cmd == "slides":
        run_step(["slides/build_link_prediction_deck.py"], "Building 14-Slide Presentation Deck (PPTX/PDF)")
    elif cmd == "study-guide":
        run_step(["reports/build_study_guide_pdf.py"], "Building 6-Page Team Study Guide PDF")
    elif cmd == "notebook":
        run_step(["scripts/build_link_prediction_notebook.py"], "Building & Executing Master Jupyter Notebook")
    elif cmd == "package":
        run_step(["scripts/package_dataset.py"], "Packaging Dataset ZIP Archive with SHA-256 Manifest")
    elif cmd == "build-all":
        for sub, desc in [
            (["src/run_pipeline.py"], "Master Link Prediction Pipeline"),
            (["src/temporal_evaluation.py"], "Chronological Temporal Backtest"),
            (["scripts/plot_assortativity.py"], "Degree Assortativity Mixing"),
            (["scripts/compute_k_core_centralities.py"], "K-Core & Centrality Rankings"),
            (["src/embedding_baseline.py"], "SVD-64 Spectral Embedding Baseline"),
            (["reports/build_link_prediction_report.py"], "8-Page Academic Report PDF"),
            (["slides/build_link_prediction_deck.py"], "14-Slide Presentation Deck"),
            (["reports/build_study_guide_pdf.py"], "6-Page Team Study Guide PDF"),
            (["scripts/build_link_prediction_notebook.py"], "Master Jupyter Notebook"),
            (["scripts/package_dataset.py"], "Dataset Package ZIP"),
            (["-m", "pytest", "tests/test_pipeline.py"], "Automated Test Suite"),
        ]:
            run_step(sub, desc)
        print("\nAll deliverables successfully built and verified!")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
