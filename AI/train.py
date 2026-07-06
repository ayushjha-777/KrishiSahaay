import tensorflow as tf
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras import layers

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.15),
    layers.RandomZoom(0.15),
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
outputs = layers.Dense(3, activation="softmax")(x)

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
EPOCHS = 10

history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=EPOCHS,
    class_weight=class_weights
)
# Save the trained model
ModelCheckpoint(
    save_best_only=True,
    monitor="val_accuracy"
)
print("\nModel saved successfully!")