from numpy import average
from torch import nn
import numpy as np
from array import array

__all__ = ['calIoU']

def calIoU(prediction, label):
    assert prediction.shape == label.shape
    prediction, label = nn.Flatten()(prediction), nn.Flatten()(label)
    res = []
    for i in range(label.shape[0]):
        count = array('i', [0, 0, 0, 0])
        P, L = np.array(prediction[i].cpu()), np.array(label[i].cpu())
        for j in range(len(P)):
            datatype = P[j] * 2 + L[j]
            try:
                count[datatype] += 1
            except IndexError:
                raise ValueError('the value of two tensors should be 0 or 1')
        TN, FN, FP, TP = count
        try:
            IoU = TP / (TP + FP + FN)
        except ZeroDivisionError:
            IoU = 1
        res.append(IoU)
    return average(res)
