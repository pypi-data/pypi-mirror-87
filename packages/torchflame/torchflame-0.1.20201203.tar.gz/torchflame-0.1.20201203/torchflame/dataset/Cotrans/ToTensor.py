import torchvision.transforms.functional as F


class ToTensor(object):
    """Convert a ``PIL Image`` or ``numpy.ndarray`` to tensor.

    Converts a PIL Image or numpy.ndarray (H x W x C) in the range
    [0, 255] to a torch.FloatTensor of shape (C x H x W) in the range [0.0, 1.0].
    """

    def __call__(self, pics):
        """
        Args:
            pic (PIL Image or numpy.ndarray): Image to be converted to tensor.

        Returns:
            Tensor: Converted image.
        """
        if not isinstance(pics, (list, tuple)):
            return F.to_tensor(pics)
        return list(map(F.to_tensor, pics))

    def __repr__(self):
        return self.__class__.__name__ + "()"
