from xml.dom import VALIDATION_ERR
import numpy as np
import pandas as pd 
from keras.preprocessing.image import ImageDataGenerator, load_img
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import random
import os
import mode
def strengthen():
    FAST_RUN = False
    IMAGE_WIDTH=128
    IMAGE_HEIGHT=128
    IMAGE_SIZE=(IMAGE_WIDTH, IMAGE_HEIGHT)
    IMAGE_CHANNELS=3
    # TODO
    # TRAIN_PATH = os.environ.get("TRAIN_PATH")
    # VALIDATION_PATH = os.environ.get("VALIDATION_PATH")
    # WEIGHT_PATH = os.environ.get("WEIGHT_PATH")
    TRAIN_PATH = "/mnt/python3/strength"
    VALIDATION_PATH = "/mnt/python3/validate"
    WEIGHT_PATH = "/mnt/python3/dog-cat-model/model.h5"
    filenames = os.listdir(TRAIN_PATH)
    n = len(filenames)
    # 小于100个则不要训练
    if(n < 100):
        return

    categories = []
    for filename in filenames:
        category = filename.split('.')[0]
        if category == 'dog':
            categories.append(1)
        else:
            categories.append(0)

    df = pd.DataFrame({
        'filename': filenames,
        'category': categories
    })

    model = mode.model()

    from keras.callbacks import EarlyStopping, ReduceLROnPlateau
    earlystop = EarlyStopping(patience=10)
    learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy', 
                                                patience=5, 
                                                verbose=1, 
                                                factor=0.5, 
                                                min_lr=0.00001)
    callbacks = [earlystop, learning_rate_reduction]


    ################# prepare data
    df["category"] = df["category"].replace({0: 'cat', 1: 'dog'}) 
    # train_df, validate_df = train_test_split(df, test_size=0.20, random_state=42)
    train_df = df
    train_df = train_df.reset_index(drop=True)


    v_filenames = os.listdir(VALIDATION_PATH)
    v_categories = []
    for filename in v_filenames:
        category = filename.split('.')[0]
        if category == 'dog':
            v_categories.append(1)
        else:
            v_categories.append(0)

    validate_df = pd.DataFrame({
        'filename': v_filenames,
        'category': v_categories
    }).sample(1000)
    validate_df = validate_df.reset_index(drop=True)
    validate_df["category"] = validate_df["category"].replace({0: 'cat', 1: 'dog'}) 
    ################# prepare data

    total_train = train_df.shape[0]
    total_validate = validate_df.shape[0]
    batch_size=15

    train_datagen = ImageDataGenerator(
        rotation_range=15,
        rescale=1./255,
        shear_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        width_shift_range=0.1,
        height_shift_range=0.1
    )

    train_generator = train_datagen.flow_from_dataframe(
        train_df, 
        TRAIN_PATH, 
        x_col='filename',
        y_col='category',
        target_size=IMAGE_SIZE,
        class_mode='categorical',
        batch_size=batch_size
    )

    validation_datagen = ImageDataGenerator(rescale=1./255)
    validation_generator = validation_datagen.flow_from_dataframe(
        validate_df, 
        VALIDATION_PATH, 
        x_col='filename',
        y_col='category',
        target_size=IMAGE_SIZE,
        class_mode='categorical',
        batch_size=batch_size
    )

    epochs=3 if FAST_RUN else 50
    model.load_weights(WEIGHT_PATH)

    history = model.fit_generator(
        train_generator, 
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=total_validate//batch_size,
        steps_per_epoch=total_train//batch_size,
        callbacks=callbacks
    )
    model.save_weights(WEIGHT_PATH)
