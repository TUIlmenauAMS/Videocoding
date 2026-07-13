#write a Python program which implements a variational autoencoder for images, with Pytorch.

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.utils import save_image

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
batch_size = 128
latent_dim = 2

# Custom Dataset class for MNIST
class MNISTDataset(torch.utils.data.Dataset):
    def __init__(self, root, train=True, transform=None, download=True):
        self.data = datasets.MNIST(root=root, train=train, transform=transform, download=download)

    def __getitem__(self, index):
        img, _ = self.data[index]
        return img

    def __len__(self):
        return len(self.data)

# Encoder network
class Encoder(nn.Module):
    def __init__(self):
        super(Encoder, self).__init__()
        
        #The Conv2d layers are like the forward 2D-DCT in conventional image coding, but learned from training data:
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=2, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1)
        self.fc1 = nn.Linear(7 * 7 * 64, 16)
        self.fc2_mean = nn.Linear(16, latent_dim)
        self.fc2_logvar = nn.Linear(16, latent_dim)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        z_mean = self.fc2_mean(x)
        z_logvar = self.fc2_logvar(x)
        return z_mean, z_logvar

# Decoder network
class Decoder(nn.Module):
    def __init__(self):
        super(Decoder, self).__init__()

        self.fc1 = nn.Linear(latent_dim, 16)
        self.fc2 = nn.Linear(16, 7 * 7 * 64)
        #The ConvTranspose2d layers are like the inverse 2D-DCT in conventional image coding, but learned from training data:
        self.conv1 = nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.conv2 = nn.ConvTranspose2d(32, 1, kernel_size=3, stride=2, padding=1, output_padding=1)

    def forward(self, z):
        x = torch.relu(self.fc1(z))
        x = torch.relu(self.fc2(x))
        x = x.view(x.size(0), 64, 7, 7)
        x = torch.relu(self.conv1(x))
        x = torch.sigmoid(self.conv2(x))
        return x

# Variational Autoencoder (VAE) model
class VAE(nn.Module):
    def __init__(self):
        super(VAE, self).__init__()

        self.encoder = Encoder()
        self.decoder = Decoder()

    def reparameterize(self, z_mean, z_logvar):
        std = torch.exp(0.5 * z_logvar)
        eps = torch.randn_like(std)
        return z_mean + eps * std #added noise, can be seen as from qunatization/de-quantization

    def forward(self, x):
        z_mean, z_logvar = self.encoder(x)
        z = self.reparameterize(z_mean, z_logvar)
        x_recon = self.decoder(z)
        return x_recon, z_mean, z_logvar

# Loss function
# Added noise is basically the quantization noise in an image coder application.
# More noise means larger quantization step-size and hence lower bit-rate.
# Combination of reconstruction loss (or error), and a goal of the added noise variance of 1
def vae_loss(x, x_recon, z_mean, z_logvar):
    reconstruction_loss = nn.functional.binary_cross_entropy(x_recon, x, reduction='sum')
    kl_divergence_loss = -0.5 * torch.sum(1 + z_logvar - z_mean.pow(2) - z_logvar.exp())
    return reconstruction_loss + kl_divergence_loss
    #The relative weighting of the reconstruction loss and the kl_divergence_loss (the noise variance goal of 1) determines 
    #the trade-off point between bit-rate and quality.

# Train the VAE model
def train_vae(model, dataloader, optimizer, num_epochs):
    model.train()
    for epoch in range(num_epochs):
        total_loss = 0.0
        for batch_idx, data in enumerate(dataloader):
            data = data.to(device)
            optimizer.zero_grad()

            # Forward pass
            recon_batch, z_mean, z_logvar = model(data)

            # Calculate loss
            loss = vae_loss(data, recon_batch, z_mean, z_logvar)

            # Backpropagation and optimization
            loss.backward()
            total_loss += loss.item()
            optimizer.step()

            if batch_idx % 100 == 0:
                print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                      .format(epoch+1, num_epochs, batch_idx+1, len(dataloader), loss.item() / len(data)))

        print('Epoch [{}/{}], Average Loss: {:.4f}'.format(epoch+1, num_epochs, total_loss / len(dataloader.dataset)))

# Test the VAE model
def test_vae(model, dataloader):
    model.eval()
    with torch.no_grad():
        for batch_idx, data in enumerate(dataloader):
            data = data.to(device)
            recon_batch, z_mean, z_logvar = model(data)
            std = torch.exp(0.5 * z_logvar)
            print("tester: z_mean=", z_mean, "std=", std)
            #print("z_mean/std=", z_mean/std)
            print("mean estimated bits per image: ", latent_dim* torch.mean(torch.log2(torch.abs(z_mean/std)+1)))
            if batch_idx == 0:
                comparison = torch.cat([data[:8], recon_batch[:8]])
                save_image(comparison.cpu(), 'reconstruction.png', nrow=8)
                break

#Main section ---------------------------------------------------------
# Initialize VAE model
model = VAE().to(device)

# Define the data transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

# Load and preprocess the MNIST dataset
train_dataset = MNISTDataset(root='./data', train=True, transform=transform, download=True)
test_dataset = MNISTDataset(root='./data', train=False, transform=transform, download=True)

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# Define the optimizer
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Train the VAE
num_epochs = 10
train_vae(model, train_dataloader, optimizer, num_epochs)

# Test the VAE
test_vae(model, test_dataloader)

#----------------Image importer and pre-processor------------------
#can you write a python function which converts a png or jpeg image into a format which is suitable for this encoder?

#Apply encoder to an image:
#Convert image to torch format:

import torch
from PIL import Image
from torchvision import transforms

def preprocess_image(image_path):
    # Open the image file
    image = Image.open(image_path).convert("L")  # Convert to grayscale

    # Define the transformation pipeline
    transform = transforms.Compose([
        transforms.Resize((28, 28)),  # Resize the image to 28x28
        transforms.ToTensor(),  # Convert the image to a PyTorch tensor
        transforms.Normalize((0.1307,), (0.3081,))  # Normalize the image, important because of the non-linearities in neural networks.
    ])

    # Apply the transformation pipeline to the image
    preprocessed_image = transform(image).unsqueeze(0)

    return preprocessed_image

# Example usage:
image_path = "TUI.png" #"image.png"
preprocessed_image = preprocess_image(image_path)
preprocessed_image = preprocessed_image.to(device) #move input to device

recon_batch, z_mean, z_logvar = model(preprocessed_image)
std = torch.exp(0.5 * z_logvar)
print("External image: z_mean=", z_mean, "std=", std)
print("Estimated bits for image: ", latent_dim* torch.mean(torch.log2(torch.abs(z_mean/std)+1)))
save_image(recon_batch.cpu(), 'reconstructionb.png')

#---------------------
#Show images:
image = Image.open(r'reconstruction.png')
image.show()
print("Comparison: Above: original. Below: after encoding and decoding. Observe the differences")

imageb = Image.open(r'reconstructionb.png')
imageb.show()
print("Test image after encoding and decoding. Observe that it now also looks like a handwritten digit!")

