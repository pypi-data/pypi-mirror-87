import json
import shutil

from pathlib import Path
from typing import Any
from typing import Dict

from aipod import logger
from aipod.trainlog import TrainningLogger


class AIModelBase:
    def __init__(self, version: str = None, datapath: str = None, **kwargs) -> None:
        self.version = version or "default"
        self.datapath = Path(datapath or "appdata/")
        self.trainning_logger = TrainningLogger(self.model_dir() / "trainning.log")
        self._model_info: Dict = None
        self.disposed = False

    def model_dir(self, *names: str, mkdir: bool = True, clear: bool = False) -> Path:
        verpath = self.datapath / "models" / self.version
        for name in names:
            verpath /= name
        if clear and verpath.exists():
            shutil.rmtree(verpath)
        if mkdir:
            verpath.mkdir(exist_ok=clear is False, parents=True)
        return verpath

    @property
    def model_info_path(self) -> Path:
        return self.model_dir(mkdir=False) / "model.json"

    @property
    def model_info(self):
        if self._model_info is None:
            if self.model_info_path.exists():
                with open(self.model_info_path, "r") as info_fp:
                    self._model_info = json.load(info_fp)
            else:
                raise Exception(
                    f"{self.model_info_path} not exists, model may haven`t initialize yet."
                )
        return self._model_info

    def dispose(self):
        self.disposed = True

    # interface methods：

    def initialize(self, binary_data: bytes = None, **kwargs) -> Any:
        logger.debug(f"initialize model {self.version}")
        # init model dir
        model_dir = self.model_dir(mkdir=False)
        if model_dir.exists():
            shutil.rmtree(model_dir)
        model_dir.mkdir(parents=True, exist_ok=False)

        # dump model parameters
        with open(self.model_info_path, "w") as info_fp:
            json.dump(kwargs, info_fp, indent=4, ensure_ascii=False)

        self._model_info = kwargs

        return {"result": True, "model_info": self.model_info}

    def train(self, binary_data: bytes = None, **kwargs) -> Any:
        raise NotSupportedError()

    def predict(self, binary_data: bytes = None, **kwargs) -> Any:
        raise NotImplementedError()

    def log(self, binary_data: bytes = None, name: str = "trainning", **kwargs) -> Any:
        if name == "trainning":
            return self.trainning_logger.read_all()
        else:
            raise NotImplementedError()


class NotSupportedError(Exception):
    """不支持的操作"""
