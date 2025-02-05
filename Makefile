.PHONY: help install_requirements install_dev_requirements

help:
	@echo "Available commands:"
	@echo "  install_requirements     Install production dependencies using uv"
	@echo "  install_dev_requirements Install development dependencies using uv"

install_requirements:
	@echo "Installing production dependencies..."
	uv pip compile pyproject.toml -o requirements.txt
	uv sync --no-dev

install_dev_requirements:
	@echo "Installing development dependencies..."
	uv pip compile pyproject.toml -o requirements.txt
	uv sync
