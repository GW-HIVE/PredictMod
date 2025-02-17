### README: Generative Adversarial Network (GAN) for Synthetic Patient Data

## Overview
This project implements a **Generative Adversarial Network (GAN)** to generate synthetic patient data, increasing the dataset size while maintaining realistic distributions. The GAN consists of a **generator** and **discriminator**, trained using PyTorch.

## How It Works
The GAN is designed to take an existing dataset of patient features and expand it by generating synthetic patients with similar statistical properties. 

### Key Components
- **`load_data(file_path)`**: Loads patient data from an Excel file and normalizes it.
- **`Generator`**: A neural network that generates synthetic patient data from random noise.
- **`Discriminator`**: A neural network that distinguishes real from synthetic data.
- **`train_gan(data, latent_dim, epochs, batch_size, lr)`**: Trains the GAN using adversarial learning.
- **`generate_synthetic_patients(generator, num_new_patients, latent_dim)`**: Uses the trained generator to create new patient samples.
- **`save_synthetic_data(synthetic_data, file_path)`**: Saves the generated patient data to an Excel file.

## Mathematical Equations
The GAN is trained using **Binary Cross-Entropy Loss**:

### Discriminator Loss:
```math
L_D = - \frac{1}{m} \sum_{i=1}^{m} \left[ y_i \log D(x_i) + (1 - y_i) \log (1 - D(G(z_i))) \right]
```
Where:
- \( D(x) \) is the discriminator output for real data.
- \( D(G(z)) \) is the discriminator output for generated data.
- \( y \) is the true label (1 for real, 0 for fake).
- \( G(z) \) is the generator output for random noise \( z \).

### Generator Loss:
```math
L_G = - \frac{1}{m} \sum_{i=1}^{m} \log D(G(z_i))
```
The generator tries to maximize \( \log D(G(z)) \), meaning it aims to fool the discriminator.

## Requirements
Ensure you have the following dependencies installed:
```bash
pip install numpy pandas torch openpyxl
```

## Usage
1. **Prepare your dataset**: Ensure your patient data is in an Excel file (`your_data.xlsx`).
2. **Run the script**:
```bash
python GAN_generation.py
```
3. **Synthetic data output**: The generated dataset will be saved as `synthetic_patients.xlsx`.

## Expected Behavior
- The script should successfully train a GAN model.
- It will generate **32 new synthetic patients** by default.
- The output dataset should include the original and synthetic patients.
- If the file `your_data.xlsx` is missing, the script will throw a `FileNotFoundError`.

## Potential Errors & Fixes
- **Normalization issues** → The dataset should only contain numeric values.

## Author
This project was developed for **synthetic patient data augmentation** using deep learning. 

For questions, contact **mfmmazumder@gwu.edu**.

