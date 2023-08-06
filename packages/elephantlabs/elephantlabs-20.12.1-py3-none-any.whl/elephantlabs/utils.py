from torch.utils.data import RandomSampler, DataLoader
from elephantlabs.datasets import RecipeGeneratorDataset
from argparse import Namespace
import numpy as np


def get_recipe_dataloaders(train_data, val_data, sp_model, hparams: Namespace):
    """
    Returns:
        dataloader (N, )
    """
    train_dataset = RecipeGeneratorDataset(train_data, sp_model, hparams)
    train_sampler = RandomSampler(train_dataset)
    train_dataloader = DataLoader(train_dataset, sampler=train_sampler,
                                  batch_size=hparams.batch_size)

    val_dataset = RecipeGeneratorDataset(val_data, sp_model, hparams)
    val_sampler = RandomSampler(val_dataset)
    val_dataloader = DataLoader(val_dataset, sampler=val_sampler,
                                batch_size=hparams.batch_size)

    return train_dataloader, val_dataloader


class AverageMeter(object):
    def __init__(self):
        """every value is a list [step, value]"""
        self.values = [[0, 0]]

    def mean_last_k(self, k=10):
        vals = [val[1] for val in self.values[-k:]]
        return np.mean(vals)

    def update(self, value):
        if self.values[0][1] == 0:
            self.values.pop(0)
        self.values.append(value)

    def reset(self):
        self.values.clear()


