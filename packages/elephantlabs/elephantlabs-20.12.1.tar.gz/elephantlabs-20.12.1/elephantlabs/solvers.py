import time, os, torch, logging
from torch import nn
import torch.utils.checkpoint
from tqdm import trange
from argparse import Namespace
from elephantlabs.utils import AverageMeter
from torch.utils.tensorboard import SummaryWriter


class Solver(object):
    def __init__(self, hparams: Namespace, model, optim, train_dataloader,
                 val_dataloader, test_dataloader, device, sp_model):
        logging.debug("Starting instantiating Solver. ")

        # self.weights = hparams.get("class_weights", None)
        self.cross_entropy = nn.CrossEntropyLoss(weight=hparams.class_weights)  # , reduction = "mean")
        # if not self.weights == None:
        #     print("Setting weighted Cross Entropy.")
        #     self.cross_entropy = nn.CrossEntropyLoss(weight=self.weights)  # , reduction = "mean")
        # else:
        #     print("Setting Cross Entropy without weights.")
        #     self.cross_entropy = nn.CrossEntropyLoss()
        self.hparams = hparams

        # for key in hparams:
        #     setattr(self, key, hparams[key])

        # self.model = config.get("model")
        # self.optimizer = config.get("optim")
        # self.train_dataloader = config.get("train_dataloader")
        # self.val_dataloader = config["val_dataloader"]
        # self.test_dataloader = config.get("test_dataloader")

        self.model = model
        self.optimizer = optim
        self.train_dataloader = train_dataloader
        self.val_dataloader = val_dataloader
        self.test_dataloader = test_dataloader
        self.device = device
        self.sp_model = sp_model

        self.iter_train_dataloader = iter(self.train_dataloader)
        self.iter_val_dataloader = iter(self.val_dataloader)
        self.iter_test_dataloader = iter(self.test_dataloader)

        self.train_loss = AverageMeter()
        self.val_loss = AverageMeter()
        self.test_loss = AverageMeter()

        # self.l2_reg = config.get("l2_reg", 0)

        self.current_epoch = 0
        self.steps_per_epoch = len(self.train_dataloader)
        self.steps = 0
        self.starting_time = None

        # self.val_every = config.get("val_every", 10)
        # self.N_val_batches = config.get("N_val_batches", 4)
        # self.skip_first_steps = config.get("skip_first_steps", 0)

        # self.device = config.get("device")
        self.writer = SummaryWriter()
        self.model.to(self.device)
        # self._write_graph()

        logging.debug("Finished instantiating Solver. ")

    def train_step(self):
        """
        Is called during the training loop. Computes the training loss and performs backprop.
        Returns:
            The loss object.
        """
        logging.debug(f"Solver: ### Starting training step.")
        batch = self._get_batch()

        self.model.zero_grad()  # evtl ueberfluessig
        self.optimizer.zero_grad()

        self.model.train()
        self.steps += 1

        loss = self._step(batch, mode="train")
        loss.backward()

        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)

        self.optimizer.step()
        torch.cuda.empty_cache()

        self.writer.add_scalar("Loss/train", loss, self.steps)
        logging.debug(f"Solver: ### Finished training step.\n")

        return loss

    def validate(self):

        if self.steps % self.hparams.val_every == 0:
            logging.debug(f"Solver: ### Starting validation.")
            self.model.eval()
            L = []

            for i in range(self.hparams.N_val_batches):  # todo: empty cache? cuda overflow
                batch = self._get_batch(mode="val")
                loss = self._step(batch, mode="val")  # todo: mode = "val"
                L.append(loss)

            loss = sum(L) / len(L)
            self.val_loss.update([self.steps, float(loss.cpu().detach().numpy())])
            self.writer.add_scalar("Loss/val", self.steps)

            torch.cuda.empty_cache()
            logging.debug(f"Solver: Finished validation.")
            return loss

    def train(self, epochs, path=os.getcwd(), filename="model", save_every=False):
        """
        The main training loop.
        Args:
            epochs: Amount of epochs.
            path: Where the model is to be saved.
            filename: Name of the model.
            save_every: Minutes.
        """
        logging.info(f"Solver: ####### Starting training ....")
        assert type(save_every) is int or save_every is False, "save_every must be int or set to False"

        self.starting_time = time.time()

        for e in range(epochs):
            logging.info(f"Solver: ####### Starting Epoch: {e}")
            self.current_epoch += 1
            self.iter_train_dataloader = iter(self.train_dataloader)
            pbar = trange(self.steps_per_epoch, position=0, unit=" Steps")

            for step in pbar:
                self.train_step()  # also increments self.steps
                self.validate()  # does not increment self.steps

                self._log_pbar(pbar, epochs)
                self._handle_save(path, filename, save_every)

        if save_every:
            self.save(path, filename)

        logging.info(f"Solver: ####### Finished training.")
        # self.writer.close()

    def _lm_loss_fn(self, lm_logits, tgt):
        """
        This Loss function is generally used in Language Models.
        Removes the last entry of the logits.
        Removes the first entry of the target.

        Args:
            lm_logits: logits of shape (ctx, N, n_embedd)  # todo
            tgt: Target is of shape (N, ctx)  # todo

        Returns:
            The LM loss

        TODO:
            Some models return logits of shape (N, ctx, n_embedd).
            a) generalize all models to output same shape
            b) adapt this method to either shape
        """
        logging.debug(f"Solver: Starting LM loss.")
        loss = nn.CrossEntropyLoss()

        # lm_logits = lm_logits.permute(1, 0, 2)  # todo: hack: (N, ctx, n_vocab)

        # Shift so that tokens < n predict n
        logging.debug(f"Solver: lm_logits.shape: {lm_logits.shape}")

        # shift_logits = lm_logits[..., :-1, :].contiguous()
        # shift_labels = tgt[..., 1:].contiguous()

        shift_logits = lm_logits[:-1, ..., :].contiguous()
        shift_labels = tgt[1:, ...].contiguous()

        logging.debug(f"Solver: shift_logits.shape: {shift_logits.shape}")
        logging.debug(f"Solver: shift_labels.shape: {shift_labels.shape}")

        # Flatten the tokens
        logits = shift_logits.view(-1, shift_logits.size(-1))
        labels = shift_labels.view(-1)

        logging.debug(f"Solver: logits.shape: {logits.shape}")
        logging.debug(f"Solver: labels.shape: {labels.shape}")

        loss = loss(logits, labels)

        logging.debug(f"Solver: Finished LM loss.")

        return loss

    def _log_pbar(self, pbar, epochs):
        """
        Helper method. Updates average train and validation loss in the progress bar.
        Args:
            pbar: Progress bar object.
            epochs: Total amount of epochs in the training loop.
        """
        avg_train_loss = self.train_loss.mean_last_k(10)
        avg_val_loss = self.val_loss.mean_last_k(10)

        pbar.set_description(
            f"Epoch {self.current_epoch:02d} / {epochs:02d}. Avg Train loss: {avg_train_loss:.2f}. Avg Val "
            f"loss: {avg_val_loss:.2f}.")
        pbar.refresh()

    def _handle_save(self, path: str, filename: str, save_every: int):
        """
        Helper method. Save a model if it is past due to be saved.
        Args:
            path:
            filename:
            save_every: Minutes.
        """
        if save_every and time.time() - self.starting_time > 60 * save_every:
            self.save(path, filename)
            self.starting_time = time.time()

    def _step(self, batch, mode="train"):
        """
        Has to be implemented by the child class.
        This method has to:
            - get Tensors from batch
            - send Tensors to relevant device
            - call model (if mode != train: with torch.no_grad())
            - compute loss
            - apply l2_reg
            - return loss object
        Args:
            batch: The dict containing model-specific inputs, labels, masks, ...
            mode: "train" or else

        Returns:
            loss: The loss object
        """
        raise NotImplementedError

    def _get_batch(self, mode="train"):
        """
            Resets the iterator for train/ val dataloader if necessary and returns the next batch.
        Args:
            mode: "train" or else

        Returns:
            The current batch for either training or validation step.
        """
        logging.debug(f"Solver: ## Getting batch.")
        if mode == "train":
            try:
                batch = next(self.iter_train_dataloader)
            except:
                self.iter_train_dataloader = iter(self.train_dataloader)
                batch = next(self.iter_train_dataloader)

        else:
            try:
                batch = next(self.iter_val_dataloader)
            except:
                self.iter_val_dataloader = iter(self.val_dataloader)
                batch = next(self.iter_val_dataloader)

        logging.debug(f"Solver: Got batch. Solver keys: {[k for k in batch.keys()]}")
        logging.debug(f"Solver: ## Finished getting batch.")

        return batch

    def _regularize_l2(self):
        logging.debug(f"Solver: Starting l2 regularization.")

        l2_loss = 0
        for W in self.model.parameters():
            l2_loss += W.norm(2)

        logging.debug(
            f"Solver: Finished l2 regularization. L2_loss: {float(l2_loss.cpu().detach().numpy()) * self.hparams.l2_reg}")
        return l2_loss * self.hparams.l2_reg

    def _write_graph(self):
        """
        Has to be implemented by child class.
        Caution: When called, model has to be in memory (not GPU).

        This method has to:
            - get a batch (CPU)
            - move batch values to device
            - write the graph using SummaryWriter()
        Returns:

        """
        raise NotImplementedError

    def save(self, path, filename):
        save_to = os.path.join(path, f"{filename}-step-{self.steps}-model.pt")
        print(f"\nSaving Model to {save_to}")
        torch.save(self.model.state_dict(), save_to)

        save_to = os.path.join(path, f"{filename}-optim.pt")
        print(f"\nSaving Optimizer to {save_to}")
        torch.save(self.optimizer.state_dict(), save_to)


class SolverRecipeGenerator(Solver):
    def __init__(self, hparams: Namespace, model, optim, train_dataloader,
                 val_dataloader, test_dataloader, device, sp_model):

        super(SolverRecipeGenerator, self).__init__(hparams, model, optim, train_dataloader,
                                                    val_dataloader, test_dataloader, device, sp_model)

        self.lm_train_loss = AverageMeter()

    def _step(self, batch, mode="train"):
        logging.debug(f"Solver: # Starting step.")

        tgt_enc = batch.get("tgt_enc").to(self.device)
        src_enc = batch.get("src_enc").to(self.device)
        tgt_key_padding_mask = batch.get("tgt_padding_mask").to(self.device)
        src_key_padding_mask = batch.get("src_padding_mask").to(self.device)

        tgt_enc = tgt_enc.permute(1, 0)  # (T, N)  todo: hack
        src_enc = src_enc.permute(1, 0)  # (S, N)  todo: hack

        if mode != "train":
            with torch.no_grad():
                lm_logits = self.model(src_enc, tgt_enc, src_key_padding_mask, tgt_key_padding_mask)
        else:
            lm_logits = self.model(src_enc, tgt_enc, src_key_padding_mask, tgt_key_padding_mask)
        logging.debug(f"Solver: lm_logits.shape: {lm_logits.shape}")

        # tgt_enc = tgt_enc[:50, ...]  # to check if variable length tgt works!

        lm_loss = self._lm_loss_fn(lm_logits, tgt_enc)
        loss = lm_loss

        if self.hparams.l2_reg != 0:
            l2_loss = self._regularize_l2()
            loss += l2_loss

        self.train_loss.update([self.steps, float(loss.cpu().detach().numpy())])
        self.lm_train_loss.update([self.steps, float(lm_loss.cpu().detach().numpy())])

        logging.debug(f"Solver: # Finished step.")
        return loss

    def _write_graph(self):
        logging.debug(f"Solver: Starting to write Graph.")
        batch = self._get_batch()  # todo: this works, AS LONG as there is only one device.
        src_enc = batch.get("src_enc").to(self.device)
        tgt_enc = batch.get("tgt_enc").to(self.device)
        self.writer.add_graph(self.model, input_to_model=[src_enc, tgt_enc])
        logging.debug(f"Solver: Finished writing Graph.")
