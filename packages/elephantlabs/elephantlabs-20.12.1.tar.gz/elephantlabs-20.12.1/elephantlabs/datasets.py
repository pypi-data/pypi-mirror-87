from torch.utils.data import Dataset
from argparse import Namespace
import random


class RecipeGeneratorDataset(Dataset):  # todo make distributed dataset
    """
    Input: - Recipes: List
    """
    def __init__(self, recipes, sp_model, hparams: Namespace):
        self.sp_model = sp_model
        self.items = []
        self.n_ctx_tgt = hparams.n_ctx_tgt
        self.n_ctx_src = hparams.n_ctx_src
        self.Recipes = recipes
        random.Random(42).shuffle(self.Recipes)

        self.items = recipes

    def __getitem__(self, idx):
        item = self.items[idx]
        item_enc = item.encode(self.sp_model)

        return item_enc

    def __len__(self):
        return len(self.items)  # TODO
