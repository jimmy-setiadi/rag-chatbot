.PHONY: format check quality dev test install

# Install dependencies
install:
	uv sync

# Format code
format:
	python scripts/format.py

# Run quality checks
check:
	python scripts/quality.py

# Full development workflow
dev:
	python scripts/dev.py

# Run tests only
test:
	python -m pytest backend/tests/ -v

# Quick format (no checks)
fmt:
	python -m black backend/
	python -m isort backend/

# Lint only
lint:
	python -m flake8 backend/