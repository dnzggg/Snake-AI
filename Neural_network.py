import math

import numpy as np


def sigmoid(value):
    new_value = 1/(1 + math.e**-value)
    return new_value


def sigmoid_derivative(value):
    new_value = sigmoid(value)*(1-sigmoid(value))
    return new_value


class NeuralNetwork:
    def __init__(self, x, y):
        self.input = x
        self.w1 = np.random.rand(self.input.shape[1], 4)
        self.w2 = np.random.rand(4, 1)
        self.y = y
        self.output = np.zeros(y.shape)

    def feed_forward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.w1))
        self.output = sigmoid(np.dot(self.layer1, self.w2))

    def back_propagation(self):
        d_weigths2 = np.dot(self.layer1.T, (2*(self.y - self.output)*sigmoid_derivative(self.output)))
        d_weigths1 = np.dot(self.input.T, (np.dot(2*(self.y - self.output)*sigmoid_derivative(self.output), self.w2.T) *
                                         sigmoid_derivative(self.layer1)))

        self.w1 += d_weigths1
        self.w2 += d_weigths2
