from typing import Protocol
from torch import device


class Transferable(Protocol):
    def to(self, gpu: device):
        raise NotImplementedError


class SaveDelegate(Protocol):
    def on_save(self, *args):
        ...
