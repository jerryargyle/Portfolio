"""
Load the data and train the models, varying the hyperparameters. Output graphs of the results.
"""

import idxreader
from gradientdescent import GradientDescent as gradient_descent_model
from neuralnetwork import NeuralNetwork as neural_network_model

from sklearn.datasets import fetch_20newsgroups_vectorized

from os import path
from sys import stdout
from matplotlib import pyplot as plt


def load_MNIST_data():
    """
    Load the MNIST dataset.
    """
    dir = path.dirname(__file__)
    training_data_filepath = path.join(dir, "..", "MNIST", "digits-train", "train-images-idx3-ubyte")
    training_labels_filepath = path.join(dir, "..", "MNIST", "digits-train", "train-labels-idx1-ubyte")
    test_data_filepath = path.join(dir, "..", "MNIST", "digits-test", "t10k-images-idx3-ubyte")
    test_labels_filepath = path.join(dir, "..", "MNIST", "digits-test", "t10k-labels-idx1-ubyte")

    training_data = idxreader.read(training_data_filepath)
    training_labels = idxreader.read(training_labels_filepath)
    test_data = idxreader.read(test_data_filepath)
    test_labels = idxreader.read(test_labels_filepath)

    return training_data, training_labels, test_data, test_labels


def load_20_newsgroups_data():
    """
    Load the 20 newsgroups dataset.
    """
    newsgroups_train = fetch_20newsgroups_vectorized(subset="train")
    newsgroups_test = fetch_20newsgroups_vectorized(subset="test")

    training_data = newsgroups_train.data
    training_labels = newsgroups_train.target
    test_data = newsgroups_test.data
    test_labels = newsgroups_test.target

    return training_data, training_labels, test_data, test_labels


def test_and_plot_gradient_descent(training_data, training_labels, test_data, test_labels, figure):
    """
    Train and test a gradient descent model using various hyperparameters, and plot the results.

    Arguments:
        training_data -- A numpy array representing the data used to train the model
        training_labels -- A numpy array representing the labels for the training data
        test_data -- A numpy array representing the data used to test the model
        test_labels -- A numpy array representing the labels for the test data
        figure -- A matplotlib.pyplot.Figure on which to render the graphs
    """
    # Vary iterations
    print "\nTest varying the iterations"
    print "---------------------------"

    iterations = [1, 2, 3, 10, 50, 100]
    accuracies = []
    for i, iteration in enumerate(iterations):
        stdout.write("\rTesting model {0} of {1}".format(i+1, len(iterations)))
        stdout.flush()
        gd_model = gradient_descent_model(n_iter=iteration)
        gd_model.train(training_data, training_labels)
        accuracies.append(gd_model.test(test_data, test_labels))
    print "\n"

    iter_plot = figure.add_subplot(221)
    iter_plot.set_title("Vary Iterations")
    plt.ylabel("Accuracy")
    plt.xlabel("Iterations")
    plt.plot(iterations, accuracies, "o")
    for point in zip(iterations, accuracies):
        iter_plot.annotate("{0}, {1}".format(*point), xy=point, xytext=(3, 0), textcoords="offset points")

    # Vary learning rate
    print "\nTest varying the learning rate"
    print "------------------------------"

    learning_rates = [0.1, 0.3, 0.6, 0.9]
    accuracies = []
    for i, learning_rate in enumerate(learning_rates):
        stdout.write("\rTesting model {0} of {1}".format(i+1, len(learning_rates)))
        stdout.flush()
        gd_model = gradient_descent_model(eta0=learning_rate)
        gd_model.train(training_data, training_labels)
        accuracies.append(gd_model.test(test_data, test_labels))
    print "\n"

    learning_rate_plot = figure.add_subplot(222)
    learning_rate_plot.set_title("Vary Learning Rate")
    plt.ylabel("Accuracy")
    plt.xlabel("Learning Rate")
    plt.plot(learning_rates, accuracies, "o")
    for point in zip(learning_rates, accuracies):
        learning_rate_plot.annotate("{0}, {1}".format(*point), xy=point, xytext=(3, 0), textcoords="offset points")

    # Vary regularizer
    print "\nTest varying the regularizer alpha"
    print "----------------------------------"

    alphas = [0.0001, 0.001, 0.005, 0.01, 0.05, 0.1]
    accuracies = []

    for i, alpha in enumerate(alphas):
        stdout.write("\rTesting model {0} of {1}".format(i+1, len(alphas)))
        stdout.flush()
        gd_model = gradient_descent_model(penalty="l2", alpha=alpha)
        gd_model.train(training_data, training_labels)
        accuracies.append(gd_model.test(test_data, test_labels))
    print "\n"

    alpha_plot = figure.add_subplot(223)
    alpha_plot.set_title("Vary Regularizer Alpha")
    plt.ylabel("Accuracy")
    plt.xlabel("Regularizer Alpha")
    plt.plot(alphas, accuracies, "o")
    for point in zip(alphas, accuracies):
        alpha_plot.annotate("{0}, {1}".format(*point), xy=point, xytext=(3, 0), textcoords="offset points")

    # Vary loss function
    print "\nTest varying the loss function"
    print "------------------------------"

    loss_functions = ['log', 'hinge', 'perceptron']
    x_values = []
    accuracies = []

    for i, loss_function in enumerate(loss_functions):
        stdout.write("\rTesting model {0} of {1}".format(i+1, len(loss_functions)))
        stdout.flush()
        gd_model = gradient_descent_model(penalty="l2", loss=loss_function)
        gd_model.train(training_data, training_labels)
        accuracies.append(gd_model.test(test_data, test_labels))
        x_values.append(i)
    print "\n"

    loss_plot = figure.add_subplot(224)
    loss_plot.set_title("Vary Loss Function")
    plt.ylabel("Accuracy")
    plt.xlabel("Loss Function")
    plt.plot(x_values, accuracies, "o")
    plt.xticks(x_values, loss_functions)
    for point in zip(x_values, accuracies):
        loss_plot.annotate("{0}".format(point[1]), xy=point, xytext=(3, 0), textcoords="offset points")


def test_and_plot_neural_network(training_data, training_labels, test_data, test_labels, figure):
    # Vary the number of hidden nodes
    print "\nTest varying the number of hidden nodes"
    print "---------------------------------------"

    hidden_nodes = [2, 5, 10]
    accuracies = []

    for i, hidden_node in enumerate(hidden_nodes):
        stdout.write("\rTesting model {0} of {1}".format(i+1, len(hidden_nodes)))
        stdout.flush()
        nn_model = neural_network_model(hidden_layer_sizes=(hidden_node,))
        nn_model.train(training_data, training_labels)
        accuracies.append(nn_model.test(test_data, test_labels))
    print "\n"

    hidden_nodes_plot = figure.add_subplot(131)
    hidden_nodes_plot.set_title("Vary # of Hidden Nodes")
    plt.ylabel("Accuracy")
    plt.xlabel("Hidden Nodes")
    plt.plot(hidden_nodes, accuracies, "o")
    for point in zip(hidden_nodes, accuracies):
        hidden_nodes_plot.annotate("{0}, {1}".format(*point), xy=point, xytext=(3, 0), textcoords="offset points")

    # Vary the learning rate
    print "\nTest varying the learning rate"
    print "------------------------------"

    learning_rates = ["constant", "adaptive"]
    x_values = []
    accuracies = []

    for i, learning_rate in enumerate(learning_rates):
        stdout.write("\rTesting model {0} of {1}".format(i+1, len(learning_rates)))
        stdout.flush()
        nn_model = neural_network_model(learning_rate=learning_rate)
        nn_model.train(training_data, training_labels)
        x_values.append(i)
        accuracies.append(nn_model.test(test_data, test_labels))
    print "\n"

    learning_rate_plot = figure.add_subplot(132)
    learning_rate_plot.set_title("Vary Learning Rate")
    plt.ylabel("Accuracy")
    plt.xlabel("Learning Rate")
    plt.xticks(x_values, learning_rates)
    plt.plot(x_values, accuracies, "o")
    for point in zip(x_values, accuracies):
        learning_rate_plot.annotate("{0}".format(point[1]), xy=point, xytext=(3, 0), textcoords="offset points")

    # Vary the regularizer alpha
    print "\nTest varying the regularizer alpha"
    print "----------------------------------"

    alphas = [0.0001, 0.001, 0.005, 0.01, 0.05, 0.1]
    accuracies = []

    for i, alpha in enumerate(alphas):
        stdout.write("\rTesting model {0} of {1}".format(i+1, len(alphas)))
        stdout.flush()
        nn_model = neural_network_model(alpha=alpha)
        nn_model.train(training_data, training_labels)
        accuracies.append(nn_model.test(test_data, test_labels))
    print "\n"

    alpha_plot = figure.add_subplot(133)
    alpha_plot.set_title("Vary Regularizer Alpha")
    plt.ylabel("Accuracy")
    plt.xlabel("Regularizer Alpha")
    plt.plot(alphas, accuracies, "o")
    for point in zip(alphas, accuracies):
        alpha_plot.annotate("{0}, {1}".format(*point), xy=point, xytext=(3, 0), textcoords="offset points")


def main():
    print "\nLoading MNIST data..."
    mnist_training_data, mnist_training_labels, mnist_testing_data, mnist_testing_labels = load_MNIST_data()

    # Convert the image data into two-dimensional arrays
    # by flattening each image to a 1-dimensional array
    mnist_training_data = mnist_training_data.reshape(len(mnist_training_data), -1)
    mnist_testing_data = mnist_testing_data.reshape(len(mnist_testing_data), -1)

    print "\nGradient Descent: MNIST Data"
    print "============================"

    mnist_gradient_descent_fig = plt.figure(1, figsize=(12, 12))
    mnist_gradient_descent_fig.suptitle("MNIST Data: Gradient Descent Model")

    test_and_plot_gradient_descent(mnist_training_data, mnist_training_labels, mnist_testing_data, mnist_testing_labels, mnist_gradient_descent_fig)

    print "\nNeural Network: MNIST Data"
    print "=========================="

    mnist_neural_network_fig = plt.figure(2, figsize=(14, 6))
    mnist_neural_network_fig.suptitle("MNIST Data: Neural Network Model")

    test_and_plot_neural_network(mnist_training_data, mnist_training_labels, mnist_testing_data, mnist_testing_labels, mnist_neural_network_fig)

    print "\nLoading 20 newsgroups data..."
    newsgroups_training_data, newsgroups_training_labels, newsgroups_testing_data, newsgroups_testing_labels = load_20_newsgroups_data()

    print "\nGradient Descent: 20 Newsgroups Data"
    print "===================================="

    newsgroups_gradient_descent_fig = plt.figure(3, figsize=(12, 12))
    newsgroups_gradient_descent_fig.suptitle("20 Newsgroups Data: Gradient Descent Model")

    test_and_plot_gradient_descent(newsgroups_training_data, newsgroups_training_labels, newsgroups_testing_data, newsgroups_testing_labels, newsgroups_gradient_descent_fig)

    print "\nNeural Network: 20 Newsgroups Data"
    print "=================================="

    newsgroups_neural_network_fig = plt.figure(4, figsize=(14, 6))
    newsgroups_neural_network_fig.suptitle("20 Newsgroups Data: Neural Network Model")

    test_and_plot_neural_network(newsgroups_training_data, newsgroups_training_labels, newsgroups_testing_data, newsgroups_testing_labels, newsgroups_neural_network_fig)

    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.show()

if __name__ == "__main__":
    main()
