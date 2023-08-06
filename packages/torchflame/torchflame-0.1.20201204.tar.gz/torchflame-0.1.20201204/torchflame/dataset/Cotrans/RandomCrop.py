import random
import torch
import torchvision
import torchvision.transforms.functional as F
import numbers
import numpy as np
from PIL import Image
import math

class RandomCrop(object):
    def __init__(self, size, padding=0):
        if isinstance(size, numbers.Number):
            self.size = (int(size), int(size))
        else:
            self.size = size
        self.padding = padding

    @staticmethod
    def get_params(img, output_size):
        w, h = img.size
        th, tw = output_size
        if w == tw and h == th:
            return 0, 0, h, w

        i = random.randint(0, h - th)
        j = random.randint(0, w - tw)
        return i, j, th, tw

    def __call__(self, imgs):
        i, j, h, w = self.get_params(imgs[0], self.size)

        def crop(img):
            if isinstance(img, torch.Tensor):
                return torchvision.transforms.ToTensor()(crop(torchvision.transforms.ToPILImage()(img)))
            if isinstance(img, np.ndarray):
                return np.asarray(crop(Image.fromarray(img.astype(np.uint8))))
            if self.padding > 0:
                img = F.pad(img, self.padding)
            return F.crop(img, i, j, h, w)

        if not isinstance(imgs, (list, tuple)):
            return crop(imgs)
        return list(map(crop, imgs))

    def __repr__(self):
        return self.__class__.__name__ + f"(size={self.size})"

class RandomResizedCrop(object):
    def __init__(
            self,
            size,
            scale=(0.08, 1.0),
            ratio=(3.0 / 4.0, 4.0 / 3.0),
            interpolation=Image.BILINEAR,
    ):
        self.size = (size, size) if isinstance(size, int) else size
        self.interpolation = interpolation
        self.scale = scale
        self.ratio = ratio

    @staticmethod
    def get_params(img, scale, ratio):
        for attempt in range(10):
            area = img.size[0] * img.size[1]
            target_area = random.uniform(*scale) * area
            aspect_ratio = random.uniform(*ratio)

            w = int(round(math.sqrt(target_area * aspect_ratio)))
            h = int(round(math.sqrt(target_area / aspect_ratio)))

            if random.random() < 0.5:
                w, h = h, w

            if w <= img.size[0] and h <= img.size[1]:
                i = random.randint(0, img.size[1] - h)
                j = random.randint(0, img.size[0] - w)
                return i, j, h, w

        # Fallback
        w = min(img.size[0], img.size[1])
        i = (img.size[1] - w) // 2
        j = (img.size[0] - w) // 2
        return i, j, w, w

    def __call__(self, imgs):
        i, j, h, w = self.get_params(imgs[0], self.scale, self.ratio)

        def resized_crop(img):
            if isinstance(img, torch.Tensor):
                return torchvision.transforms.ToTensor()(resized_crop(torchvision.transforms.ToPILImage()(img)))
            if isinstance(img, np.ndarray):
                return np.asarray(resized_crop(Image.fromarray(img.astype(np.uint8))))
            return F.resized_crop(img, i, j, h, w, self.size, self.interpolation)

        return list(map(resized_crop, imgs)) if isinstance(imgs, (list, tuple)) else resized_crop(imgs)

    def __repr__(self):
        return self.__class__.__name__ + "(size={0})".format(self.size)
