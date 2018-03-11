from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""
Ein Cnn Model und die dazügehörigen Konvertierungsfunktion für das Klassifzieren der Notenhöhe.
"""

import tensorflow as tf
import numpy as np
import math

__author__  = "Bonifaz Stuhr"
__version__ = "0.0.0"
__status__ = "Production"

def predictionToNoteHightClassificationFn(predictions):
    """
    Wandelt den Output-Vector des Cnns in eine String für die interne Notenrepräsentation um.

    :param predictions tensor : Eine Output-Vector des Cnns.
    :return: string, string : Die Notenhöhe, der Step und die Octave der Note.
    """
    #Converting the prediction vector into one of the values in the following list:
    predictionStrings = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B']
    predictedSteps = []
    predictedOctaves = []
    for i in range(0, len(predictions)):
        propVec = predictions[i]["probabilities"]
        predictionIndex = np.argmax(propVec)
        predictedSteps.append(predictionStrings[predictionIndex])
        predictedOctaves.append(math.floor(predictionIndex / 7) + 4)

    return predictedSteps, predictedOctaves

def noteHightToInt(step, octave):
    """
    Wandelt den Input in einen im Kontext eindeutigen numerischen Wert für die One-Hot Kodierung um.

    :param step : string Der Step der Note (z.B. C)
    :param octave : string Die Octave der Note (z.B. 4)
    :return: int : Der Step und die Octave, in numerischer Repräsentation für die One-Hot Kodierung.
    """
    #Converting the values into a nummeric vector for onehot.
    hight = None;
    if step == 'C':
        hight = 1
    elif step == 'D':
        hight = 2
    elif step == 'E':
        hight = 3
    elif step == 'F':
        hight = 4
    elif step == 'G':
        hight = 5
    elif step == 'A':
        hight = 6
    elif step == 'B':
        hight = 7
    if int(octave) == 4:
        return hight - 1
    elif int(octave) == 5:
        return (hight + 7) - 1

def cnnNoteHightModel(features, labels, mode, params):
    """
    Model Funktion eines Cnns, welches die Layer, die Modi, und weiteres (z.B. Dropout) eines Cnns definiert.

    Dieses Cnn dient zur Klassifizerung der Notenhöhe

    :param features : tensor Enthält den Input, der zum Training, zur Klassifizierung oder zu Evaluation benutzt wird.
    :param labels : tensor Enthält die Lables zu den features
    :param mode : tensor Der Modus der Ausführung z.b. TRAIN, EVAL oder PREDICT.
    """
    # Input Layer
    # Reshape X to 4-D tensor: [batch_size, width, height, channels]
    # Note images are 28x96 pixels, and have one color channel
    input_layer = tf.reshape(features["x"], [-1, 28, 96, 1])

    # Convolutional Layer #1
    # Computes 32 features using a 5x5 filter with ReLU activation.
    # Padding is added to preserve width and height.
    # Input Tensor Shape: [batch_size, 28, 96, 1]
    # Output Tensor Shape: [batch_size, 28, 96, 32]
    conv1 = tf.layers.conv2d(
        inputs=input_layer,
        filters=32,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)

    # Pooling Layer #1
    # First max pooling layer with a 2x2 filter and stride of 2
    # Input Tensor Shape: [batch_size, 28, 96, 32]
    # Output Tensor Shape: [batch_size, 14, 48, 32]
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2, 2], strides=2)

    # Convolutional Layer #2
    # Computes 64 features using a 5x5 filter.
    # Padding is added to preserve width and height.
    # Input Tensor Shape: [batch_size, 14, 48, 32]
    # Output Tensor Shape: [batch_size, 14, 48, 64]
    conv2 = tf.layers.conv2d(
        inputs=pool1,
        filters=64,
        kernel_size=[5, 5],
        padding="same",
        activation=tf.nn.relu)

    # Pooling Layer #2
    # Second max pooling layer with a 2x2 filter and stride of 2
    # Input Tensor Shape: [batch_size, 14, 48, 64]
    # Output Tensor Shape: [batch_size, 7, 24, 64]
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[2, 2], strides=2)

    # Flatten tensor into a batch of vectors
    # Input Tensor Shape: [batch_size, 7, 24, 64]
    # Output Tensor Shape: [batch_size, 7 * 24 * 64]
    pool2_flat = tf.reshape(pool2, [-1, 7 * 24 * 64])

    # Dense Layer
    # Densely connected layer with 1024 neurons
    # Input Tensor Shape: [batch_size, 7 * 24 * 64]
    # Output Tensor Shape: [batch_size, 1024]
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)

    # Add dropout operation; 0.6 probability that element will be kept
    dropout = tf.layers.dropout(
        inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

    # Logits layer
    # Input Tensor Shape: [batch_size, 1024]
    # Output Tensor Shape: [batch_size, 14]
    logits = tf.layers.dense(inputs=dropout, units=14)

    predictions = {
        # Generate predictions (for PREDICT and EVAL mode)
        "classes": tf.argmax(input=logits, axis=1),
        # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
        # `logging_hook`.
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    # MODE PREDICT
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate Loss (for both TRAIN and EVAL modes)
    onehot_labels = tf.one_hot(indices=tf.cast(labels, tf.int32), depth=14)
    loss = tf.losses.softmax_cross_entropy(
        onehot_labels=onehot_labels, logits=logits)

    # MODE TRAIN
    # Configure the Training Op (for TRAIN mode)
    if mode == tf.estimator.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=params["learning_rate"])
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # MODE EVAL
    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"])}
    return tf.estimator.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)
