from tap import Tap
import torch
from torch import nn
from torch.optim.optimizer import Optimizer
from .model import KahtModuleCallback, KahtDataModule, KahtModule
from kaht.logger import logger
import os
from .base import SaveDelegate
from collections import deque


class TrainerConfigBase(Tap):
    min_steps: int = 1
    max_steps: int = 1
    valid_interval: int = 1
    report_interal: int = 1
    grad_clip: float = -1.0
    log_dir: str = 'logs/'
    log_file: str = '/dev/null'  # custom your log file
    gpu: int = -1

    @property
    def device(self):
        return torch.device(
                f"cuda:{self.gpu}" if self.gpu > 0 and torch.cuda.is_available() else 'cpu')


class Trainer(SaveDelegate):
    module: KahtModuleCallback
    data_module: KahtDataModule

    def __init__(self, config: TrainerConfigBase):

        if not os.path.exists(os.path.join('.', config.log_dir)):
            os.mkdir(os.path.join('.', config.log_dir))
        self.min_steps = config.min_steps
        self.max_steps = config.max_steps
        self.current_step: int = 0
        self.valid_every = config.valid_interval
        self.report_every = config.report_interal
        self.device = config.device
        self.grad_clip = config.grad_clip
        self.logger = logger(os.path.join(config.log_dir, config.log_file))
        self.saved_models = list()

    def on_save(self, *args):
        for name in args:
            self.saved_models.append(name)

    def fit(self,
            module: KahtModule,
            data_module: KahtDataModule,
            end_with_test: bool = False):
        self.module = module
        self.data_module = data_module
        module.current_epoch = self.current_step
        module.to(self.device)
        module.will_train()
        optimizers = module.configure_optimizer()
        losses = deque([], self.report_every)
        for batch in data_module.train_dataloader():
            if not module.training:
                module.switch('train')
            batch.to(self.device)
            module.on_train_one_step_start(self.logger)
            loss = module.train_one_step(batch)
            losses.append(loss.cpu().item())
            if isinstance(optimizers, list):
                for optim in optimizers:
                    assert isinstance(optim, Optimizer)
                    optim.zero_grad()
                    loss.backward()
                    if self.grad_clip > 0:
                        nn.utils.clip_grad_norm_(module.params_for_clip(), self.grad_clip)
                    optim.step()
            elif isinstance(optimizers, Optimizer):
                optimizers.zero_grad()
                loss.backward()
                if self.grad_clip > 0:
                    nn.utils.clip_grad_norm_(module.params_for_clip(), self.grad_clip)
            else:
                raise ValueError(f"NOT SUPPORT OPTIM TYPE, support List[Optim] or Optim, GET"
                                 f" {type(optimizers)}")
            self.current_step += 1
            module.next()
            if self.current_step % self.valid_every == 0:
                module.switch('eval')
                self.logger.info(f"Valid after {self.current_step} steps...")
                val_outputs = list()
                for test_batch in data_module.valid_dataloader():
                    module.will_valid()
                    test_batch.to(self.device)
                    output = module.valid_one_task(test_batch)
                    val_outputs.append(output)
                module.on_valid_end(val_outputs)
            if self.current_step % self.report_every == 0:
                module.report_every(losses=losses)
            if self.current_step == self.max_steps:
                self.logger.critical("END TRAINING.")
                module.save('_latest')
                if end_with_test:
                    module.switch('eval')
                    self.logger.info("Testing after train end...")
                    test_outputs = list()
                    for test_batch in data_module.test_dataloader():
                        module.will_test()
                        test_batch.to(self.device)
                        output = module.test_one_task(test_batch)
                        test_outputs.append(output)
                    module.on_valid_end(test_outputs)
                break
        module.on_train_end()
