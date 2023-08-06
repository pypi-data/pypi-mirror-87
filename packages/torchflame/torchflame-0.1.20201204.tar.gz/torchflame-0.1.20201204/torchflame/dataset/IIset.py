import numpy as np
from torch.utils.data import Dataset
import os
from PIL import Image
from .functional import pick
from torchvision import transforms
from . import Cotrans


class IIset(Dataset):
    '''
    A dataset whose both input and output is image.
    Transforms of images include RandomResizedCrop, RandomHorizontalFlip, ColorJitter and Normalize.
    '''
    def __init__(self,
                 raw_root: str,
                 label_root: str,
                 input_shape=(480, 320),
                 output_shape=(480, 320),
                 binarization=lambda x: 255 if x == 255 else 0,
                 oversample=(1, 0.1)):
        '''
        Parameters:
        raw_root: the input image folder address.
        label_root: the label image folder address. Image should have the same file name with its corresponding label.
        input_shape: the size of image your model needs. Both image and label will be random-resized-cropped to <input_shape>. 
        output_shape: the size of label your model outputs. If it's not equal to input_shape, then center-crop to <output_shape>
                      in the base of random-resized-cropped label.
        binarization: binarize every pixel of the label. Set <None> if not wanted else a Lambda expression.
        oversample: A tuple of 2 float numbers, e.g. [ratio, deviation]. Set <None> if not wanted.
                    The probability of one sample to be picked is expressed by average(label) * ratio + deviation
                    Deviation is better not zero. 
        '''
        self.raw_root, self.label_root = raw_root, label_root
        self.input_shape, self.output_shape = input_shape, output_shape
        self.namelist = os.listdir(raw_root)
        self.binarization, self.oversample = binarization, oversample
        self.oversample_ratio, self.oversample_deviation = oversample

    def __getitem__(self, i):
        name = self.namelist[i]
        imgIn = Image.open(os.path.join(self.raw_root, name))
        try:
            imgOut = Image.open(os.path.join(self.label_root, name))
        except FileNotFoundError:
            raise FileNotFoundError(f'Image<{name}> has no corresponding label')
        assert imgIn.size == imgOut.size

        if self.binarization:
            imgOut = Image.fromarray(np.vectorize(self.binarization)(np.asarray(imgOut)[..., 0]).astype(np.uint8))
        cotrans = Cotrans.Compose([Cotrans.RandomResizedCrop(self.input_shape), Cotrans.RandomHorizontalFlip()])
        while True:
            imgInCrop, imgOutCrop = cotrans([imgIn, imgOut])
            imgOutCrop = transforms.CenterCrop(self.output_shape)(imgOutCrop)
            if self.oversample and pick(np.average(imgOutCrop) / 255 * self.oversample_ratio, self.oversample_deviation):
                imgIn, imgOut = imgInCrop, imgOutCrop
                break
        imgIn, imgOut = Cotrans.ToTensor()([imgIn, imgOut])
        imgIn = transforms.Compose([transforms.ColorJitter(0.5, 0.5, 0.5, 0.5),
                                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])(imgIn)
        return imgIn.float(), imgOut.squeeze().long()

    def __len__(self):
        return len(self.namelist)


if __name__ == "__main__":
    pass
