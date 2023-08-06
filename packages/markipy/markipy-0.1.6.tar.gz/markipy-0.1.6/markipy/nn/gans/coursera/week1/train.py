import torch
from torch import nn
from tqdm.auto import tqdm
from torchvision import transforms
from torchvision.datasets import MNIST  # Training dataset
from torchvision.utils import make_grid
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

from markipy.nn import DEFAULT_DATA_PATH
from markipy import makedirs

from .gen import Generator, get_noise, get_gen_loss
from .dis import Discriminator, get_disc_loss

torch.manual_seed(0)  # Set for testing purposes, please do not change!


def show_tensor_images(image_tensor, num_images=25, size=(1, 28, 28)):
    '''
    Function for visualizing images: Given a tensor of images, number of images, and
    size per image, plots and prints the images in a uniform grid.
    '''
    image_unflat = image_tensor.detach().cpu().view(-1, *size)
    image_grid = make_grid(image_unflat[:num_images], nrow=5)
    plt.imshow(image_grid.permute(1, 2, 0).squeeze())
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

    # Image results
    images_path = '/tmp/coursera/mnist/week1/'
    makedirs(images_path)

    n_epochs = 50
    cur_step = 0
    mean_generator_loss = 0
    mean_discriminator_loss = 0
    test_generator = True  # Whether the generator should be tested
    gen_loss = False
    error = False
    for epoch in range(n_epochs):

        for real, _ in tqdm(dataloader):
            cur_batch_size = len(real)

            # Flatten the batch of real images from the dataset
            real = real.view(cur_batch_size, -1).to(device)

            ### Update discriminator ###
            # Zero out the gradients before backpropagation
            disc_opt.zero_grad()

            # Calculate discriminator loss
            disc_loss = get_disc_loss(gen, disc, criterion, real, cur_batch_size, z_dim, device)

            # Update gradients
            disc_loss.backward(retain_graph=True)

            # Update optimizer
            disc_opt.step()

            # For testing purposes, to keep track of the generator weights
            if test_generator:
                old_generator_weights = gen.gen[0][0].weight.detach().clone()

            ### Update generator ###
            #     Hint: This code will look a lot like the discriminator updates!
            #     These are the steps you will need to complete:
            #       1) Zero out the gradients.
            #       2) Calculate the generator loss, assigning it to gen_loss.
            #       3) Backprop through the generator: update the gradients and optimizer.

            gen_opt.zero_grad()
            gen_loss = get_gen_loss(gen, disc, criterion, cur_batch_size, z_dim, device)
            gen_loss.backward(retain_graph=True)
            gen_opt.step()

            # For testing purposes, to check that your code changes the generator weights
            if test_generator:
                try:
                    assert lr > 0.0000002 or (gen.gen[0][0].weight.grad.abs().max() < 0.0005 and epoch == 0)
                    assert torch.any(gen.gen[0][0].weight.detach().clone() != old_generator_weights)
                except:
                    error = True
                    print("Runtime tests have failed")

            # Keep track of the average discriminator loss
            mean_discriminator_loss += disc_loss.item() / display_step

            # Keep track of the average generator loss
            mean_generator_loss += gen_loss.item() / display_step

            ### Visualization code ###
            if cur_step % display_step == 0 and cur_step > 0:
                print(
                    f"Epoch {epoch}, step {cur_step}: Generator loss: {mean_generator_loss}, discriminator loss: {mean_discriminator_loss}")
                fake_noise = get_noise(cur_batch_size, z_dim, device=device)
                fake = gen(fake_noise)
                show_tensor_images(fake)
                show_tensor_images(real)
                mean_generator_loss = 0
                mean_discriminator_loss = 0
            cur_step += 1
