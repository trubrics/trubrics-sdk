lint:
	@pre-commit run --all-files

local-build:
	@pip install -e .

train-titanic:
	@python examples/training/titanic.py

streamlit-demo:
	@streamlit run examples/streamlit/app-titanic.py

auto-docs:
	@sphinx-autobuild docs/source docs/build/html

install:
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt

install-dev:
	@python -m pip install --upgrade pip
	@pip install -r requirements-dev.txt

test:
	@pytest
