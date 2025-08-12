PYTHON ?= python3

.PHONY: setup run benchmark

setup:
	$(PYTHON) -m venv .venv && .venv/bin/pip install -r requirements.txt

run:
	PYTHONPATH=src $(PYTHON) -m src.cli --help

benchmark:
	PYTHONPATH=src $(PYTHON) benchmarks/run_bench.py
