import torchvision.transforms.functional as F
from ..functional import pick


class RandomHorizontalFlip(object):
    def __call__(self, imgs):
        if not isinstance(imgs, (list, tuple)):
            return F.hflip(imgs) if pick(0.5) else imgs
        return list(map(F.hflip, imgs)) if pick(0.5) else imgs

    def __repr__(self):
        return self.__class__.__name__ + '()'


class RandomVerticalFlip(object):
    def __call__(self, imgs):
        if not isinstance(imgs, (list, tuple)):
            return F.vflip(imgs) if pick(0.5) else imgs
        return list(map(F.vflip, imgs)) if pick(0.5) else imgs

    def __repr__(self):
        return self.__class__.__name__ + '()'
