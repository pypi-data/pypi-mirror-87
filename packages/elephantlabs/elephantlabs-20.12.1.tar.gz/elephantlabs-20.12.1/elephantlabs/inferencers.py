import numpy as np
import torch
import torch.nn as nn
from argparse import Namespace
import logging


class Inferencer(object):
    def __init__(self, model, sp_model, device, tokens_to_ignore, special_tokens):
        self.model = model
        self.sp_model = sp_model
        self.tokens_to_ignore = tokens_to_ignore
        self.device = device
        self.model.to(device)
        self.special_tokens = special_tokens

    def generate_tokens(self, recipe: object, tokens_to_generate: int, top_k: int, N_start_tokens=5) -> dict:
        """
        This method actually generates the recipe. It takes a Recipe-Object as input,
        passes it to the model and generates tokens_to_generate tokens.

        Args:
            recipe: The Recipe object, consisting of ingredients, type, etc.
            tokens_to_generate: Amount of tokens to generate.
            top_k: Hyperparameter for generation.

        Returns:
            Returns a dictionary with the output_ids (First N_start_tokens  + generated tokens)
        """
        assert N_start_tokens > 0, "At least 1 Token to start with."
        logging.debug(f"###### Inferencer: Starting to generate tokens.")
        recipe_enc = recipe.encode(sp_model=self.sp_model)  # recipe_enc should be equal to batch
        output_ids = self._gen_loop(recipe_enc, tokens_to_generate, top_k, N_start_tokens).tolist()
        logging.debug(f"Inferencer: Finished generating tokens.")

        return {"output_ids": output_ids}

    def _gen_loop(self, recipe_enc, tokens_to_generate, top_k, N_start_tokens):
        """
        Helper method. Given a set of input ids, generate tokens until
        END-Token or until tokens_to_generate tokens were generated.

        Args:
            - recipe_enc: A dict containing the encoded recipe. Dimensions and datatypes matter!
            - tokens_to_generate: Amount of tokens to generate.
            - top_k: Hyperparameter for generation.
            - N_start_tokens: N first tokens of the phrase.

        Returns:
            - An np.array consisting of all the tokens generated.
        """
        logging.debug(f"#### Inferencer: Starting generation loop.")

        src_enc = recipe_enc.get("src_enc").unsqueeze(1)   # (S, 1)
        tgt_enc = recipe_enc.get("tgt_enc").unsqueeze(1)  # (T, 1)

        tgt_enc = tgt_enc[:N_start_tokens, ...]

        tgt_key_padding_mask = recipe_enc.get("tgt_padding_mask").unsqueeze(0)  # (1, T)
        src_key_padding_mask = recipe_enc.get("src_padding_mask").unsqueeze(0)  # (1, S)

        tgt_key_padding_mask = tgt_key_padding_mask[..., :N_start_tokens]
        logging.debug(f"#### tgt_enc.shape: {tgt_enc.shape}, src_enc.shape: {src_enc.shape}")

        for step in range(tokens_to_generate):
            winner = self._gen_next(src_enc, tgt_enc, src_key_padding_mask,
                                    tgt_key_padding_mask, top_k)

            tgt_enc = torch.cat((tgt_enc.view(-1), torch.tensor(winner).unsqueeze(0))).unsqueeze(1)
            tgt_key_padding_mask = torch.cat((tgt_key_padding_mask.view(-1), torch.tensor(False).unsqueeze(0))).unsqueeze(0)

            if winner == self.special_tokens.get("eos_token"):  # stopping token
                return tgt_enc[..., 0]

        logging.debug(f"Inferencer: Finished generation loop.")
        return tgt_enc[..., 0]

    def _gen_next(self, src_enc, tgt_enc, src_key_padding_mask, tgt_key_padding_mask, top_k):
        """
        Helper function.
        Given src_enc and top_k, generate only one token.

        Args:
            src_enc: The src_enc of shape (1, S)
            tgt_enc: Target consists of
                a) the start sequence and
                b) the previously generated tokens
                of shape (1, T)
            top_k: top k to sample from.
        Returns:
             Returns the predicted token as integer.

        Todo:
            update doc
        """
        logging.debug(f"### Inferencer: Starting to generate next token.")

        src_enc = src_enc.to(self.device)
        tgt_enc = tgt_enc.to(self.device)
        src_key_padding_mask = src_key_padding_mask.to(self.device)
        tgt_key_padding_mask = tgt_key_padding_mask.to(self.device)

        with torch.no_grad():
            lm_logits = self.model(src_enc, tgt_enc, src_key_padding_mask, tgt_key_padding_mask)

        logging.debug(f"### Inferencer: lm_logits.shape: {lm_logits.shape}")

        predictions = lm_logits[-1, 0, :]

        logging.debug(f"### Inferencer: predictions.shape: {predictions.shape}, pred[0]: {predictions[0]}")

        # predictions = torch.topk(predictions[1:], top_k)  # todo: hack, ignore 0 (<PAD>)
        predictions = torch.topk(predictions, top_k)  # todo: hack, ignore 0 (<PAD>)

        new_logits = predictions[0]
        new_items = predictions[1].cpu().numpy()

        probs = nn.functional.softmax(new_logits, dim=0).cpu().numpy()

        logging.debug(f"### Inferencer: probs: {probs}")

        winner = int(np.random.choice(new_items, p=probs))

        logging.info(f"Inferencer: Finished generation of next token: {winner}.\n")
        return winner
