"""
Fit and test a neural network model.
"""

__all__ = ["NeuralNetwork"]

from sklearn.neural_network import MLPClassifier
from numpy import mean


class NeuralNetwork:
    """
    A wrapper class around sklearn.neural_network.MLPClassifier
    """
    def __init__(self, hidden_layer_sizes=(2,), learning_rate="constant", alpha=0.0001):
        """
        The NeuralNetwork constructor.

        Arguments:
            hidden_layer_sizes -- A tuple representing the number and sizes of hidden layers.
                                  Each index represents a layer, and the value at that index
                                  represents the number of neurons at that layer. Defaults to
                                  (2,).
            learning_rate -- A string representing the learning rate schedule for weight updates.
                             Options are "constant", "invscaling", or "adaptive". Defaults to
                             "constant".
            alpha -- A float representing the regularizer alpha. Defaults to 0.0001.
        """
        self.classifier = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation="tanh", learning_rate=learning_rate, alpha=alpha, solver="sgd")

    def train(self, data, labels):
        """
        Train the classifier.

        Arguments:
            data -- A numpy array representing the training data.
            labels -- A numpy array representing the training labels.
                      Must be N rows x 1 column, where N is the number of
                      training data examples.
        """
        self.classifier.fit(data, labels)

    def test(self, data, labels):
        """
        Test the classifier.

        Arguments:
            data -- A numpy array representing the testing data.
            labels -- A numpy array representing the testing labels.
                      Must be N rows x 1 column, where N is the number of
                      testing data examples.
        """
        predictions = self.classifier.predict(data)
        accuracy = mean(predictions == labels)
        return accuracy
