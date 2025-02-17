import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

# Load and preprocess data
def load_data(file_path):
    """Loads and normalizes patient data from an Excel file."""
    df = pd.read_excel(file_path, header=None)
    data = df.select_dtypes(include=[np.number]).values  # Ensure only numeric data is used
    data_range = np.max(data, axis=0) - np.min(data, axis=0)
    data = (data - np.min(data, axis=0)) / (data_range + 1e-8)  # Avoid division by zero
    return data

# Generator Model
class Generator(nn.Module):
    def __init__(self, latent_dim, output_dim):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 128),
            nn.BatchNorm1d(128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, output_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

# Discriminator Model
class Discriminator(nn.Module):
    def __init__(self, input_dim):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

# Train the GAN
def train_gan(data, latent_dim=10, epochs=5000, batch_size=16, lr=0.0002):
    """Trains the GAN to generate synthetic patient data."""
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    patient_dim = data.shape[1]  # Number of features
    generator = Generator(latent_dim, patient_dim).to(device)
    discriminator = Discriminator(patient_dim).to(device)
    
    criterion = nn.BCELoss()
    optimizer_g = optim.Adam(generator.parameters(), lr=lr, betas=(0.5, 0.999))
    optimizer_d = optim.Adam(discriminator.parameters(), lr=lr, betas=(0.5, 0.999))
    
    real_labels = torch.ones(batch_size, 1).to(device)
    fake_labels = torch.zeros(batch_size, 1).to(device)
    
    for epoch in range(epochs):
        # Train Discriminator
        idx = np.random.randint(0, data.shape[0], batch_size)
        real_samples = torch.tensor(data[idx], dtype=torch.float32).to(device)
        noise = torch.randn(batch_size, latent_dim).to(device)
        fake_samples = generator(noise)
        
        d_loss_real = criterion(discriminator(real_samples), real_labels)
        d_loss_fake = criterion(discriminator(fake_samples.detach()), fake_labels)
        d_loss = (d_loss_real + d_loss_fake) / 2
        
        optimizer_d.zero_grad()
        d_loss.backward()
        optimizer_d.step()
        
        # Train Generator
        noise = torch.randn(batch_size, latent_dim).to(device)
        g_loss = criterion(discriminator(generator(noise)), real_labels)
        
        optimizer_g.zero_grad()
        g_loss.backward()
        optimizer_g.step()
        
        if epoch % 500 == 0:
            print(f"Epoch {epoch}/{epochs} | D Loss: {d_loss.item():.4f} | G Loss: {g_loss.item():.4f}")
    
    return generator

# Generate new synthetic patients
def generate_synthetic_patients(generator, num_new_patients=32, latent_dim=10):
    """Uses the trained generator to create new patient data."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    noise = torch.randn(num_new_patients, latent_dim).to(device)
    synthetic_data = generator(noise).detach().cpu().numpy()
    return synthetic_data

# Save synthetic data to Excel
def save_synthetic_data(synthetic_data, file_path):
    """Saves the generated synthetic data to an Excel file."""
    df = pd.DataFrame(synthetic_data)
    df.to_excel(file_path, index=False, header=False)

# Main execution
if __name__ == "__main__":
    file_path = "sample_data.xlsx"  # Replace with actual file path
    try:
        data = load_data(file_path)
        generator = train_gan(data)
        new_patients = generate_synthetic_patients(generator, num_new_patients=32)
        
        # Append synthetic patients to original dataset
        full_data = np.vstack([data, new_patients])
        save_synthetic_data(full_data, "synthetic_patients.xlsx")
        print("Synthetic patient dataset saved successfully!")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found. Please check the file path and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
