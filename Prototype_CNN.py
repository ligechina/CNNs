from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

#Imports

import numpy as np
import tensorflow as tf

from tensorflow.contrib import learn
from tensorflow.contrib.learn.python.learn.estimators import model_fn as model_fn_lib

tf.logging.set_verbosity(tf.logging.INFO)

# Our application logic will be added here

if __name__ == "__main__":
    tf.app.run()

def cnn_model_fn(features, labels, mode):
    """Model function for CNN."""
    # Input Layer
    input_layer = tf.reshape(features,[-1,28,28,1])

    #Convolutional Layer #1
    conv1 = tf.layers.conv2d(inputs=input_layer,
                             filters=32,
                             kernel_size=[5,5],
                             padding="same",
                             activation=tf.nn.relu)

    #Pooling Layer #1
    pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[2,2], strides=2)

    #Convolutional Layer #2 and Pooling Layer #2
    conv2 = tf.layers.conv2d(inputs=pool1,
                             filters=64,
                             kernel_size=[5, 5],
                             padding="same",
                             activation=tf.nn.relu)

    # Pooling Layer #2
    pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size = [2, 2], strides=2)

    #Dense Layer
    pool2_flat = tf.reshape(pool2,[-1,7*7*64])
    dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
    dropout = tf.layers.dropout(inputs=dense, rate=0.4, training=mode == learn.ModeKeys.TRAIN)

    #Logits Layer
    logits = tf.layers.dense(inputs=dropout, units=10)

    loss = None
    train_op = None

    #Calculate Loss(for both TRAIN and EVAL models)
    if mode!= learn.ModeKeys.INFER:
        onehot_labels = tf.one_hot(indices=tf.cast(labels,tf.int32),depth=10)
        loss = tf.losses.softmax_cross_entropy(onehot_labels=onehot_labels,logits=logits)

    #Configure the Training Op(for TRAIN mode)
    if mode == learn.ModeKeys.TRAIN:
        train_op = tf.contrib.layers.optimize_loss(loss=loss,
                                                   global_step=tf.contrib.framework.get_globel_step(),
                                                   learning_rate=0.001,
                                                   optimizer="SGD")

    #Generate Predictions
    Predictions = {
        "classes":tf.arg_max(input=logits,axis=1),
        "probabilites": tf.nn.softmax(logits,name="softmax_tensor")
    }

    #Return a ModelFnOps Object
    return model_fn_lib.ModelFnOps(mode=mode,predictions = Predictions, loss = loss, train_op = train_op)
