import tensorflow as tf
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.25),
    layers.RandomZoom(0.25),
    layers.RandomTranslation(0.15, 0.15),
    layers.RandomContrast(0.25),
    layers.RandomBrightness(0.25),
])

# Dataset paths
train_dir = "dataset/train"
val_dir = "dataset/validation"

# Constants
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
AUTOTUNE = tf.data.AUTOTUNE

# Load training dataset
train_dataset = tf.keras.utils.image_dataset_from_directory(
    train_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True
)

# Load validation dataset
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    val_dir,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)
# Compute class weights
labels = np.concatenate([
    y.numpy() for _, y in train_dataset
])

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)

class_weights = dict(enumerate(class_weights))

print("Class Weights:", class_weights)
class_names = train_dataset.class_names
train_dataset = train_dataset.cache().prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.cache().prefetch(buffer_size=AUTOTUNE)

print("\nClasses Found:")
print(class_names)
print(len(class_names))
# Load MobileNetV2 pretrained model
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers
base_model.trainable = False

# Input Layer
inputs = tf.keras.Input(shape=(224, 224, 3))

# Data Augmentation
x = data_augmentation(inputs)

# Preprocessing for MobileNetV2
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

# Pass through MobileNetV2
x = base_model(x, training=False)

# Convert feature maps to a single vector
x = layers.GlobalAveragePooling2D()(x)

# Reduce overfitting
x = layers.Dropout(0.2)(x)

# Fully Connected Layer
x = layers.Dense(128, activation="relu")(x)

# Output Layer
# NOTE: dynamic now - was hardcoded to 3, which silently breaks once
# you add Pest/Bacteria (5 classes total).
outputs = layers.Dense(len(class_names), activation="softmax")(x)

# Final Model
model = tf.keras.Model(inputs, outputs)

# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)
model.summary()
# Train the model
EPOCHS = 15

checkpoint_cb = tf.keras.callbacks.ModelCheckpoint(
    "models/potato_disease_model_5class.keras",
    save_best_only=True,
    monitor="val_accuracy"
)

early_stop_cb = tf.keras.callbacks.EarlyStopping(
    monitor="val_accuracy",
    patience=4,
    restore_best_weights=True
)

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=[checkpoint_cb, early_stop_cb]
)

# Save the trained model
# NOTE: checkpoint_cb above already saves the BEST epoch during training.
# This explicit save is a safety net in case training stops early / crashes
# before the callback's last save, so you never end up with no model file
# (which was silently happening before - ModelCheckpoint(...) was being
# created but never passed to model.fit, and model.save() was never called).
model.save("models/potato_disease_model_5class_final.keras")
print("\nModel saved successfully to models/potato_disease_model_5class_final.keras")
print("Best checkpoint saved to models/potato_disease_model_5class.keras")