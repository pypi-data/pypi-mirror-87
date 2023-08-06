import numpy as np
from torch.utils.data import Dataset
import os
from PIL import Image
from .functional import pick
from torchvision import transforms
from . import Cotrans

class IIset(Dataset):
    def __init__(self, raw_root, label_root, input_shape=(480, 320), output_shape=(480, 320)):
        self.raw_root, self.label_root = raw_root, label_root
        self.input_shape, self.output_shape = input_shape, output_shape
        self.namelist = os.listdir(raw_root)

    def __getitem__(self, i):
        name = self.namelist[i]
        imgIn = Image.open(os.path.join(self.raw_root, name))
        try:
            imgOut = Image.open(os.path.join(self.label_root, name))
        except FileNotFoundError:
            raise FileNotFoundError(f'Image<{name}> has no corresponding label')
        assert imgIn.size == imgOut.size
        
        imgOut = Image.fromarray(np.vectorize(lambda x: 255 if x == 255 else 0)(np.asarray(imgOut)[..., 0]).astype(np.uint8))
        cotrans = Cotrans.Compose([
            Cotrans.RandomResizedCrop(self.input_shape),
            Cotrans.RandomHorizontalFlip()
        ])
        while True:
            imgInCrop, imgOutCrop = cotrans([imgIn, imgOut])
            imgOutCrop = transforms.CenterCrop(self.output_shape)(imgOutCrop)
            if pick(np.average(imgOutCrop) / 255, 0.1):
                imgIn, imgOut = imgInCrop, imgOutCrop
                break
        imgIn, imgOut = Cotrans.ToTensor()([imgIn, imgOut])
        imgIn = transforms.Compose([
            transforms.ColorJitter(0.5, 0.5, 0.5, 0.5),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])(imgIn)
        return imgIn.float(), imgOut.squeeze().long()
    

    def __len__(self):
        return len(self.namelist)


if __name__ == "__main__":
    pass
