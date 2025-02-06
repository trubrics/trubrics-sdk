.PHONY: help install_requirements install_dev_requirements

UV_VERSION=0.5.26

help:
	@echo "Available commands:"
	@echo "  install_requirements     Install production dependencies using uv"
	@echo "  install_dev_requirements Install development dependencies using uv"

setup_uv_venv:
	@echo "Create uv virtual env"
	pip install uv==${UV_VERSION}
	uv venv

install_requirements:
	@echo "Installing production dependencies..."
	uv pip compile pyproject.toml -o requirements.txt
	uv sync --no-dev

install_dev_requirements:
	@echo "Installing development dependencies..."
	uv pip compile pyproject.toml -o requirements.txt
	uv sync
