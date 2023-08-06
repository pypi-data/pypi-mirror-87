from argparse import Namespace
import torch, logging
from torch import nn
import math


def position_for(batch_size, n_steps, past_length, device=None):
    """
    Simply returns ([[0, 1, 2, ..., ]])
    Args:
        batch_size:
        n_steps:
        past_length:
        device:

    Returns:

    Todo:
        Update doc string.
    """

    return (torch.arange(past_length, n_steps + past_length, device=device)
            .unsqueeze(0).repeat(batch_size, 1))


class TransformerWithHeads(nn.Module):
    def __init__(self, hparams: Namespace):
        super(TransformerWithHeads, self).__init__()
        self.hparams = hparams
        self.EncoderDecoder = EncoderDecoder(hparams)
        self.lm_head = nn.Linear(hparams.embedding_dim, hparams.n_vocab)

    def forward(self, src_enc, tgt_enc, src_key_padding_mask=None,
                tgt_key_padding_mask=None):
        logging.debug("######### TransformerWithHeads: Starting forward.")
        hidden_states = self.EncoderDecoder(src_enc, tgt_enc, src_key_padding_mask, tgt_key_padding_mask)  # (T, N, E)
        logging.debug(f"######### hidden_states.shape: {hidden_states.shape}")
        lm_logits = self.lm_head(hidden_states)  # (T, N, n_vocab)
        logging.debug(f"######### lm_logits.shape: {lm_logits.shape}")

        return lm_logits


class EncoderDecoder(nn.Module):
    def __init__(self, hparams: Namespace):
        super(EncoderDecoder, self).__init__()
        self.hparams = hparams

        def get_emb(n_vocab, embedding_dim):
            embedding_layer = torch.nn.Embedding(n_vocab,
                                                 embedding_dim,
                                                 padding_idx=3)  # todo: dirty
            return embedding_layer

        self.text_embedding = get_emb(hparams.n_vocab, hparams.embedding_dim)

        # Positional encoding is (ctx, 1, embedding_dim)
        self.register_buffer(  # todo: different positional encoding for src ?
            "positional_encoding",
            self.generate_positional_encoding(
                ctx=self.hparams.n_ctx_tgt,
                embedding_dim=self.hparams.embedding_dim,
            )
        )

        self.transformer = torch.nn.Transformer(  # src_enc input shape: (S, N, E) !
            d_model=self.hparams.embedding_dim,
            nhead=self.hparams.num_attention_heads,
            num_encoder_layers=self.hparams.num_encoder_layers,
            num_decoder_layers=self.hparams.num_decoder_layers,
            dim_feedforward=self.hparams.intermediate_feedforward_dim,
            dropout=self.hparams.intermediate_dropout,
        )

        # Mask has -inf for all values that follow tgt (T, T)
        self.register_buffer(
            "tgt_attention_mask",
            self.transformer.generate_square_subsequent_mask(self.hparams.n_ctx_tgt),
        )

    def generate_positional_encoding(self, ctx: int, embedding_dim: int) -> torch.FloatTensor:
        # Dim must be even
        assert embedding_dim % 2 == 0

        # Returns a (seq_len, emb) tensor
        positional_encodings = []
        for pos in range(ctx):
            positional_encodings.append([])
            for i in range(0, int(embedding_dim / 2)):
                # Even index
                positional_encodings[-1].append(
                    math.sin(pos / (10000 ** (2 * i / embedding_dim)))
                )
                # Odd index
                positional_encodings[-1].append(
                    math.cos(pos / (10000 ** (2 * i / embedding_dim)))
                )
        result = torch.FloatTensor(
            positional_encodings,
        ).unsqueeze(1)
        assert result.shape == (ctx, 1, embedding_dim)
        return result

    def forward(self, src_enc, tgt_enc, src_key_padding_mask, tgt_key_padding_mask):
        """
        src_enc (S, N)
        tgt_enc (T, N)
        src_padding_mask (N, S)
        tgt_padding_mask (N, T)

        Should return (H, N, E)
        """
        logging.debug("######## EncoderDecoder: Starting forward.")
        logging.debug(f"######## src_enc.shape: {src_enc.shape}, tgt_enc.shape: {tgt_enc.shape}")

        # tgt_enc = tgt_enc[:50, ...]  # to check if variable length tgt works!
        # tgt_key_padding_mask = tgt_key_padding_mask[..., :50]  # to check if variable length tgt works!

        tgt_emb = self.text_embedding(tgt_enc)  # (T, N, embedding_dim)
        src_emb = self.text_embedding(src_enc)  # (S, N, embedding_dim)

        logging.debug(f"######## tgt_emb.shape: {tgt_emb.shape}, src_emb.shape: {src_emb.shape}")

        positional_tgt_emb = self.positional_encoding[:tgt_enc.shape[0]]  # (T, 1, embedding_dim)
        positional_src_emb = self.positional_encoding[:src_enc.shape[0], ..., ...]  # (S, 1, embedding_dim)

        logging.debug(f"######## positional_tgt_emb.shape: {positional_tgt_emb.shape}, "
                      f"positional_src_emb.shape: {positional_src_emb.shape}")

        positional_src_emb = src_emb + positional_src_emb  # (S, 1, embedding_dim)
        positional_tgt_emb = tgt_emb + positional_tgt_emb  # (T, 1, embedding_dim)

        logging.debug(f"######## src_key_padding_mask.shape: {src_key_padding_mask.shape}, "
                      f"tgt_key_padding_mask.shape: {tgt_key_padding_mask.shape}")

        two_d_attn_mask = self.tgt_attention_mask[:tgt_enc.shape[0], :tgt_enc.shape[0]]
        logging.debug(f"######## two_d_attn_mask.shape: {two_d_attn_mask.shape}")

        hidden_states = self.transformer(
            src=positional_src_emb,
            tgt=positional_tgt_emb,
            src_key_padding_mask=src_key_padding_mask,
            tgt_key_padding_mask=tgt_key_padding_mask,
            tgt_mask=two_d_attn_mask,
        )

        return hidden_states
