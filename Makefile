lint:
	@pre-commit run --all-files

local-build:
	@pip install -e .

streamlit-demo:
	@streamlit run examples/streamlit/app-titanic.py

auto-docs:
	@sphinx-autobuild docs/source docs/build/html
