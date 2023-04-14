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

save-titanic-tutorial-notebook:
	@python -m ipykernel install --user --name=trubrics-venv
	@jupyter nbconvert \
	--execute examples/classification_titanic/titanic-full-demo.ipynb \
	--to html --output-dir docs/

streamlit-titanic:
	@streamlit run trubrics/example/app_titanic_streamlit.py

gradio-titanic:
	@python trubrics/example/app_titanic_gradio.py

dash-titanic:
	@python trubrics/example/app_titanic_dash.py
