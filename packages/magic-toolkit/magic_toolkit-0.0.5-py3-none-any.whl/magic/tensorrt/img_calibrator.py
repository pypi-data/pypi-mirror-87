import glob
import random
import os
import cv2
import tensorrt as trt
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit  # initialize cuda


class ImgEntropyCalibrator(trt.IInt8EntropyCalibrator2):
    def __init__(self, imageCollectPath, batch_size, img_shape, n_random_samples, preprocess_fn,
                 cache_file='calibration_cache.bin'):
        """Entropy calibration for int8 calibration
        :param imageCollectPath: root directory of train dataset
        :param batch_size: equal to max_batch_size of engine
        :param img_shape: img_shape of tensorrt input
        :param n_random_samples: randomly sample without replacement from dataset
        :param preprocess_fn: process image data before taken into tensorrt
        :param cache_file:
        """
        super(ImgEntropyCalibrator, self).__init__()

        calibration_files = glob.glob(imageCollectPath + "/**/*.jpg", recursive=True)
        self.batch_size = batch_size
        self.preprocess_fn = preprocess_fn
        assert len(img_shape) == 3
        self.calibration_data = np.zeros((batch_size, img_shape[0], img_shape[1], img_shape[2]), dtype=np.float32)

        random.shuffle(calibration_files)

        n_random_samples = min(n_random_samples, len(calibration_files))
        self.samples = random.sample(calibration_files, n_random_samples)
        self.batch = 0

        self.cache_file = cache_file
        self.device_input = cuda.mem_alloc(self.calibration_data.nbytes)  # mem_alloc for cuda input

    def get_batch_size(self):
        return self.batch_size

    def get_batch(self, names, p_str=None):

        files_for_batch = self.samples[self.batch_size * self.batch: self.batch_size * (self.batch + 1)]
        if not files_for_batch:
            return None

        for i, path in enumerate(files_for_batch):
            print("[DataLoader] loading ", path)
            img = cv2.imread(path)
            self.calibration_data[i] = self.preprocess_fn(img)
        self.batch += 1
        print("[DataLoader] remaining:{}/{} ".format(self.batch * self.batch_size, len(self.samples)))

        cuda.memcpy_htod(self.device_input, self.calibration_data)
        return [int(self.device_input)]  # return device_input pointer

    def read_calibration_cache(self, *args, **kwargs):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                print("reading calibration_cache for calibration ")
                return f.read()

    def write_calibration_cache(self, cache):
        with open(self.cache_file, "wb") as f:
            f.write(cache)
