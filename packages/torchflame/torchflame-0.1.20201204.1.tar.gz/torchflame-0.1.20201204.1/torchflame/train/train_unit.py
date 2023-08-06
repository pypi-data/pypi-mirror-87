from tqdm import tqdm
import torch
from .functional import calIoU


def train(model, criterion, optimizer, trainLoader): 

    train_loss, train_IoU, batchs = 0.0, 0.0, 0
    device = next(model.parameters()).device
    model.train()
    for X, Y in tqdm(trainLoader):
        optimizer.zero_grad()
        X, Y = X.to(device), Y.to(device)
        out = model(X)
        loss = criterion(out, Y)
        loss.backward()
        optimizer.step()
        batchs += 1
        train_loss += loss.item()
        prediction = torch.argmax(out, 1)
        train_IoU += calIoU(prediction, Y)
    return {'loss': train_loss / batchs, 'IoU': train_IoU / batchs}
