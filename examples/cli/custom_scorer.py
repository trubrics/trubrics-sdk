import numpy as np
from sklearn.metrics import make_scorer


def my_custom_loss_func(y_true, y_pred):
    diff = np.abs(y_true - y_pred).max()
    return np.log1p(diff)


custom_score = make_scorer(my_custom_loss_func, greater_is_better=False)
custom_scorers = {"my_custom_loss": custom_score}
