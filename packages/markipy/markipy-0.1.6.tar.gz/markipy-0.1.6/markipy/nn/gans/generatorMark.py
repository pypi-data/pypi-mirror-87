import torch
from torch import nn
from markipy.nn.commons import make_noise, get_linear_block, get_conv2d_block, get_deconv2d_block
import torch.nn.functional as F


class Generator(nn.Module):
    """
    Generator Class
    Values:
        z_dim: the dimension of the noise vector, a scalar
        im_dim: the dimension of the images, fitted for the dataset used, a scalar
          (MNIST images are 28 x 28 = 784 so that is your default)
        hidden_dim: the inner dimension, a scalar
    """

    def __init__(self, input_channel=1, device='cuda'):
        super(Generator, self).__init__()
        self.device = device
        # Build the neural network

        ic = input_channel
        self.oc = 5

        self.m = nn.Upsample(scale_factor=1.2, mode='bilinear')
        self.cv1 = get_conv2d_block(ic, self.oc, ks=5, normalize=True, activation=nn.LeakyReLU(0.2))
        self.f = nn.Flatten(2)

        self.l_hidden = 10
        self.Ln = [nn.Linear(1089, self.l_hidden) for n in range(self.oc)]

        self.bidirectional = 2
        self.ls_hidden = 10

        # Input (seq_len, batch, input_size)
        self.lstm = nn.LSTM(self.l_hidden, self.ls_hidden, 1, dropout=0.33, bidirectional=True)

        self.cv2 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.cv3 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.cv4 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.cv5 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.cv6 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.cv7 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.cv8 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.cv9 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.cv10 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.cv11 = get_conv2d_block(1, 1, ks=3, p=2, normalize=True, activation=nn.LeakyReLU(0.2))

        self.to_init_lstm = True
        self.last_n_batch = 0

    def forward(self, X):
        """
        Function for completing a forward pass of the generator: Given a noise tensor,
        returns generated data.
        Parameters:
            noise: a noise tensor with dimensions (examples, dimensions)
        """

        n_sampled = X.shape[0]

        if self.to_init_lstm or self.last_n_batch != n_sampled:
            self.hn = torch.zeros(self.bidirectional, n_sampled, self.l_hidden, device=self.device)
            self.cn = torch.zeros(self.bidirectional, n_sampled, self.l_hidden, device=self.device)
            self.to_init_lstm = False
            self.last_n_batch = n_sampled

        X = F.leaky_relu(self.m(X), 0.1)
        X = F.leaky_relu(self.cv1(X), 0.1)
        X = F.leaky_relu(self.f(X), 0.1)

        Xn = torch.zeros(n_sampled, self.oc, self.l_hidden, device=self.device)

        for xi in range(self.oc):
            Xn[:, xi, :] = F.leaky_relu(self.Ln[xi](X[:, :1].view(n_sampled, 1089)), 0.1)

        X, (self.hn, self.cn) = self.lstm(Xn.permute(1, 0, 2), (self.hn, self.cn))

        X = X.permute(1, 0, 2)

        X = X.flatten(0);
        X = X.view(n_sampled, 1, 10, 10);

        X = self.cv2(X);

        X = self.cv3(X);

        X = self.cv4(X);

        X = self.cv5(X);

        X = self.cv6(X);

        X = self.cv7(X);

        X = self.cv8(X);

        X = self.cv9(X);

        X = self.cv10(X);

        return X

    # Needed for grading
    def get_gen(self):
        return self.gen


def get_gen_loss(gen, disc, criterion, labels, num_images, z_dim, device):
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

    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = 'cpu'
    n_sample = 1
    noise_c = 1
    noise_w = noise_b = 28

    gen = Generator(input_channel=noise_c, device=device).to(device)
    noise_input = make_noise(n_sample, (noise_c, noise_w, noise_b), device=device)

    print(summary(gen, noise_input, show_input=True))
    print(summary(gen, noise_input, show_input=False))

