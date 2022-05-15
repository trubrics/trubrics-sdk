lint:
	@pre-commit run --all-files

local-build:
	@pip install -e .
