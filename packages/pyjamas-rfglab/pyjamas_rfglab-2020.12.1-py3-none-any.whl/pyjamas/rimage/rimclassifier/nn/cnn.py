"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import numpy
from sklearn.model_selection import train_test_split
import theano
import theano.tensor as T
from theano.tensor.nnet import conv2d
from theano.tensor.nnet import softmax
from theano.tensor import shared_randomstreams
from theano.tensor.signal import pool
from theano.tensor.nnet import sigmoid

from pyjamas.rimage.rimclassifier.featurecalculator_rowofpixels import FeatureCalculatorROP


#### Main class used to construct and train networks
class Network(object):
    DEFAULT_RAND_STATE: int = 42
    DEFAULT_BATCH_SIZE = 16
    DEFAULT_EPOCH_NUMBER = 60
    DEFAULT_LEARNING_RATE = 0.001
    DEFAULT_TEST_SIZE = 0.2

    def __init__(self, layers, epochs=DEFAULT_EPOCH_NUMBER, mini_batch_size=DEFAULT_BATCH_SIZE,
                 learning_rate=DEFAULT_LEARNING_RATE, GPU=False):
        """Takes a list of `layers`, describing the network architecture, and
        a value for the `mini_batch_size` to be used during training
        by stochastic gradient descent.
        """
        if GPU:
            print("Trying to run using a GPU.")
            try:
                theano.config.device = 'gpu'
                theano.config.floatX = 'float32'
            except:
                print(f"Failed to configure GPU.\nRunning with a CPU.")
        else:
            print("Running with a CPU.")

        self.layers = layers
        self.epochs = epochs
        self.mini_batch_size = mini_batch_size
        self.learning_rate = learning_rate
        self.params = [param for layer in self.layers for param in layer.params]
        self.x = T.matrix("x")
        self.y = T.ivector("y")
        init_layer = self.layers[0]
        init_layer.set_inpt(self.x, self.x, self.mini_batch_size)
        for j in range(1, len(self.layers)):
            prev_layer, layer = self.layers[j - 1], self.layers[j]
            layer.set_inpt(
                prev_layer.output, prev_layer.output_dropout, self.mini_batch_size)
        self.output = self.layers[-1].output
        self.output_dropout = self.layers[-1].output_dropout
        self.fc = FeatureCalculatorROP()

    def SGD(self, training_data, epochs, mini_batch_size, learning_rate,
            validation_data, lmbda=0.0):
        # Train the network using mini-batch stochastic gradient descent.
        training_x, training_y = training_data
        validation_x, validation_y = validation_data

        # compute number of minibatches for training, validation and testing
        num_training_batches = int(size(training_data) / mini_batch_size)
        num_validation_batches = int(size(validation_data) / mini_batch_size)

        # define the (regularized) cost function, symbolic gradients, and updates
        l2_norm_squared = sum((layer.w ** 2).sum() for layer in self.layers)
        cost = self.layers[-1].cost(self) + \
               0.5 * lmbda * l2_norm_squared / num_training_batches
        grads = T.grad(cost, self.params)
        updates = [(param, param - learning_rate * grad)
                   for param, grad in zip(self.params, grads)]

        # define functions to train a mini-batch, and to compute the
        # accuracy in validation and test mini-batches.
        i = T.lscalar()  # mini-batch index
        train_mb = theano.function(
            [i], cost, updates=updates,
            givens={
                self.x:
                    training_x[i * self.mini_batch_size: (i + 1) * self.mini_batch_size],
                self.y:
                    training_y[i * self.mini_batch_size: (i + 1) * self.mini_batch_size]
            })
        validate_mb_accuracy = theano.function(
            [i], self.layers[-1].accuracy(self.y),
            givens={
                self.x:
                    validation_x[i * self.mini_batch_size: (i + 1) * self.mini_batch_size],
                self.y:
                    validation_y[i * self.mini_batch_size: (i + 1) * self.mini_batch_size]
            })

        # Do the actual training
        best_validation_accuracy = 0.0
        for epoch in range(epochs):
            for minibatch_index in range(num_training_batches):
                iteration = num_training_batches * epoch + minibatch_index
                if iteration % 1000 == 0:
                    print(f"Training mini-batch number {iteration}")
                cost_ij = train_mb(minibatch_index)
                if (iteration + 1) % num_training_batches == 0:
                    validation_accuracy = numpy.mean([validate_mb_accuracy(j) for j in range(num_validation_batches)])
                    print(f"Epoch {epoch}: validation accuracy {(validation_accuracy * 100.):.2f}%")
                    if validation_accuracy > best_validation_accuracy:
                        print(f"This is the best validation accuracy to date.")
                        best_validation_accuracy = validation_accuracy
                        best_iteration = iteration
        print(f"Finished training network.")
        print(
            f"Best validation accuracy of {(best_validation_accuracy * 100):.2f}% obtained at iteration {best_iteration}.")

    def fit(self, x: numpy.ndarray, y: numpy.ndarray):
        # Make sure the category array has a minimum at zero (sklearn methods like +1 and -1 as category labels).
        if numpy.amin(y) < 0:
            y[numpy.where(y < 0)] = 0

        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=Network.DEFAULT_TEST_SIZE,
                                                            random_state=Network.DEFAULT_RAND_STATE)

        training_data = shared((X_train, y_train))
        validation_data = shared((X_test, y_test))

        self.SGD(training_data=training_data, validation_data=validation_data, epochs=self.epochs,
                 mini_batch_size=self.mini_batch_size, learning_rate=self.learning_rate)

    def predict(self, test_features: numpy.ndarray) -> numpy.ndarray:
        # The image data need to be repeated *mini_batch_size, as the batch size is embedded in the networks architecture.
        test_x, test_y = shared((numpy.repeat(test_features, self.mini_batch_size, 0),
                                 numpy.repeat(numpy.asarray([1]), self.mini_batch_size, 0)))

        i = T.lscalar()  # mini-batch index

        self.test_mb_predictions = theano.function(
            [i], self.layers[-1].y_out,
            givens={
                self.x:
                    test_x[i * self.mini_batch_size: (i + 1) * self.mini_batch_size]
            })

        y_out = self.test_mb_predictions(0)

        return numpy.asarray([y_out[0]])  # This output is consistent with the scikit-learn predict functions.


    def predict_proba(self, test_features: numpy.ndarray) -> numpy.ndarray:
        # The image data need to be repeated *mini_batch_size, as the batch size is embedded in the networks architecture.
        test_x, test_y = shared((numpy.repeat(test_features, self.mini_batch_size, 0),
                                 numpy.repeat(numpy.asarray([1]), self.mini_batch_size, 0)))

        i = T.lscalar()  # mini-batch index

        self.test_mb_predictions = theano.function(
            [i], (self.layers[-1].y_out, self.layers[-1].p_out),
            givens={
                self.x:
                    test_x[i * self.mini_batch_size: (i + 1) * self.mini_batch_size]
            })

        _, p_out = self.test_mb_predictions(0)

        return numpy.asarray([[1-p_out[0], p_out[0]]])  # This output is consistent with the scikit-learn predict_proba functions.


    def predict_batch(self, test_features: numpy.ndarray) -> numpy.ndarray:
        if test_features.shape[0] != self.mini_batch_size:
            return numpy.ndarray([])

        # The image data need to be repeated *mini_batch_size, as the batch size is embedded in the networks architecture.
        test_x, test_y = shared((test_features, numpy.repeat(numpy.asarray([-1]), self.mini_batch_size, 0)))

        self.test_mb_predictions = theano.function(
            [], (self.layers[-1].y_out, self.layers[-1].p_out),
            givens={
                self.x:
                    test_x
            })

        y_out, p_out = self.test_mb_predictions()

        return numpy.asarray([y_out, p_out])

#### Define layer types

class ConvPoolLayer(object):
    """Used to create a combination of a convolutional and a max-pooling
    layer.  A more sophisticated implementation would separate the
    two, but for our purposes we'll always use them together, and it
    simplifies the code, so it makes sense to combine them.
    """

    def __init__(self, filter_shape, image_shape, poolsize=(2, 2),
                 activation_fn=sigmoid):
        """`filter_shape` is a tuple of length 4, whose entries are the number
        of filters, the number of input feature maps, the filter height, and the
        filter width.
        `image_shape` is a tuple of length 4, whose entries are the
        mini-batch size, the number of input feature maps, the image
        height, and the image width.
        `poolsize` is a tuple of length 2, whose entries are the y and
        x pooling sizes.
        """
        self.filter_shape = filter_shape
        self.image_shape = image_shape
        self.poolsize = poolsize
        self.activation_fn = activation_fn
        # initialize weights and biases
        n_out = (filter_shape[0] * numpy.prod(filter_shape[2:]) / numpy.prod(poolsize))
        self.w = theano.shared(
            numpy.asarray(
                numpy.random.normal(loc=0, scale=numpy.sqrt(1.0 / n_out), size=filter_shape),
                dtype=theano.config.floatX),
            borrow=True)
        self.b = theano.shared(
            numpy.asarray(
                numpy.random.normal(loc=0, scale=1.0, size=(filter_shape[0],)),
                dtype=theano.config.floatX),
            borrow=True)
        self.params = [self.w, self.b]

    def set_inpt(self, inpt, inpt_dropout, mini_batch_size):
        self.inpt = inpt.reshape(self.image_shape)
        conv_out = conv2d(
            input=self.inpt, filters=self.w, filter_shape=self.filter_shape,
            input_shape=self.image_shape)
        pooled_out = pool.pool_2d(
            input=conv_out, ws=self.poolsize, ignore_border=True)
        self.output = self.activation_fn(
            pooled_out + self.b.dimshuffle('x', 0, 'x', 'x'))
        self.output_dropout = self.output  # no dropout in the convolutional layers


class FullyConnectedLayer(object):

    def __init__(self, n_in, n_out, activation_fn=sigmoid, p_dropout=0.0):
        self.n_in = n_in
        self.n_out = n_out
        self.activation_fn = activation_fn
        self.p_dropout = p_dropout
        # Initialize weights and biases
        self.w = theano.shared(
            numpy.asarray(
                numpy.random.normal(
                    loc=0.0, scale=numpy.sqrt(1.0 / n_out), size=(n_in, n_out)),
                dtype=theano.config.floatX),
            name='w', borrow=True)
        self.b = theano.shared(
            numpy.asarray(numpy.random.normal(loc=0.0, scale=1.0, size=(n_out,)),
                          dtype=theano.config.floatX),
            name='b', borrow=True)
        self.params = [self.w, self.b]

    def set_inpt(self, inpt, inpt_dropout, mini_batch_size):
        self.inpt = inpt.reshape((mini_batch_size, self.n_in))
        self.output = self.activation_fn(
            (1 - self.p_dropout) * T.dot(self.inpt, self.w) + self.b)
        self.y_out = T.argmax(self.output, axis=1)
        self.inpt_dropout = dropout_layer(
            inpt_dropout.reshape((mini_batch_size, self.n_in)), self.p_dropout)
        self.output_dropout = self.activation_fn(
            T.dot(self.inpt_dropout, self.w) + self.b)

    def accuracy(self, y):
        """Return the accuracy for the mini-batch."""
        return T.mean(T.eq(y, self.y_out))


class SoftmaxLayer(object):

    def __init__(self, n_in, n_out, p_dropout=0.0):
        self.n_in = n_in
        self.n_out = n_out
        self.p_dropout = p_dropout
        # Initialize weights and biases
        self.w = theano.shared(
            numpy.zeros((n_in, n_out), dtype=theano.config.floatX),
            name='w', borrow=True)
        self.b = theano.shared(
            numpy.zeros((n_out,), dtype=theano.config.floatX),
            name='b', borrow=True)
        self.params = [self.w, self.b]

    def set_inpt(self, inpt, inpt_dropout, mini_batch_size):
        self.inpt = inpt.reshape((mini_batch_size, self.n_in))
        self.output = softmax((1 - self.p_dropout) * T.dot(self.inpt, self.w) + self.b)
        # self.y_out = T.argmax(self.output, axis=1)
        self.p_out, self.y_out = T.max_and_argmax(self.output, axis=1)
        self.inpt_dropout = dropout_layer(
            inpt_dropout.reshape((mini_batch_size, self.n_in)), self.p_dropout)
        self.output_dropout = softmax(T.dot(self.inpt_dropout, self.w) + self.b)

    def cost(self, net):
        """Return the log-likelihood cost."""
        return -T.mean(T.log(self.output_dropout)[T.arange(net.y.shape[0]), net.y])

    def accuracy(self, y):
        "Return the accuracy for the mini-batch."
        return T.mean(T.eq(y, self.y_out))


#### Miscellanea
def size(data):
    """Return the size of the dataset `data`."""
    return data[0].get_value(borrow=True).shape[0]


def dropout_layer(layer, p_dropout):
    srng = shared_randomstreams.RandomStreams(
        numpy.random.RandomState(0).randint(999999))
    mask = srng.binomial(n=1, p=1 - p_dropout, size=layer.shape)
    return layer * T.cast(mask, theano.config.floatX)


def shared(data):
    """Place the data into shared variables.  This allows Theano to copy
    the data to the GPU, if one is available.
    """
    shared_x = theano.shared(
        numpy.asarray(data[0], dtype=theano.config.floatX), borrow=True)
    shared_y = theano.shared(
        numpy.asarray(data[1], dtype=theano.config.floatX), borrow=True)
    return shared_x, T.cast(shared_y, "int32")


# Activation functions for neurons
def linear(z):
    return z


def ReLU(z):
    return T.maximum(0.0, z)


def tanh(z):
    return T.tanh(z)
