.PHONY: help install install-dev test test-verbose test-coverage lint format clean clean-all run-example docs

help:
	@echo "Self-Healing Playwright Framework - Available Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  make install         - Install package and dependencies"
	@echo "  make install-dev     - Install package with development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test            - Run unit tests"
	@echo "  make test-verbose    - Run tests with verbose output"
	@echo "  make test-coverage   - Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            - Run code linting (flake8)"
	@echo "  make format          - Format code with black"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           - Clean build artifacts and cache"
	@echo "  make clean-all       - Deep clean (includes .venv)"
	@echo ""
	@echo "Running:"
	@echo "  make run-example     - Run the example usage script"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs            - Open documentation"
	@echo ""

install:
	pip install -r requirements.txt
	playwright install chromium

install-dev:
	pip install -e ".[dev]"
	playwright install chromium

test:
	python -m pytest tests/

test-verbose:
	python -m pytest tests/ -v

test-cov.pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-all: clean
	rm -rf .venv/
	@echo "Deep clean complete. Run 'make install' to reinstall."

run-example:
	python examples/example_usage.py

docs:
	@echo "Opening documentation..."
	@if command -v open >/dev/null 2>&1; then \
		open docs/README.md; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open docs/README.md; \
	else \
		echo "Please open docs/README.md in your browser"; \
	fi
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

run-example:
	python examples/example_usage.py
