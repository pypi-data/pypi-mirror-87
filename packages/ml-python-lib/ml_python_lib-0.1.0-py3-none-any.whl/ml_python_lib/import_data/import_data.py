import tensorflow as tf
from typing import Tuple, List
import os
from dynaconf import settings

# configuration
TRAIN_SPLIT_RATE = settings.TRAIN_SPLIT_RATE
VAL_SPLIT_RATE = settings.VAL_SPLIT_RATE

# constants
TEST_SPLIT_RATE = 1 - TRAIN_SPLIT_RATE - VAL_SPLIT_RATE
FILES_DS = Tuple[List[str], int,
                 Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]]


def download_data(ds_name: str, ds_origin: str) -> FILES_DS:
    subdir = 'data'
    flname = ds_name.split('.')[0]
    data_dir = os.path.join(subdir, flname)
    tf.keras.utils.get_file(
        ds_name,
        origin='/'.join([ds_origin, ds_name]),
        extract=True,
        cache_dir='.', cache_subdir='data'
    )
    filenames = tf.io.gfile.glob(os.path.join(data_dir, '*', '*'))
    filenames = tf.random.shuffle(filenames)
    num_samples = len(filenames)
    num_train = int(TRAIN_SPLIT_RATE * num_samples)
    num_val = int(VAL_SPLIT_RATE * num_samples)
    train_files = filenames[:num_train]
    val_files = filenames[num_train:num_train + num_val]
    test_files = filenames[num_train + num_val:]
    ds_class = [dir_name
                for dir_name in tf.io.gfile.listdir(data_dir)
                if dir_name != "README.md"]
    return (ds_class, num_train,
            (tf.data.Dataset.from_tensor_slices(train_files),
             tf.data.Dataset.from_tensor_slices(val_files),
             tf.data.Dataset.from_tensor_slices(test_files))
            )
