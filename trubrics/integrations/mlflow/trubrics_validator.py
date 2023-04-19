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
            data: must be a pandas DataFrame with the following columns.
                This is overwritten if a data_context is provided in evaluator_config.
            evaluator_config: A dictionary of additional configurations for the trubrics evaluator. Contains:
                trubric_path: the path to the trubric file
                model: the model to validate
                data_context: an optional data context to validate the model on
        """
        self.client = MlflowClient()
        self.run_id = run_id
        self.evaluator_config = evaluator_config

        if isinstance(model, str):
            raise Exception("model must be a model object, not a string for the trubrics evaluator")

        X = dataset.features_data
        y = dataset.labels_data
        testing_data = pd.DataFrame(X, columns=dataset.feature_names).assign(target=y)
        data_context = self.evaluator_config.get("data_context") or DataContext(
            target="target", testing_data=testing_data
        )

        trubric_from_file = Trubric.parse_file(self.evaluator_config["trubric_path"])

        trubric_run_context = TrubricRun(
            data_context=data_context,
            model=self.evaluator_config.get("model"),
            model_name=model.metadata.artifact_path,
            model_version=model.metadata.model_uuid,
            trubric=trubric_from_file,
            tags=["nb-demo-new"],
            failing_severity="error",
        )

        new_trubric = trubric_run_context.set_new_trubric()
        self.client.log_dict(self.run_id, dictionary=new_trubric.dict(), artifact_file="demo-trubric.json")
        new_trubric.raise_trubric_failure()
