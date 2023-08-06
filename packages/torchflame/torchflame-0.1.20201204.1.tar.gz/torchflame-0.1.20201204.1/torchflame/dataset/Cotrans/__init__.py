from .Compose import Compose
from .RandomCrop import RandomCrop, RandomResizedCrop
from .RandomFlip import RandomHorizontalFlip, RandomVerticalFlip
from .Resize import Resize
from .ToTensor import ToTensor

__all__ = ['Compose', 'RandomCrop', 'RandomHorizontalFlip', 'RandomResizedCrop', 'RandomVerticalFlip', 'Resize', 'ToTensor']

__doc__ = '''
    Cotrans is the modification of torchvision.transforms to process multi-images the same way.
    It only contains of transforms you may need to process multi-images and NEVER combine with torchvision.transforms.

    example:

    from torchflame import Cotrans
    from PIL import Image


    image1, image2 = Image.open('image1.png'), Image.open('image2.png')
    cotrans = Cotrans.Compose([
        Cotrans.RandomReszedCrop([480, 320]),
        Cotrans.RandomHorizontalFlip(),
        Cotrans.ToTensor()
    ])
    image1, image2 = cotrans([image1, image2])
'''
