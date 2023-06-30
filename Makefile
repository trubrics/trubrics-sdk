upgrade-pip:
	@python3 -m pip install --upgrade pip

lint:
	@pre-commit run --all-files

local-build:
	@pip install -e .

docs-serve:
	@mkdocs serve

install: upgrade-pip
	@pip install -r requirements.txt

install-dev: upgrade-pip local-build
	@pip install -r requirements-dev.txt

test:
	@pytest

test-coverage:
	@pytest --cov=trubrics tests
