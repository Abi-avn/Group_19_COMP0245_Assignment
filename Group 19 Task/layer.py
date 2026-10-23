import numpy as np

'''
Use this code to create the layers for convolution
Quite basic at the moment 

'''

class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    # Returns output
    def forward(self, input):
        pass

    # Updates parameters and returns input gradient
    def backward(self, output_gradient, learning_rate):
        pass


class Dense(Layer):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.weights = np.random.randn(output_size, input_size)
        self.bias = np.random.randn(output_size, 1)

    def forward(self, input):
        self.input = input
        return np.dot(self.weights, self.input) + self.bias

    def backward(self, output_gradient, learning_rate):
        weights_gradient = np.dot(output_gradient, self.input.T)
        # Compute the input gradient BEFORE updating the weights
        input_gradient = np.dot(self.weights.T, output_gradient)

        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * output_gradient
        return input_gradient