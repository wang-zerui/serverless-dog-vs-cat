from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tensorflow as tf
from skimage import io, transform, color
from keras.preprocessing.image import ImageDataGenerator, load_img
import mode
import pandas as pd
import numpy as np

_NUM_CLASSES = 2
image_size = [128, 128]
os.environ['TF_ENABLE_WINOGRAD_NONFUSED'] = '1'
model = mode.model()

def predictInputFn(image_path):
    image = transform.resize(color.rgb2gray(io.imread(image_path)), [128, 128]) - 0.5
    images = tf.image.convert_image_dtype(image, dtype=tf.float32)
    dataset = tf.data.Dataset.from_tensors((images,))
    return dataset.batch(1).make_one_shot_iterator().get_next(), None


def predict(image_path):
    print("Predicting ", image_path)
    test_filenames = [image_path]
    test_df = pd.DataFrame({
        'filename': test_filenames
    })
    nb_samples = test_df.shape[0]
    test_gen = ImageDataGenerator(rescale=1./255)
    batch_size = 15
    test_generator = test_gen.flow_from_dataframe(
        test_df, 
        "./", 
        x_col='filename',
        y_col=None,
        class_mode=None,
        target_size=[128, 128],
        batch_size=batch_size,
        shuffle=False
    )
    predict = model.predict(test_generator, steps=np.ceil(nb_samples/batch_size))
    return {"dog": str(predict[0][1]), "cat": str(predict[0][0])}


if __name__ == '__main__':
    image_files = "/Users/chentong/Documents/code/s-devs/dog-cat/1.jpeg"
    print(predict(image_files))