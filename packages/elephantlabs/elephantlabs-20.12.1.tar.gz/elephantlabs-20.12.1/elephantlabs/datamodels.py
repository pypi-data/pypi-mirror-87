import hashlib, torch
import numpy as np
from argparse import Namespace


class DataModel(object):
    """
    Todo: Implement Base class.
    """
    pass


class Recipe(object):
    def __init__(self, data, hparams, special_tokens: dict):
        assert type(data) == dict, "data must be dict."
        assert type(hparams) == Namespace, "hparams must be Namespace."

        self.len_src = hparams.n_ctx_src
        self.len_tgt = hparams.n_ctx_tgt

        self.special_tokens = special_tokens

        for key in data:
            setattr(self, key, data[key])

    def __hash__(self):
        return int(hashlib.sha256(self.comment_text.encode('utf-8')).hexdigest(), 16) % 10 ** 8

    def __eq__(self, other):
        if not isinstance(other, Recipe):
            return NotImplemented
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return self.title

    def __len__(self):
        return len(self.instructions)

    def len_ingredients(self):
        return len(self.ingredients)

    def _pad(self, length):
        pass

    def get_ingredients(self):
        return self.ingredients


    def get_instructions(self):
        return self.instructions

    def _encode_instruction(self, sp_model):
        instructions_enc = sp_model.encode_as_ids(self.instructions)  # todo
        instructions_enc = [self.special_tokens.get("sos_token")] + instructions_enc + [
            self.special_tokens.get("eos_token")]
        instructions_enc = np.array(instructions_enc[:self.len_tgt])
        instructions_enc = torch.LongTensor(np.pad(instructions_enc, (0, self.len_tgt - instructions_enc.shape[0]),
                                                   constant_values=self.special_tokens.get("pad_token")))
        instructions_padding_mask = (instructions_enc == self.special_tokens.get("pad_token"))  # todo padding token
        return instructions_enc, instructions_padding_mask

    def _encode_ingredients(self, sp_model):
        ingredients_enc = [[self.special_tokens.get("sep_token")] + sp_model.encode_as_ids(t) for t in self.ingredients]
        ingredients_enc = [item for sublist in ingredients_enc for item in sublist][:self.len_src]
        ingredients_enc = np.array(ingredients_enc)
        ingredients_enc = torch.LongTensor(np.pad(ingredients_enc, (0, self.len_src - ingredients_enc.shape[0]),
                                                  constant_values=self.special_tokens.get("pad_token")))
        ingredients_padding_mask = (ingredients_enc == self.special_tokens.get("pad_token"))  # todo padding token
        return ingredients_enc, ingredients_padding_mask

    def encode(self, sp_model):
        instructions_enc, instructions_padding_mask = self._encode_instruction(sp_model)
        ingredients_enc, ingredients_padding_mask = self._encode_ingredients(sp_model)
        src_len = int(self.len_src - sum(ingredients_padding_mask))
        tgt_len = int(self.len_tgt - sum(instructions_padding_mask))

        return {
            "tgt_enc": instructions_enc,
            "tgt_padding_mask": instructions_padding_mask,
            "tgt_len": tgt_len,
            "src_enc": ingredients_enc,
            "src_padding_mask": ingredients_padding_mask,
            "src_len": src_len
        }
