import torch
from torch import nn
from tqdm.auto import tqdm
from torchvision import transforms
from torchvision.datasets import MNIST  # Training dataset
from torchvision.utils import make_grid
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from markipy.nn.gans.generator import get_gen_loss, Generator
from markipy.nn.gans.discriminator import get_disc_loss, Discriminator
from markipy.nn.commons import show_tensor_images, make_noise
from markipy.basic import date


torch.manual_seed(0)  # Set for testing purposes, please do not change!

PROJECT="MNIST"
VERSIONE="0.1"
RUN="11"

# default `log_dir` is "runs" - we'll be more specific here\
logs=f'runs/{PROJECT}_{VERSIONE}.{date()}#{RUN}'

writer = SummaryWriter(logs)
print(f"Logs at: {logs}")



def log_image_board(writer, images, label):
    # create grid of images
    img_grid = torchvision.utils.make_grid(images)

    # show images
    matplotlib_imshow(img_grid, one_channel=True)

    # write to tensorboard
    writer.add_image(label, img_grid)


if __name__ == "__main__":


    # Mnist Playground
    device = torch.device('cuda')
    n_epochs = 200
    noise_c = 1 
    noise_w = noise_b = 8
    z_dim = (noise_c, noise_w, noise_b)
    display_step = 500
    batch_size = 128
    lr = 0.00001
    
    # Weights and Biases. Profiler
    # wandb.init(project=PROJECT)
    # config = wandb.config
    # # Hyperparameters and Store
    # config.n_epochs = n_epochs
    # config.z_dim = z_dim 
    # config.display_step = display_step
    # config.batch_size = batch_size
    # config.lr = lr
    # config.device = device

    
    # Load MNIST dataset as tensors
    dataloader = DataLoader(
        MNIST('.', download=True, transform=transforms.ToTensor()),
        batch_size=batch_size,
        shuffle=True)

    criterion = nn.BCEWithLogitsLoss()
    gen = Generator().to(device)
    gen_opt = torch.optim.Adam(gen.parameters(), lr=lr)
    disc = Discriminator().to(device)
    disc_opt = torch.optim.Adam(disc.parameters(), lr=lr)

 
    cur_step = 0
    mean_generator_loss = 0
    mean_discriminator_loss = 0
    test_generator = True  # Whether the generator should be tested
    gen_loss = False
    error = False

    print("Start Training Loop")
    for epoch in range(n_epochs):
        
        # Dataloader returns the batches
        for real, label in tqdm(dataloader):
            cur_batch_size = len(real)

            # Flatten the batch of real images from the dataset
            real = real.view(cur_batch_size, -1).to(device)

            ### Update discriminator ###
            # Zero out the gradients before backpropagation
            disc_opt.zero_grad()

            # Calculate discriminator loss
            disc_loss = get_disc_loss(gen, disc, criterion, real, label,  cur_batch_size, z_dim, device)

            # Update gradients
            disc_loss.backward(retain_graph=True)

            # Update optimizer
            disc_opt.step()

            # For testing purposes, to keep track of the generator weights
            if test_generator:
                old_generator_weights = gen.gen[0][0].weight.detach().clone()

            # Update gradients
            gen_opt.zero_grad()

            # Update optimizer
            gen_loss = get_gen_loss(gen, disc, criterion, label, cur_batch_size, z_dim, device)

            # Update gradients
            gen_loss.backward(retain_graph=True)

            # Update optimizer
            gen_opt.step()

            # For testing purposes, to check that your code changes the generator weights
            if test_generator:
                try:
                    assert lr > 0.0000002 or (gen.gen[0][0].weight.grad.abs().max() < 0.0005 and epoch == 0)
                    assert torch.any(gen.gen[0][0].weight.detach().clone() != old_generator_weights)
                    
                except:
                    error = True
                    
                    # wandb.log({"no_training": 1, "epoch": epoch, "loss": loss})
                    print("Runtime tests have failed")

            # Keep track of the average discriminator loss
            mean_discriminator_loss += disc_loss.item() / display_step

            # Keep track of the average generator loss
            mean_generator_loss += gen_loss.item() / display_step

            ### Visualization code ###
            if cur_step % display_step == 0 and cur_step > 0:

                # wandb.log({ "Epoch" : epoch, "step": cur_step , "Generator_Loss" : mean_generator_loss, "Discriminator_Loss": mean_discriminator_loss })
                print(f"Epoch {epoch}, step {cur_step}: Generator loss: {mean_generator_loss}, discriminator loss: {mean_discriminator_loss}")

                noise = make_noise(cur_batch_size, z_dim, device=device)
                # noise = scale_noise_by_label_number(noise, label)
                fake = gen(noise)
                show_tensor_images(fake)
                show_tensor_images(real)
                
                mean_generator_loss = 0
                mean_discriminator_loss = 0
            
            # Increase step
            cur_step += 1
        

    
