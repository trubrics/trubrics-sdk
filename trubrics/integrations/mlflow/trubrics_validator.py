import pandas as pd
from mlflow import MlflowClient
from mlflow.models.evaluation import ModelEvaluator

from trubrics.context import DataContext
from trubrics.validations import Trubric
from trubrics.validations.run import TrubricRun


class TrubricsValidator(ModelEvaluator):
    def can_evaluate(self, model_type, **kwargs):
        return model_type in ["classifier", "regressor"]

    # pylint: disable=unused-argument
    def evaluate(self, *, model, dataset, run_id, evaluator_config, **kwargs):
        """
        Args:
            run_id: The ID of the MLflow Run to which to log results
            dataset: mlflow dataset. Is overwritten if a data_context is provided in evaluator_config
            evaluator_config: A dictionary of additional configurations for the trubrics evaluator. Contains:
                trubric_path: the path to the trubric file
                model: the model to validate
                tags: optional tags to add to the trubric
                failing_severity: optional severity level to raise the trubric. Default is "error"
                custom_scorers: optional dict of custom scorers for computing custom metrics
                custom_validator: optional custom validator
                slicing_functions: optional dict of slicing functions
                data_context: an optional data context to validate the model on
        """
        self.client = MlflowClient()
        self.run_id = run_id
        self.evaluator_config = evaluator_config

        X = dataset.features_data
        y = dataset.labels_data
        testing_data = pd.DataFrame(X, columns=dataset.feature_names).assign(target=y)
        data_context = self.evaluator_config.get("data_context") or DataContext(
            target="target", testing_data=testing_data
        )

        trubric_run_context = TrubricRun(
            data_context=data_context,
            model=self.evaluator_config["model"],
            model_name=model.metadata.artifact_path,
            model_version=model.metadata.model_uuid,
            trubric=Trubric.parse_file(self.evaluator_config["trubric_path"]),
            tags=self.evaluator_config.get("tags") or ["mlflow-run"],
            failing_severity=self.evaluator_config.get("failing_severity") or "error",
            custom_scorers=self.evaluator_config.get("custom_scorers"),
            slicing_functions=self.evaluator_config.get("slicing_functions"),
            custom_validator=self.evaluator_config.get("custom_validator"),
            metadata={
                "mlflow_run_id": self.run_id,
                "mlflow.username": self.client.get_run(self.run_id).data.tags["mlflow.user"],
            },
        )

        new_trubric = trubric_run_context.set_new_trubric()
        self.client.log_dict(self.run_id, dictionary=new_trubric.dict(), artifact_file="demo-trubric.json")
        new_trubric.raise_trubric_failure()
