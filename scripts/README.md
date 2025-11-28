# Development Scripts

## Overview
Code quality and development workflow scripts for the RAG system.

## Scripts

### `format.py`
Formats code using Black and isort with consistency checks.
```bash
python scripts/format.py
```

### `quality.py` 
Runs comprehensive quality checks:
- Black formatting validation
- Import sorting validation  
- Flake8 linting
- Test suite execution
```bash
python scripts/quality.py
```

### `dev.py`
Complete development workflow:
1. Code formatting
2. Quality checks
```bash
python scripts/dev.py
```

## Makefile Commands

```bash
# Install dependencies
make install

# Format code
make format

# Run quality checks  
make check

# Full development workflow
make dev

# Run tests only
make test

# Quick format (no validation)
make fmt

# Lint only
make lint
```

## Code Quality Tools

### Black
- Line length: 88 characters
- Target: Python 3.13
- Excludes: chroma_db, build directories

### isort
- Profile: black (compatible)
- Multi-line output: 3
- Trailing commas: enabled

### Flake8
- Max line length: 88
- Ignores: E203, W503, E501
- Per-file ignores for tests and __init__.py

## Pre-commit Workflow

Recommended workflow before committing:
```bash
make dev
```

This ensures code is properly formatted and passes all quality checks.