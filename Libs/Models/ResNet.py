import tensorflow, matplotlib as plt
from keras.layers import Flatten
from keras.layers.core import Dense
from keras.models import Sequential
from keras.optimizers import Adam

def convolutional_block(X, f, filters, layer, block, s=2):
    """
    X -- input tensor
    f -- int, shape of conv window
    filters -- array of filters in conv layer
    layer -- int layer number
    block -- string for layer

    returns 
    x -- output tensor
    """

def identity_block(X, f, filters, stage, block):
    
    pass