import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.mixed_precision import set_global_policy
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
print("Importing Modules Successfully")

# # Enable mixed precision for faster training on GPU
set_global_policy('mixed_float16')

# Check GPU availability
print("Available GPUs:", tf.config.list_physical_devices('GPU'))

# Define parameters
IMG_SIZE = (229, 317) # Assuming your image size is 203x307
SEQUENCE_LENGTH = 3 # Adjust as needed (number of past frames to use)

def load_and_preprocess_data(data_dir):
images = []
for filename in sorted(os.listdir(data_dir)):
if filename.endswith(".png"):
img = cv2.imread(os.path.join(data_dir, filename), cv2.IMREAD_GRAYSCALE)
img = img / 255.0 # Normalize to [0, 1]
images.append(img)
return np.array(images)

def create_sequences(images, seq_length):
X, y = [], []
for i in range(len(images) - seq_length):
X.append(images[i:i + seq_length])
y.append(images[i + seq_length])
return np.array(X), np.array(y)

def load_all_places_data(base_dir, seq_length):
X_all, y_all = [], []
for place_dir in sorted(os.listdir(base_dir)):
full_path = os.path.join(base_dir, place_dir)
if os.path.isdir(full_path):
print(f"Loading data from: {full_path}")
images = load_and_preprocess_data(full_path)
X, y = create_sequences(images, seq_length)
if len(X) > 0:
X_all.append(X)
y_all.append(y)
return np.concatenate(X_all), np.concatenate(y_all)

# Set path to parent directory containing place-wise subfolders
base_data_dir = "/kaggle/input"

# Load all sequences
X, y = load_all_places_data(base_data_dir, SEQUENCE_LENGTH)

# Expand dimensions
X = np.expand_dims(X, axis=-1)
y = np.expand_dims(y, axis=-1)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

# Create TensorFlow datasets
train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(16)
test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(16)

# --- 2. Model Architecture ---
model = models.Sequential([
layers.ConvLSTM2D(32, (3, 3), activation='relu', padding='same', return_sequences=False, input_shape=(SEQUENCE_LENGTH, IMG_SIZE[0], IMG_SIZE[1], 1)),
layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
layers.Conv2D(1, (3, 3), activation='linear', padding='same', dtype=tf.float32) # Linear activation for regression
])
print("Model created successfully!")

# --- 3. Compile and Train Model ---
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae']) # Use MSE for grayscale values
print("Model compiled successfully!")

model.fit(train_dataset, epochs=100, validation_data=test_dataset)
print("Model trained successfully!")

# --- 4. Predict Future Grayscale Image ---
future_input = X[-1:] # Last known sequence
predicted_lulc = model.predict(future_input)[0] # shape: (H, W, 1)

# Remove extra dimension
predicted_lulc = np.squeeze(predicted_lulc) # shape: (H, W)

# Optional: Scale values to 0–255 for saving/viewing as image
predicted_lulc = np.clip(predicted_lulc, 0, 1) # Ensure values stay in [0, 1]
predicted_lulc = (predicted_lulc * 255).astype(np.uint8)

# Save predicted LULC image
cv2.imwrite('predicted_LULC_2023.png', predicted_lulc)
print("Predicted LULC image saved successfully!")

# Display the predicted image
plt.imshow(predicted_lulc, cmap='gray')
plt.show()

# --- 5. Recursive Multi-Year Prediction (10 Years) ---
future_steps = 10
predicted_images = []

# Start with the last known input sequence
current_sequence = X[-1] # shape: (SEQUENCE_LENGTH, H, W, 1)

for year in range(future_steps):
# Add batch dimension
input_seq = np.expand_dims(current_sequence, axis=0)

# Predict next image
predicted_image = model.predict(input_seq)[0] # shape: (H, W, 1)
predicted_image = np.clip(predicted_image, 0, 1) # Ensure values stay in range

# Save prediction
predicted_images.append(predicted_image)

# Update sequence: remove oldest, append new prediction
predicted_image_expanded = np.expand_dims(predicted_image, axis=0) # shape: (1, H, W, 1)
current_sequence = np.concatenate([current_sequence[1:], predicted_image_expanded], axis=0)

# --- 6. Save Predicted Images ---
for idx, image in enumerate(predicted_images, start=1):
image_uint8 = (np.squeeze(image) * 255).astype(np.uint8)
filename = f'_{idx}.png'
cv2.imwrite(filename, image_uint8)
print(f"Saved: {filename}")

# Optional: Visualize
plt.figure()
plt.imshow(image_uint8, cmap='gray')
plt.title(f'Year +{idx}')
plt.axis('off')
plt.show()