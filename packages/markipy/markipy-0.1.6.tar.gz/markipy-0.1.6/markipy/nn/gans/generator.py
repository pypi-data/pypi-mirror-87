import torch
from torch import nn
from markipy.nn.commons import make_noise, get_linear_block, get_conv2d_block, get_deconv2d_block

def get_gen_block(self):
    pass

class Generator(nn.Module):
    """
    Generator Class
    Values:
        z_dim: the dimension of the noise vector, a scalar
        im_dim: the dimension of the images, fitted for the dataset used, a scalar
          (MNIST images are 28 x 28 = 784 so that is your default)
        hidden_dim: the inner dimension, a scalar
    """

    def __init__(self, noise_channel=1):
        super(Generator, self).__init__()
        # Build the neural network
        self.gen = nn.Sequential(
            # Manage the noise Input n_sample, noise_channel
            get_conv2d_block(noise_channel, 10, ks=3, p=1),
            get_deconv2d_block(10, 9, ks=5, p=0),
            get_deconv2d_block(9, 8, ks=5, p=0),
            get_deconv2d_block(8, 7, ks=5, p=0),
            get_deconv2d_block(7, 6, ks=5, p=0),
            get_deconv2d_block(6, 5, ks=5, p=0),
            get_deconv2d_block(5, 4, ks=5, p=0),
            get_deconv2d_block(4, 3, ks=5, p=0),
            
            get_conv2d_block(3, 10, ks=3, p=0, activation=nn.LeakyReLU(0.2)),
            get_conv2d_block(10, 20, ks=3, p=0, activation=nn.LeakyReLU(0.2)),
            get_conv2d_block(20, 30, ks=3, p=0, activation=nn.LeakyReLU(0.2)),
            get_conv2d_block(30, 40, ks=3, p=0, activation=nn.LeakyReLU(0.2)),
            get_conv2d_block(40, 30, ks=3, p=1),
            get_conv2d_block(30, 20, ks=3, p=1),
            get_conv2d_block(20, 10, ks=3, p=1),
            get_conv2d_block(10, 1, ks=3, p=1),
    
            nn.Flatten(),
            nn.Linear(784, 784),
            nn.Sigmoid(),
        )

    def forward(self, noise):
        """
        Function for completing a forward pass of the generator: Given a noise tensor,
        returns generated data.
        Parameters:
            noise: a noise tensor with dimensions (examples, dimensions)
        """
        return self.gen(noise)

    # Needed for grading
    def get_gen(self):
        return self.gen


def get_gen_loss(gen, disc, criterion, labels,  num_images, z_dim, device):
    """
    Return the loss of the generator given inputs.
    Parameters:
        gen: the generator model, which returns an image given z-dimensional noise
        disc: the discriminator model, which returns a single-dimensional prediction of real/fake
        criterion: the loss function, which should be used to compare
               the discriminator's predictions to the ground truth reality of the images
               (e.g. fake = 0, real = 1)
        num_images: the number of images the generator should produce,
                which is also the length of the real images
        z_dim: the dimension of the noise vector, a scalar
        device: the device type
    Returns:
        gen_loss: a torch scalar loss value for the current batch
    """
    #     These are the steps you will need to complete:
    #       1) Create noise vectors and generate a batch of fake images.
    #           Remember to pass the device argument to the get_noise function.
    #       2) Get the discriminator's prediction of the fake image.
    #       3) Calculate the generator's loss. Remember the generator wants
    #          the discriminator to think that its fake images are real
    #     *Important*: You should NOT write your own loss function here - use criterion(pred, true)!

    noise = make_noise(num_images, z_dim, device=device)
    # noise = scale_noise_by_label_number(noise, labels)
    x_gen = gen(noise)

    y_fake = disc(x_gen)
    gen_loss = criterion(y_fake, torch.ones_like(y_fake, device=device))

    return gen_loss


if __name__ == '__main__':

    from pytorch_model_summary import summary


    n_sample = 1
    noise_c = 1 
    noise_w = noise_b = 8

    noise_input = make_noise( n_sample, (noise_c, noise_w, noise_b), device='cuda')
    
    print(summary(Generator().cuda(), noise_input,  show_input=True))
    print(summary(Generator().cuda(), noise_input,  show_input=False))



