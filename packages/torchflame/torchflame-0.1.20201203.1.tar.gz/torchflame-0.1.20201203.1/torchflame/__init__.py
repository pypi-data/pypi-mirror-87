# -*- coding:utf-8 -*-

from . import dataset, models, train, functional, optim

__author__ = 'Jewelry'

__all__ = ['models', 'dataset', 'train', 'functional', 'optim']

# 12.2
# extend plot_procedure to dataframes

# 12.1
# add plot_procedure grid_resize eval_tranforms fuse

# 11.30
# verify the centerCrop and oversampling of IIset
# add plot_pair 
# delete nn temporarily

# 11.29
# add rev_trans
# debug IIset
# add non-padding unet
# add choice 'centercrop' to IIset
# rectify plot4 -> plots

# 11.28
# add optim and import optimizers from torch_optimizer
# add Swish 
# RandomCrop -> RandomResizedCrop
# TODO upload to pypi

# 11.23
# 1. add train_unit test_unit
# 2. unet rectified
# 3. calIoU fix the issue of nan
# 4. Important: transforms->Cotrans, Never mix torch stardart transforms and Cotrans up!!
