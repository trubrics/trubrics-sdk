class ExampleCustomModel:
    """
    This is a custom model that scores passengers based on probability of survival.
    """

    def __init__(self, model):
        self.model = model
        self._estimator_type = "regressor"

    def predict(self, df):
        return self.model.predict(df)

    def fit(self, X_train, y_train):
        return self.model.fit(X_train, y_train)

    def get_params(self, deep):
        return {"model": self.model}
