import torch
from torch import nn
from tqdm.auto import tqdm
from torchvision import transforms
from torchvision.datasets import MNIST
from torchvision.utils import make_grid
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

from markipy.nn import DEFAULT_DATA_PATH
from markipy import makedirs

from .gen import Generator, get_noise
from .dis import Discriminator

torch.manual_seed(0)  # Set for testing purposes, please do not change!


def show_tensor_images(image_tensor, num_images=25, size=(1, 28, 28), save_path=None):
    '''
    Function for visualizing images: Given a tensor of images, number of images, and
    size per image, plots and prints the images in an uniform grid.
    '''
    image_tensor = (image_tensor + 1) / 2
    image_unflat = image_tensor.detach().cpu()
    image_grid = make_grid(image_unflat[:num_images], nrow=5)
    plt.imshow(image_grid.permute(1, 2, 0).squeeze())
    if save_path is not None:
        plt.savefig(save_path, format='jpg')
    else:
        plt.show()


def train():
    criterion = nn.BCEWithLogitsLoss()
    z_dim = 64
    display_step = 500
    batch_size = 128
    # A learning rate of 0.0002 works well on DCGAN
    lr = 0.0002

    # These parameters control the optimizer's momentum, which you can read more about here:
    # https://distill.pub/2017/momentum/ but you don’t need to worry about it for this course!
    beta_1 = 0.5
    beta_2 = 0.999
    device = 'cuda'

    # You can tranform the image values to be between -1 and 1 (the range of the tanh activation)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,)),
    ])

    dataloader = DataLoader(
        MNIST(DEFAULT_DATA_PATH / 'MNIST', download=True, transform=transform),
        batch_size=batch_size,
        shuffle=True)

    gen = Generator(z_dim).to(device)
    gen_opt = torch.optim.Adam(gen.parameters(), lr=lr, betas=(beta_1, beta_2))
    disc = Discriminator().to(device)
    disc_opt = torch.optim.Adam(disc.parameters(), lr=lr, betas=(beta_1, beta_2))

    # You initialize the weights to the normal distribution
    # with mean 0 and standard deviation 0.02
    def weights_init(m):
        if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
            torch.nn.init.normal_(m.weight, 0.0, 0.02)
        if isinstance(m, nn.BatchNorm2d):
            torch.nn.init.normal_(m.weight, 0.0, 0.02)
            torch.nn.init.constant_(m.bias, 0)

    gen = gen.apply(weights_init)
    disc = disc.apply(weights_init)

    n_epochs = 50
    cur_step = 0
    mean_generator_loss = 0
    mean_discriminator_loss = 0

    # Image results
    images_path = 'tmp/coursera/mnist/week2/'
    makedirs(images_path)

    for epoch in range(n_epochs):
        # Dataloader returns the batches
        for real, _ in tqdm(dataloader):
            cur_batch_size = len(real)
            real = real.to(device)

            ## Update discriminator ##
            disc_opt.zero_grad()
            fake_noise = get_noise(cur_batch_size, z_dim, device=device)
            fake = gen(fake_noise)
            disc_fake_pred = disc(fake.detach())
            disc_fake_loss = criterion(disc_fake_pred, torch.zeros_like(disc_fake_pred))
            disc_real_pred = disc(real)
            disc_real_loss = criterion(disc_real_pred, torch.ones_like(disc_real_pred))
            disc_loss = (disc_fake_loss + disc_real_loss) / 2

            # Keep track of the average discriminator loss
            mean_discriminator_loss += disc_loss.item() / display_step
            # Update gradients
            disc_loss.backward(retain_graph=True)
            # Update optimizer
            disc_opt.step()

            ## Update generator ##
            gen_opt.zero_grad()
            fake_noise_2 = get_noise(cur_batch_size, z_dim, device=device)
            fake_2 = gen(fake_noise_2)
            disc_fake_pred = disc(fake_2)
            gen_loss = criterion(disc_fake_pred, torch.ones_like(disc_fake_pred))
            gen_loss.backward()
            gen_opt.step()

            # Keep track of the average generator loss
            mean_generator_loss += gen_loss.item() / display_step

            ## Visualization code ##
            if cur_step % display_step == 0 and cur_step > 0:
                print(
                    f"Step {cur_step}: Generator loss: {mean_generator_loss}, discriminator loss: {mean_discriminator_loss}")
                show_tensor_images(fake, save_path=f'{images_path}/{cur_step}-fake.jpg')
                show_tensor_images(real, save_path=f'{images_path}/{cur_step}-real.jpg')
                mean_generator_loss = 0
                mean_discriminator_loss = 0
            cur_step += 1
