import torch
from torch import nn

from markipy.nn.commons import make_noise
from markipy.nn.commons import get_linear_block, get_conv2d_block


def get_disc_block(channel_in, channel_out):
    return nn.Sequential(
        get_conv2d_block(channel_in, channel_out, ks=5, normalize=False, activation=nn.LeakyReLU(0.2)),
        nn.MaxPool2d((3, 3), stride=(1, 1))
    )


class Discriminator(nn.Module):
    """
    Discriminator Class
    Values:
        im_dim: the dimension of the images, fitted for the dataset used, a scalar
            (MNIST images are 28x28 = 784 so that is your default)
        hidden_dim: the inner dimension, a scalar
    """

    def __init__(self, im_dim=784, hidden_dim=32):
        super(Discriminator, self).__init__()
        self.disc = nn.Sequential(
            get_disc_block(1, 10),
            get_disc_block(10, 20),
            get_disc_block(20, 30),
            get_disc_block(30, 2),
            nn.Flatten(),
            nn.Linear(800, im_dim)
        )

    def forward(self, image):
        """
        Function for completing a forward pass of the discriminator: Given an image tensor,
        returns a 1-dimension tensor representing fake/real.
        Parameters:
            image: a flattened image tensor with dimension (im_dim)
        """
        return self.disc(image.view(image.shape[0], 1, 28, 28))

    # Needed for grading
    def get_disc(self):
        """
        Returns:
            the sequential model
        """
        return self.disc


def get_disc_loss(gen, disc, criterion, real, label, num_images, z_dim, device):
    """
    Return the loss of the discriminator given inputs.
    Parameters:
        gen: the generator model, which returns an image given z-dimensional noise
        disc: the discriminator model, which returns a single-dimensional prediction of real/fake
        criterion: the loss function, which should be used to compare
               the discriminator's predictions to the ground truth reality of the images
               (e.g. fake = 0, real = 1)
        real: a batch of real images
        num_images: the number of images the generator should produce,
                which is also the length of the real images
        z_dim: the dimension of the noise vector, a scalar
        device: the device type
    Returns:
        disc_loss: a torch scalar loss value for the current batch
    """
    #     These are the steps you will need to complete:
    #       1) Create noise vectors and generate a batch (num_images) of fake images.
    #            Make sure to pass the device argument to the noise.
    #       2) Get the discriminator's prediction of the fake image
    #            and calculate the loss. Don't forget to detach the generator!
    #            (Remember the loss function you set earlier -- criterion. You need a
    #            'ground truth' tensor in order to calculate the loss.
    #            For example, a ground truth tensor for a fake image is all zeros.)
    #       3) Get the discriminator's prediction of the real image and calculate the loss.
    #       4) Calculate the discriminator's loss by averaging the real and fake loss
    #            and set it to disc_loss.
    #     Note: Please do not use concatenation in your solution. The tests are being updated to
    #           support this, but for now, average the two losses as described in step (4).
    #     *Important*: You should NOT write your own loss function here - use criterion(pred, true)!

    noise = make_noise(num_images, z_dim, device=device)
    # noise = scale_noise_by_label_number(noise, label)
    x_gen = gen(noise)

    y_fake = disc(x_gen)
    loss_fake = criterion(y_fake, torch.zeros_like(y_fake))

    y_real = disc(real)
    loss_real = criterion(y_real, torch.ones_like(y_real))

    disc_loss = (loss_fake + loss_real) / 2

    return disc_loss


if __name__ == '__main__':

    from pytorch_model_summary import summary

    n_sample = 1
    img_c = 1 
    img_w = img_b = 28

    noise_input = make_noise( n_sample, (img_c, img_w, img_b), device='cuda')
    
    disc = Discriminator().cuda()

    print(summary(disc, noise_input,  show_input=True))
    print(summary(disc, noise_input,  show_input=False))




