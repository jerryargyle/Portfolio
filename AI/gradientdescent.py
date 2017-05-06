"""
Fit and test a gradient descent classification model.
"""

__all__ = ["GradientDescent"]

from sklearn.linear_model import SGDClassifier
from numpy import mean


class GradientDescent:
    """
    A wrapper class around sklearn.linear_model.SGDClassifier.
    """
    def __init__(self, loss='log', penalty='none', n_iter=5, eta0=0.0, alpha=0.0001):
        """
        The GradientDescent constructor.

        Arguments:
            loss -- A string representing the type of loss function to use. Defaults to 'hinge'. 
                    Options include 'log', 'hinge', and 'perceptron'.
                    See http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html#sklearn.linear_model.SGDClassifier
                    for details.
            penalty -- A string representing the type of regularizer to use. Defaults to 'none'.
                       Options include 'l2', 'l1', 'elasticnet', or 'none'.
            n_iter -- An integer representing the number of times to iterate over the data while
                      training the algorithm. Defaults to 5.
            eta0 -- A float representing the learning rate. If left at the default 0.0 value,
                    it is not used.
            alpha -- A float representing the regularizer alpha. Defaults to 0.0001.
        """
        learning_rate = 'constant' if eta0 > 0.0 else 'optimal'
        self.classifier = SGDClassifier(loss=loss, penalty=penalty, n_jobs=-1, learning_rate=learning_rate, eta0=eta0)

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
