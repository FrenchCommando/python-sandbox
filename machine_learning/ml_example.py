import logging
import tensorflow as tf
import matplotlib.pyplot as plt

logger = logging.getLogger("")
logger.setLevel(logging.INFO)

logging.info("Tensorflow version {}".format(tf.__version__))

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

nx_train = tf.keras.utils.normalize(x_train, axis=1)
nx_test = tf.keras.utils.normalize(x_test, axis=1)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(nx_train, y_train, epochs=3)

val_loss, val_acc = model.evaluate(nx_test, y_test)

for u in range(10):
    plt.imshow(x_test[u], cmap=plt.cm.binary)
    plt.show()
