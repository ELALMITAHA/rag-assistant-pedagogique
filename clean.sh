#!/bin/bash

echo "🧹 Cleaning project..."

# ***** REMOVE CACHE DIRECTORIES *****
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +
find . -type d -name ".mypy_cache" -exec rm -rf {} +
find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +

# ***** REMOVE CACHE FILES *****
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

echo "✅ Cleanup done."