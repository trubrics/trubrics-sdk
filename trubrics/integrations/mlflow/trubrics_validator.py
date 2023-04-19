from mlflow import MlflowClient
from mlflow.models.evaluation import ModelEvaluator


class TrubricsValidator(ModelEvaluator):
    def can_evaluate(self, model_type, **kwargs):
        return model_type in ["classifier", "regressor"]

    def evaluate(self, run_id, evaluator_config, **kwargs):
        self.client = MlflowClient()
        self.run_id = run_id
        self.evaluator_config = evaluator_config

        new_trubric = self.evaluator_config["trubric_run"].set_new_trubric()
        self.client.log_dict(self.run_id, dictionary=new_trubric.dict(), artifact_file="demo-trubric.json")
        new_trubric.raise_trubric_failure()
