import numpy as np
import tensorflow as tf
model_dir = "/Users/chentong/Documents/code/s-devs/dog-cat/model.h5"
def model():
    model = tf.keras.models.load_model(model_dir)
    # 加载pb模型
    # model = tf.keras.models.load_model("../weights/minist")

    model.summary()
    return model
