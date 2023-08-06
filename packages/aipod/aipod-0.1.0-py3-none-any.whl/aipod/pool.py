import gc
import threading

from collections import OrderedDict
from typing import ClassVar

from aipod import logger
from aipod.model import AIModelBase


class ModelPool:
    def __init__(
        self, model_class: ClassVar[AIModelBase], size: int = None, datapath: str = None
    ) -> None:
        self.model_class = model_class
        self.pool = OrderedDict()  # LRU cache
        if size is None:
            size = 1
        self.size = int(size)
        self.lock = threading.Lock()
        self.datapath = datapath

    def get(self, version: str) -> AIModelBase:
        with self.lock:
            if version is None:
                version = "default"
            if version not in self.pool:
                self._load_model(version)
            model = self.pool.pop(version)
            self.pool[version] = model
            return model

    def release(self, version: str) -> None:
        with self.lock:
            self._release(version)

    def _load_model(self, version: str) -> AIModelBase:
        if self.size > 0:
            while len(self.pool) >= self.size:
                keys = list(self.pool.keys())
                logger.debug(f"release model {keys[0]}")
                self._release(keys[0])
                logger.debug(
                    f"finish release model {keys[0]}: {list(self.pool.keys())}"
                )
        self.pool[version] = self.model_class(version=version, datapath=self.datapath)

    def _release(self, version: str) -> None:
        if version in self.pool:
            model = self.pool.pop(version)
            model.dispose()
            del model
            gc.collect()
