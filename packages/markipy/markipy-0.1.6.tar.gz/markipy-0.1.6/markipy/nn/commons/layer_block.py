import torch
from torch import nn

def get_linear_block(input_dim, output_dim, normalize=True, activation=nn.ReLU(inplace=True)):
    """
    Function for returning nn.Sequential (Linear + BatchNorm1D + Activation)
    block of type neural network given input and output dimensions.
    Parameters:
        input_dim: the dimension of the input vector, a scalar
        output_dim: the dimension of the output vector, a scalar
        normilize: True if add batch_normalization
        activation: the activation function from torch nn 
    Returns:
        nn torch module with a linear transformation
        followed by a batch normalization and then a activation (default relu)
    """
    modules = []
    modules.append(nn.Linear(input_dim, output_dim))
    if normalize:
        modules.append(nn.BatchNorm1d(output_dim))
    modules.append(activation)

    return nn.Sequential(*modules)

def get_conv2d_block(in_channels, out_channels, normalize=True,  ks=5, s=1, p=2, d=1, activation=nn.LeakyReLU(0.1)):
    modules = []

    modules.append(nn.Conv2d(in_channels, out_channels, kernel_size=ks, stride=s, padding=p, dilation=d))
    if normalize:
         modules.append(nn.BatchNorm2d(out_channels))
    modules.append(activation)
    return nn.Sequential(*modules)


def get_conv1d_block(in_channels, out_channels, normalize=True,  ks=5, s=1, p=2, d=1, activation=nn.LeakyReLU(0.1)):
    modules = []

    modules.append(nn.Conv2d(in_channels, out_channels, kernel_size=ks, stride=s, padding=p, dilation=d))
    if normalize:
         modules.append(nn.BatchNorm2d(out_channels))
    modules.append(activation)
    return nn.Sequential(*modules)



def get_deconv2d_block(in_channels, out_channels, normalize=True,  ks=5, s=1, p=2, d=1, activation=nn.LeakyReLU(0.1)):
    modules = []
    modules.append(nn.ConvTranspose2d(in_channels, out_channels, kernel_size=ks, stride=s, padding=p, dilation=d))
    if normalize:
         modules.append(nn.BatchNorm2d(out_channels))
    modules.append(activation)
    return nn.Sequential(*modules)
