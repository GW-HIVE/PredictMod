import tensorflow as tf
import glob
#import imageio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import PIL
from tensorflow.keras import layers
import time
from IPython import display
tf.__version__

#Reading data and label of formatted patient data, as well as keeping track of variable headers from original data

data = pd.read_excel('data.xlsx')
labels = pd.read_excel('label.xlsx')
headers = pd.read_excel('var_list_.xlsx')
data = data.iloc[:, 1:] #removed first column because it was all NAN will FIX this later
row_select = [1, 2, 4, 5, 6, 7]
global variable_headers
variable_headers = headers.iloc[row_select, 2]

# remove any NAN rows in data

train_images = np.zeros((1,data.shape[1]))
train_labels = np.zeros((1,1))
isnan = data.isna().any(axis=1)
counter = 0
for i in isnan:
  if i == False:
    patient_to_append = data.iloc[counter, :];label_to_append = labels.iloc[counter]
    numpy_array = patient_to_append.to_numpy(); numpy_label = label_to_append.to_numpy();
    train_images = np.insert(train_images, -1, numpy_array, axis=0);
    train_labels = np.insert(train_labels, -1, numpy_label, axis=0);
  counter += 1
train_images = train_images[:-1]
train_labels = train_labels[:-1]
train_labels = train_labels.flatten()

# Normalize data, and keep track of data to un normalize it later as well

global max_store 
max_store = np.zeros((1,1))
for i in range(0,train_images.shape[1]):
  col_max = np.max(train_images[:,i])
  max_store = np.insert(max_store, -1, col_max, axis = 0)
for j in range(0,max_store.shape[0] - 1):
  train_images[:,j] = train_images[:,j]/max_store[j]
max_store = np.delete(max_store, -1)

#Convert to tf class for GAN training 
BATCH_SIZE = len(train_images)
train_images = train_images.reshape((-1, 1, 6, 1)) #6 is because of 6 variables, make this dynamic later
train_dataset = tf.data.Dataset.from_tensor_slices(train_images) #fix to include buffer size, not sure if it's needed but whatever
#FUNCTIONS FOR GENERATOR, DISCRIMINATOR, AND TRAINING PROCESS
def make_generator_model():
    model = tf.keras.Sequential()

    model.add(layers.Dense(3 * 11 * 64, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Reshape((3, 11, 64)))
    assert model.output_shape == (None, 3, 11, 64)

    model.add(layers.Conv2DTranspose(32, kernel_size=(3, 3), strides=(1, 1), padding='same', use_bias=False))
    assert model.output_shape == (None, 3, 11, 32)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())


    model.add(layers.Conv2D(1, kernel_size=(3, 3), strides=(3, 2), padding='same', use_bias=False, activation='tanh'))
    #assert model.output_shape == (None, 1, 6, 1)

    return model

generator = make_generator_model()

def make_discriminator_model():
    model = tf.keras.Sequential()

    # Assuming you want to process each time step independently
    model.add(layers.Conv1D(32, 3, strides=1, padding='same', input_shape=(1,6,1)))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    # Downsample
    model.add(layers.Conv1D(16, 3, strides=2, padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    # Flatten and output
    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model

discriminator = make_discriminator_model()

cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    total_loss = real_loss + fake_loss
    return total_loss

def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)

generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer,
                                 discriminator_optimizer=discriminator_optimizer,
                                 generator=generator,
                                 discriminator=discriminator)

EPOCHS = 45
noise_dim = 100
num_examples_to_generate = 1000

# You will reuse this seed overtime (so it's easier)
# to visualize progress in the animated GIF)
current_time = int(time.time())
tf.random.set_seed(current_time)
seed = tf.random.normal([num_examples_to_generate, noise_dim])# so change this later to avoid repeat data generation

# Notice the use of `tf.function`
# This annotation causes the function to be "compiled".
@tf.function
def train_step(images):
    noise = tf.random.normal([BATCH_SIZE, noise_dim])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
      generated_images = generator(noise, training=True)
      images = tf.reshape(images, (-1, 1, 6, 1))
      real_output = discriminator(images, training=True)
      fake_output = discriminator(generated_images, training=True)

      gen_loss = generator_loss(fake_output)
      disc_loss = discriminator_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

def generate_and_save_images(model, epoch, test_input,):
  # Notice `training` is set to False.
  # This is so all layers run in inference mode (batchnorm).
  predictions = model(test_input, training=False)
  np_pred = predictions.numpy()
  reshaped_predictions = np.squeeze(np_pred, axis=(1, 3))
  print(reshaped_predictions.shape)
  for j in range(0,max_store.shape[0]):
    reshaped_predictions[:,j] = reshaped_predictions[:,j]*max_store[j]
  df = pd.DataFrame(reshaped_predictions, columns=variable_headers)
  #fig = plt.figure(figsize=(4, 4))
  #for i in range(predictions.shape[0]):
      #plt.subplot(4, 4, i+1)
      #plt.imshow(predictions[i, :, :, 0] * 127.5 + 127.5, cmap='gray') #Alter this to add the max from each column variable
      #plt.axis('off')
  df.to_excel('EHR_at_epoch_{:04d}.xlsx'.format(epoch))
  #plt.savefig('image_at_epoch_{:04d}.png'.format(epoch))
  #plt.show()

def train(dataset, epochs):
    for epoch in range(epochs):
        start = time.time()

        for image_batch in dataset:
            train_step(image_batch)

        # Produce images for the GIF as you go
        display.clear_output(wait=True)
        generate_and_save_images(generator,
                                epoch + 1,
                                seed)

        # Save the model every 15 epochs
        if (epoch + 1) % 15 == 0:
            checkpoint.save(file_prefix = checkpoint_prefix)

        print ('Time for epoch {} is {} sec'.format(epoch + 1, time.time()-start))

    # Generate after the final epoch
    display.clear_output(wait=True)
    generate_and_save_images(generator,
                            epochs,
                            seed)
  
regular_dataset = train_dataset.batch(256)  # Specify the batch size

# Get the element_spec
element_spec = regular_dataset.element_spec

# Print the element_spec
print(element_spec)

# If the element_spec is a TensorShape, you can get the dimensions
if isinstance(element_spec, tf.TensorShape):
    print("Shape of the dataset:", element_spec.as_list())

train(train_dataset, EPOCHS)
checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))