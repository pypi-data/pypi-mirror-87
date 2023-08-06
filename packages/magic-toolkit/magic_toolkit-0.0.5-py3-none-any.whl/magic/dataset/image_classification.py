import glob
import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from .dataset import Dataset
import xml.etree.ElementTree as ET

class SampleForClf:
    """sample for image classification, returned by dataset"""

    def __init__(self, image=None, label=None):
        self.image = image
        self.label = label

class KittiDataset(Dataset):
    """
    1. parse kitti dataset
    2. kitti format:
         train
          -- image
          -- label
         test
          -- image
          -- label
    """

    def __init__(self, dataset_path, transform, npz_cached=False):
        self.dataset_path = dataset_path
        self.transform = transform
        self.npz_cached = npz_cached
        assert os.path.exists(self.dataset_path)
        self.img_dir = os.path.join(dataset_path, "image")
        self.label_dir = os.path.join(dataset_path, "label")
        self.npz_dir = None
        assert os.path.exists(self.img_dir)
        assert os.path.exists(self.label_dir)
        if self.npz_cached:
            self.npz_dir = os.path.join(dataset_path, "npz")
            os.makedirs(self.npz_dir, exist_ok=True)  # do noting if exists
        # get all paths of image in directory
        self.img_paths = []
        img_suffix = ["*.jpg", "*.png"]
        for fmt in img_suffix:
            ret = glob.glob(os.path.join(self.img_dir, fmt))
            self.img_paths.extend(ret)

    def __getitem__(self, index):
        sample = self.get_sample(index)
        # preprocess, data argument
        if self.transform:
            data = self.transform(sample)
            assert isinstance(data, dict), "transform must return dict"
            assert len(data) > 0
            return data
        else:
            return sample

    def __len__(self):
        return len(self.img_paths)

    def get_sample(self, index):
        img_path = self.img_paths[index]
        img_name = ".".join(os.path.basename(img_path).split(".")[:-1])
        if self.npz_cached:
            # pre-load from npz
            npz_path = os.path.join(self.npz_dir, img_name + ".npz")
            if os.path.exists(npz_path):
                cached = np.load(npz_path)
                return SampleForClf(cached['image'], cached['label'])
        # get ground truth from txt
        txt_path = os.path.join(self.label_dir, img_name + ".txt")
        assert os.path.exists(txt_path), "label error: {} does not exist".format(txt_path)
        with open(txt_path) as f:
            lines = [l.strip().split() for l in f.readlines()]

        sample = SampleForClf()
        """catch exception to prevent training from terminating"""
        try:
            sample.image = cv2.imread(img_path)
            sample.label = np.array(lines, dtype=np.str)
            assert isinstance(sample.label, np.ndarray), print(lines)
        except Exception as err:
            print("error sample:", txt_path)
            print("error info:", err)
            print("label:", lines)
            print("-" * 100)
        if self.npz_cached:
            npz_path = os.path.join(self.npz_dir, img_name + ".npz")
            cached = {"image": sample.image, "label": sample.label}
            np.savez(npz_path, **cached)
        return sample

    def split(self, test_size=0.3, shuffle=True):
        """return train_set, test_set"""
        train_set = KittiDataset(self.dataset_path, self.transform, self.npz_cached)
        test_set = KittiDataset(self.dataset_path, self.transform, self.npz_cached)
        train_x, test_x = train_test_split(self.img_paths, test_size=test_size, random_state=100, shuffle=shuffle)
        train_set.img_paths = train_x
        test_set.img_paths = test_x
        print("split dataset >>> train_size={}, test_size={}".format(len(train_set), len(test_set)))
        return train_set, test_set

class XMLDataset(Dataset):
    """
    1. parse xml dataset
    2. xml format:
         train
          -- image
          -- label
         test
          -- image
          -- label
    3. pass sample = {"image": numpy, "label": numpy} to Transformer
    """

    def __init__(self, dataset_path, transform,
                 xmlKey={"object": "object",
                         "class": "name",
                         "bbox": "bndbox",
                         "xmin": "xmin",
                         "ymin": "ymin",
                         "xmax": "xmax",
                         "ymax": "ymax"},
                 npz_cached=False):
        self.xmlKey = xmlKey
        self.dataset_path = dataset_path
        self.transform = transform
        self.npz_cached = npz_cached
        assert os.path.exists(self.dataset_path)
        self.img_dir = os.path.join(dataset_path, "image")
        self.label_dir = os.path.join(dataset_path, "label")
        self.npz_dir = None
        assert os.path.exists(self.img_dir)
        assert os.path.exists(self.label_dir)
        if self.npz_cached:
            self.npz_dir = os.path.join(dataset_path, "npz")
            os.makedirs(self.npz_dir, exist_ok=True)  # do noting if exists
        # get all paths of image in directory
        self.img_paths = []
        img_suffix = ["*.jpg", "*.png"]
        for fmt in img_suffix:
            ret = glob.glob(os.path.join(self.img_dir, fmt))
            self.img_paths.extend(ret)

    def __getitem__(self, index):
        sample = self.get_sample(index)
        # preprocess, data argument
        if self.transform:
            data = self.transform(sample)
            assert isinstance(data, dict), "transform must return dict"
            assert len(data) > 0
            return data
        else:
            return sample

    def __len__(self):
        return len(self.img_paths)

    def get_sample(self, index):
        img_path = self.img_paths[index]
        img_name = ".".join(os.path.basename(img_path).split(".")[:-1])
        if self.npz_cached:
            # pre-load from npz
            npz_path = os.path.join(self.npz_dir, img_name + ".npz")
            if os.path.exists(npz_path):
                cached = np.load(npz_path)
                return SampleForClf(cached['image'], cached['label'])
        # get ground truth from txt
        xml_path = os.path.join(self.label_dir, img_name + ".xml")
        assert os.path.exists(xml_path), "label error: {} does not exist".format(xml_path)
        tree = ET.parse(xml_path)
        root = tree.getroot()
        lines = list()
        for obj in root.iter(self.xmlKey["object"]):
            cls = obj.find(self.xmlKey["class"]).text
            bbox = obj.find(self.xmlKey["bbox"])
            xmin = bbox.find(self.xmlKey["xmin"]).text
            ymin = bbox.find(self.xmlKey["ymin"]).text
            xmax = bbox.find(self.xmlKey["xmax"]).text
            ymax = bbox.find(self.xmlKey["ymax"]).text
            lines.append([cls, xmin, ymin, xmax, ymax])

        sample = SampleForClf()
        """catch exception to prevent training from terminating"""
        try:
            sample.image = cv2.imread(img_path)
            sample.label = np.array(lines, dtype=np.str)
            assert isinstance(sample.label, np.ndarray), print(lines)
        except Exception as err:
            print("error sample:", xml_path)
            print("error info:", err)
            print("label:", lines)
            print("-" * 100)
        if self.npz_cached:
            npz_path = os.path.join(self.npz_dir, img_name + ".npz")
            cached = {"image": sample.image, "label": sample.label}
            np.savez(npz_path, **cached)
        return sample

    def split(self, test_size=0.3, shuffle=True):
        """return train_set, test_set"""
        train_set = XMLDataset(self.dataset_path, self.transform, self.xmlKey, self.npz_cached)
        test_set = XMLDataset(self.dataset_path, self.transform, self.xmlKey, self.npz_cached)
        train_x, test_x = train_test_split(self.img_paths, test_size=test_size, random_state=100, shuffle=shuffle)
        train_set.img_paths = train_x
        test_set.img_paths = test_x
        print("split dataset >>> train_size={}, test_size={}".format(len(train_set), len(test_set)))
        return train_set, test_set