from torchvision.utils import make_grid
import torch.nn.functional as F
import matplotlib.pyplot as plt
import torch

DEFAULT_TENSOR_DEVICE = torch.device('cuda')


def show_tensor_images(image_tensor, num_images=25, size=(1, 28, 28), nrow=5, show=True):
    """
    Function for visualizing images: Given a tensor of images, number of images, and
    size per image, plots and prints the images in a uniform grid.
    """
    image_unflat = image_tensor.detach().cpu().view(-1, *size)
    image_grid = make_grid(image_unflat[:num_images], nrow=nrow)
    plt.imshow(image_grid.permute(1, 2, 0).squeeze())
    if show:
        plt.show()


def make_noise(n_samples, dimensions, device='cuda'):
    """
    Function for creating noise vectors: Given the dimensions (n_samples, z_dim),
    creates a tensor of that shape filled with random numbers from the normal distribution.
    Parameters:
        n_samples: the number of samples to generate, a scalar
        dimensions: the dimension of the noise vector, a scalar
        device: the device type
    """
    # NOTE: To use this on GPU with device='cuda', make sure to pass the device
    # argument to the function you use to generate the noise.
    if not isinstance(dimensions, tuple):
        dimensions = (dimensions,)
    return torch.randn((n_samples,) + dimensions, device=device)


def make_one(n_samples, dimensions, device=DEFAULT_TENSOR_DEVICE):
    if not isinstance(dimensions, tuple):
        dimensions = (dimensions,)
    return torch.ones(size=(n_samples,) + dimensions, device=device)


def make_ramp(n_samples, dimensions, device=DEFAULT_TENSOR_DEVICE):
    if not isinstance(dimensions, tuple):
        dimensions = (dimensions,)
    X = torch.ones(size=(n_samples,) + dimensions, device=device)
    i = 0
    for x in X:
        x += i
        i += 1
    return X


# def log_image_board(writer, images, label):
#     # show images
#     image_unflat = image_tensor.detach().cpu().view(-1, *size)
#     image_grid = make_grid(image_unflat[:num_images], nrow=5)
#     show_tensor_images(img_grid, show=False)
#     # write to tensorboard
#     writer.add_image(label, img_grid)

