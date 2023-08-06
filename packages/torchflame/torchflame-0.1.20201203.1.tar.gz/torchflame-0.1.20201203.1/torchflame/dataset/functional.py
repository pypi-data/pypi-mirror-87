import random
import torch
from torch.utils.data.dataset import random_split
from torchvision.transforms import ToPILImage
import numpy as np
__ALL__ = ['pick', 'ratio_split', 'rev_trans']

__all__ = __ALL__ + ['__ALL__']


def pick(probability, base=0):
    compare = random.random()
    return True if probability + base > compare else False


def ratio_split(dataset, percentages):
    if round(sum(percentages), 3) != 1.0:
        raise ValueError(
            'Sum of input percentages({}) does not equal 1'.format(sum(percentages)))
    lenList = list(map(lambda x: int(x * len(dataset)), percentages))
    lenList[-1] = len(dataset) - sum(lenList[0:-1])
    return random_split(dataset, lenList)


def rev_trans(tensor, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]):
    mean = torch.FloatTensor(mean).view(3,1,1).expand(*tensor.shape)
    std = torch.FloatTensor(std).view(3,1,1).expand(*tensor.shape)
    return ToPILImage()(tensor * std + mean)

