from typing import Callable


class BaseModel:
    def __init__(self, model: Callable):
        self.model = model

    def predict(self, data):
        try:
            return self.model.predict(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict() method.") from error

    def predict_proba(self, data):
        try:
            return self.model.predict_proba(data)
        except AttributeError as error:
            raise AttributeError("Model has no .predict_proba() method.") from error
