from setuptools import find_packages, setup

setup(
    name="mflow-test-plugin",
    version="0.0.1",
    description="Test plugin for MLflow",
    packages=find_packages(),
    install_requires=["mlflow"],
    entry_points={
        "mlflow.model_evaluator": "trubrics=trubrics_validator:TrubricsValidator",
    },
)
