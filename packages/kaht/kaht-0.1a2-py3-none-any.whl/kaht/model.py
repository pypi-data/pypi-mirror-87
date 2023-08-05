from abc import ABC
from typing import Protocol, List, Any, Generator, Union, Iterable, Literal
from torch.utils.data.dataloader import DataLoader
from torch.optim.optimizer import Optimizer
import torch
from logging import Logger
from .base import Transferable, SaveDelegate

MODE = Literal['eval', 'train']
SAVED_SUFFIX = Literal['_best', '_latest']
TEST_CHOICES = Literal['best', 'latest']


class KahtDataModule(Transferable, ABC):
    def train_dataloader(self, *args, **kwargs) -> Generator[Transferable, None, None]:
        raise NotImplementedError

    def test_dataloader(self) -> Iterable[Transferable]: ...

    def valid_dataloader(self) -> Iterable[Transferable]: ...


class KahtModuleCallback(Protocol):
    mode: MODE

    save_delegate: SaveDelegate

    def will_train(self, *args, **kwargs): ...

    def on_train_one_step_start(self, logger: Logger): ...

    def train_one_step(self, task_batch) -> torch.Tensor:
        raise NotImplementedError

    def configure_optimizer(self) -> Union[Optimizer, List[Optimizer]]: ...

    def train_steps_end(self, outputs: List[Any]): ...

    def on_train_end(self): ...

    def will_test(self, *args, **kwargs): ...

    def test_one_task(self, batch): ...

    def on_test_end(self, outpus: List[Any]): ...

    def will_valid(self, *args, **kwargs): ...

    def valid_one_task(self, batch) -> Any: ...

    def on_valid_end(self, outpus: List[Any]): ...

    def params_for_clip(self): ...

    def report_every(self, losses: Iterable): ...

    def save(self, suffix: SAVED_SUFFIX, others: str = ''):
        """ Save and return saved result.
        :param suffix:
        :param others: other information
        :return:
        """
        raise NotImplementedError

    @property
    def training(self) -> bool:
        return self.mode == 'train'

    def switch(self, mode: MODE):
        raise NotImplementedError


class KahtModule(KahtModuleCallback, torch.nn.Module, ABC):
    model_name: str = 'KahtModule'
    current_epoch: int = 0

    def next(self):
        self.current_epoch += 1

    def __init__(self):
        super(KahtModule, self).__init__()

    def switch(self, mode: MODE):
        if mode == 'eval':
            self.eval()
        elif mode == 'train':
            self.train()

    def save_checkpoint(self, filename: str):
        torch.save(self, filename)

    def save(self, suffix: SAVED_SUFFIX, others: str = ''):
        filename = f"{self.model_name}_{others}_{suffix}.ckpt"
        self.save_checkpoint(filename)
        self.save_delegate.on_save(filename)
