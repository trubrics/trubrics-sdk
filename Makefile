lint:
	@pre-commit run --all-files

local-build:
	@pip install -e .

streamlit-demo:
	@streamlit run demo/streamlit/app-titanic.py
