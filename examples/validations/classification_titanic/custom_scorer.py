from sklearn.metrics import accuracy_score, make_scorer


def custom_binary_error(y_true, y_pred):
    """
    An example of an error metric for binary classification.
    """
    accuracy = accuracy_score(y_true, y_pred)
    return round(1 - accuracy, 3)


custom_score = make_scorer(custom_binary_error, greater_is_better=False)
custom_scorers = {"my_custom_loss": custom_score}
