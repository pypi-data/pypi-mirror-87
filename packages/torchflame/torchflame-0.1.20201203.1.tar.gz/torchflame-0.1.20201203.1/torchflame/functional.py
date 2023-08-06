import torch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from .dataset.functional import pick, ratio_split, rev_trans
from torchvision import transforms
__all__ = ['plots', 'plot_pair', 'plot_procedure', 'grid_resize', 'eval_tranforms', 'fuse']
__all__ += ['pick', 'ratio_split', 'rev_trans']


def plots(figs, figsize, layout, save=''):
    plt.figure(figsize=figsize)
    assert len(layout) == 2
    for i in range(layout[0] * layout[1]):
        plt.subplot(*layout, i + 1)
        if isinstance(figs[i], (np.ndarray, torch.Tensor)) and len(figs[i].shape) == 2:
            plt.imshow(figs[i], 'Greys_r')
            continue
        plt.imshow(figs[i])
    if save:
        plt.savefig(save, facecolor='white')
    plt.show()


def plot_pair(sample, figsize=(10, 6)):
    plots([rev_trans(sample[0]), sample[1].float()], figsize=figsize, layout=(1, 2))


def plot_procedure(df, keys):
    def _plot(df, keys):
        if isinstance(df, str):
            df = pd.read_excel(df)
        epochs = np.arange(1, len(df) + 1)
        for key in keys:
            plt.plot(epochs, df[key], label=key)
    plt.figure(figsize=(8, 5))
    if isinstance(df, (list, tuple)):
        for Slc in df:
            _plot(Slc, keys)
    else:
        _plot(df, keys)
    plt.legend()
    plt.xlabel("epoch")
    plt.show()


def grid_resize(image, grid):
    width, height = image.size
    image = image.resize((width // grid * grid, height // grid * grid))
    return image


def eval_tranforms(image, norm=[[0.485, 0.456, 0.406], [0.229, 0.224, 0.225]]):
    trans = transforms.Compose([transforms.ToTensor(), transforms.Normalize(*norm)])
    return trans(image).unsqueeze(0)


def fuse(raw, label):
    image = np.array(raw) * 0.8
    image[..., 1] = image[..., 1] + 0.2 * np.array(label.squeeze(0).argmax(dim=0).cpu() * 255)
    return image.astype(np.uint8)
