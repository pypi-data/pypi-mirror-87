import copy
import pandas as pd
import numpy as np
from .train_unit import train
from .test_unit import test
import torch
import os


def train_overall(model, criterion, optimizer, trainLoader, valLoader, num_epochs, saveaddr=''):
    '''
    model needs to move to device you want.
    '''
    best_model_wts = copy.deepcopy(model.state_dict())
    best_loss = np.inf
    train_loss_all, train_IoU_all, val_loss_all, val_IoU_all = [], [], [], []
    print("Train on", next(model.parameters()).device)
    for epoch in range(1, num_epochs + 1):
        print("Epoch {}/{}".format(epoch, num_epochs))
        record = train(model, criterion, optimizer, trainLoader)
        train_loss_all.append(record['loss'])
        train_IoU_all.append(record['IoU'])
        print(f"EPOCH {epoch}: Train Loss: {record['loss']:.4f}, Train IoU: {record['IoU']:.3f}")
        record = test(model, criterion, valLoader)
        val_loss_all.append(record['loss'])
        val_IoU_all.append(record['IoU'])
        print(f"EPOCH {epoch}: Val Loss: {record['loss']:.4f}, Val IoU: {record['IoU']:.3f}")
        if saveaddr:
            torch.save(model, os.path.join(saveaddr, f'unet_{epoch}.pkl'))

        if record['loss'] < best_loss:
            best_loss = record['loss']
            best_model_wts = copy.deepcopy(model.state_dict())

    train_process = pd.DataFrame(
        data={
            "epoch": range(1, num_epochs + 1),
            "train_loss_all": train_loss_all,
            'train_IoU_all': train_IoU_all,
            "val_loss_all": val_loss_all,
            'val_IoU_all': val_IoU_all
        })
    model.load_state_dict(best_model_wts)
    return model, train_process
