import tensorflow as tf

import numpy as np
from dl_utils import *

gpus = tf.config.experimental.list_physical_devices('GPU')
print("gpus: ", gpus)
if gpus:
    try:
        tf.config.experimental.set_virtual_device_configuration(
            gpus[np.random.randint(0, len(gpus))],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=512)])
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)


class infer():
    def __init__(self):
        self.model = tf.keras.models.load_model("./getFuncFromGraph.h5")

      
    def infer_and_estimation(self, img, cameraInfo, prevInfo):
        img = parse_image(img, shape=(224,224))[np.newaxis, :]
        result = self.model.predict(img)
        landmarks = result[0][0]
        rendervis = result[1][0]
        renderOnOff = result[2][0]
        
        return landmarks, rendervis, renderOnOff