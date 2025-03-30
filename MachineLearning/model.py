import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.mixed_precision import set_global_policy
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Enable mixed precision for faster training on GPU
set_global_policy('mixed_float16')

# Check GPU availability
print("Available GPUs:", tf.config.list_physical_devices('GPU'))

# Define parameters
IMG_SIZE = (203, 307)  # Assuming your image size is 203x307
SEQUENCE_LENGTH = 5  # Adjust as needed (number of past frames to use)

# --- 1. Data Loading and Preprocessing ---
def load_and_preprocess_data(data_dir):
    images = []
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".png"):
            img = cv2.imread(os.path.join(data_dir, filename), cv2.IMREAD_GRAYSCALE)
            img = img / 255.0  # Normalize to [0, 1]
            images.append(img)
    return np.array(images)

def create_sequences(images, seq_length):
    X, y = [], []
    for i in range(len(images) - seq_length):
        X.append(images[i:i + seq_length])
        y.append(images[i + seq_length])
    return np.array(X), np.array(y)

# Load your data (replace 'data_directory' with your actual path)
data_dir = "./"  
images = load_and_preprocess_data(data_dir)
X, y = create_sequences(images, SEQUENCE_LENGTH)

# Expand dimensions for ConvLSTM input
X = np.expand_dims(X, axis=-1)  
y = np.expand_dims(y, axis=-1)  

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Create TensorFlow datasets
train_dataset = tf.data.Dataset.from_tensor_slices((X_train, y_train)).batch(16)
test_dataset = tf.data.Dataset.from_tensor_slices((X_test, y_test)).batch(16)

# --- 2. Model Architecture ---
model = models.Sequential([
    layers.ConvLSTM2D(32, (3, 3), activation='relu', padding='same', return_sequences=False, input_shape=(SEQUENCE_LENGTH, IMG_SIZE[0], IMG_SIZE[1], 1)),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same', dtype=tf.float32)  # Ensure final layer outputs float32
])
print("Model created successfully!")

# --- 3. Compile and Train Model ---
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])  # Use binary_crossentropy
print("Model compiled successfully!")

model.fit(train_dataset, epochs=60, validation_data=test_dataset)  # Reduce epochs
print("Model trained successfully!")

# --- 4. Predict Future LULC ---
future_input = X[-1:]  # Last known sequence
predicted_lulc = model.predict(future_input)[0]

# Apply thresholding and squeeze
predicted_lulc = (predicted_lulc > 0.5).astype(np.uint8)
predicted_lulc = np.squeeze(predicted_lulc)

# Save predicted LULC image
cv2.imwrite('predicted_LULC_2023.png', predicted_lulc * 255)
print("Predicted LULC image saved successfully!")

# Display the predicted image
plt.imshow(predicted_lulc, cmap='gray')
plt.show()
