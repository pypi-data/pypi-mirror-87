import torchvision.transforms.functional as F
from functools import partial
from PIL import Image


class Resize(object):
    """Resize the input PIL Images to the given size.

    Args:
        size (sequence or int): Desired output size. If size is a sequence like
            (h, w), output size will be matched to this. If size is an int,
            smaller edge of the image will be matched to this number.
            i.e, if height > width, then image will be rescaled to
            (size * height / width, size)
        interpolation (int, optional): Desired interpolation. Default is
            ``PIL.Image.BILINEAR``
    """

    def __init__(self, size, interpolation=Image.BILINEAR):
        assert isinstance(size, int) or (isinstance(size, (list, tuple)) and len(size) == 2)
        self.size = size
        self.interpolation = interpolation

    def __call__(self, imgs):
        """
        Args:
            imgs (PIL Image): Images to be scaled.

        Returns:
            PIL Image: Rescaled image.
        """
        resize = partial(F.resize(size=self.size, interpolation=self.interpolation))
        if not isinstance(imgs, (list, tuple)):
            return resize(imgs)
        return list(map(resize, imgs))

    def __repr__(self):
        return self.__class__.__name__ + "(size={0})".format(self.size)
