.PHONY: help test pipeline temporal assort centrality embeddings notebook report slides study-guide package build-all serve status

PYTHON := MPLCONFIGDIR=/tmp .venv/bin/python
PYTEST := MPLCONFIGDIR=/tmp .venv/bin/pytest

help:
	@echo "======================================================================"
	@echo " Department of Machine Learning — Bitcoin Trust Link Prediction"
	@echo "======================================================================"
	@echo " make test        : Run full automated unit and integration test suite"
	@echo " make pipeline    : Execute master end-to-end link prediction pipeline"
	@echo " make temporal    : Execute chronological temporal backtest (2010-2016)"
	@echo " make assort      : Plot degree assortativity mixing topology"
	@echo " make centrality  : Compute K-core shell decomposition & centralities"
	@echo " make embeddings  : Benchmark Graph Representation Learning (SVD baseline)"
	@echo " make notebook    : Recompile & execute master Jupyter notebook"
	@echo " make report      : Recompile formal 8-page academic PDF report"
	@echo " make slides      : Recompile 14-slide presentation deck (PPTX & PDF)"
	@echo " make study-guide : Recompile printable team viva study guide PDF"
	@echo " make package     : Rebuild dataset package ZIP with SHA-256 manifest"
	@echo " make build-all   : Rebuild all deliverables end-to-end"
	@echo " make serve       : Launch live web dashboard on http://localhost:5000"
	@echo " make status      : Inspect all deliverables and verification hashes"
	@echo "======================================================================"

test:
	$(PYTEST) tests/test_pipeline.py

pipeline:
	$(PYTHON) src/run_pipeline.py

temporal:
	$(PYTHON) src/temporal_evaluation.py

assort:
	$(PYTHON) scripts/plot_assortativity.py

centrality:
	$(PYTHON) scripts/compute_k_core_centralities.py

embeddings:
	$(PYTHON) src/embedding_baseline.py

notebook:
	$(PYTHON) scripts/build_link_prediction_notebook.py

report:
	$(PYTHON) reports/build_link_prediction_report.py

slides:
	$(PYTHON) slides/build_link_prediction_deck.py

study-guide:
	$(PYTHON) reports/build_study_guide_pdf.py

package:
	$(PYTHON) scripts/package_dataset.py

build-all: pipeline temporal assort centrality embeddings report slides study-guide notebook package test
	@echo "All deliverables successfully built and verified!"

serve:
	$(PYTHON) src/serve.py 5000

status:
	@echo "=== Deliverables Status ==="
	@ls -lh reports/link_prediction_report.pdf slides/link_prediction_presentation.pdf dataset_package/bitcoin_trust_dataset_package.zip notebooks/bitcoin_link_prediction_recommendation.ipynb
