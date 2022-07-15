lint:
	@pre-commit run --all-files

local-build:
	@pip install -e .

train-titanic:
	@python examples/training/titanic.py

streamlit-demo:
	@streamlit run examples/streamlit/app-titanic.py

docs-serve:
	@mkdocs serve

install:
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt

install-dev: local-build
	@python -m pip install --upgrade pip
	@pip install -r requirements-dev.txt

test:
	@pytest

test-coverage:
	@pytest --cov=trubrics tests

example-trubric:
	@trubrics run examples/trubrics_config.py
