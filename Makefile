upgrade-pip:
	@python3 -m pip install --upgrade pip

lint:
	@pre-commit run --all-files

local-build:
	@pip install -e .

streamlit-demo:
	@streamlit run examples/app_generate_trubric.py

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

example-run-trubric:
	@trubrics run \
	--no-save-ui \
	--trubric-config-path "examples/classification_titanic" \
	--trubric-output-file-path "examples/classification_titanic" \
	--trubric-output-file-name "my_new_trubric.json"

save-titanic-tutorial-notebook:
	@python -m ipykernel install --user --name=trubrics-venv
	@jupyter nbconvert \
	--execute examples/classification_titanic/titanic-demo.ipynb \
	--to html --output-dir docs/notebooks/

streamlit-titanic:
	@streamlit run trubrics/example/feedback_app_titanic.py  
