import copy
from tqdm import tqdm
import torch
import pandas as pd
import torch.nn.functional as F
from .functional import calIoU

def test(model, criterion, valLoader):

    device = next(model.parameters()).device
    val_loss, val_IoU, batchs = 0.0, 0.0, 0
    model.eval() 
    for X, Y in tqdm(valLoader):
        X, Y = X.to(device), Y.to(device)
        out = model(X)
        loss = criterion(out, Y)
        batchs += 1
        val_loss += loss.item()
        prediction = torch.argmax(out, 1)
        val_IoU += calIoU(prediction, Y)
    return {'loss': val_loss / batchs, 'IoU': val_IoU / batchs}
