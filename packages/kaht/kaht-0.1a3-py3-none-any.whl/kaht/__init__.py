from .model import KahtModuleCallback, KahtDataModule, KahtModule
from .base import SaveDelegate, Transferable
from .metrics import MetricsItem, do_metrics
from .trainer import TrainerConfigBase, Trainer

__version__ = '0.1a3'


@property
def version():
    return __version__


del metrics

__all__ = ['Trainer', 'TrainerConfigBase', 'KahtModuleCallback', 'KahtModule', 'KahtDataModule',
           'MetricsItem',
           'do_metrics', 'SaveDelegate', 'Transferable', '__version__']
