import numpy as np

def absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Compute the absolute error loss.

    Arguments:
        y_true -- Ground truth (correct) target values.
        y_pred -- Predicted values.

    Returns:
        nd.array -- The losses as an array of floats.
    """
    return np.abs(y_true - y_pred)

absolute_error.c_derivative = "absolute_error"

def squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Compute the squared error loss.

    This is the default loss function used in fitting and selecting graphs from QGraphs.

    Arguments:
        y_true -- Ground truth (correct) target values.
        y_pred -- Predicted values.

    Returns:
        nd.array -- The losses as an array of floats.
    """

    # Some graphs may prodce very large/small predictions. This can result in an overflow which we ignore. 
    # Graphs that behave like this will perform bad and be discarded by the trainer 
    with np.errstate(over="ignore"):
        return np.power((y_pred - y_true), 2)

squared_error.c_derivative = "squared_error"

def binary_cross_entropy(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Compute the cross entropy loss between the labels and predictions.

    This is a good alternative choice for binary classification problems. If cannot be used for fitting QGraphs with output data that is not binary. Doing so will result in a RuntimeError.

    Arguments:
        y_true -- Ground truth (correct) target values.
        y_pred -- Predicted values.

    Returns:
        nd.array -- The losses as an array of floats.
    """
    epsilon = 1e-7
    y_pred = np.clip(y_pred, epsilon, 1. - epsilon)
    y_true = y_true.astype(int)

    if (y_true>1).any() or (y_true<0).any():
        raise RuntimeError("Binary cross entropy loss function requires boolean truth values")

    return -y_true*np.log(y_pred) - (1-y_true)*np.log(1-y_pred)


binary_cross_entropy.c_derivative = "binary_cross_entropy"


def _get_loss_function(name_or_func):
    # The loss function was provided instead of the name.
    # Return the function itself, if it is among the
    # known loss functions.
    if type(name_or_func).__name__ == "function":
        name_or_func = name_or_func.__name__

    if name_or_func in ("absolute_error"):
        return absolute_error
    if name_or_func in ("squared_error"):
        return squared_error
    if (name_or_func in ("categorical_cross_entropy", "binary_cross_entropy")):
        return binary_cross_entropy

    raise ValueError("Unknown loss provided")
