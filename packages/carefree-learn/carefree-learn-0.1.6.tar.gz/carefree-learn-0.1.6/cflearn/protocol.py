import numpy as np

from abc import abstractmethod
from abc import ABCMeta
from typing import Any
from typing import Set
from typing import Dict
from typing import Type
from typing import Tuple
from typing import Union
from typing import Callable
from typing import Optional
from typing import NamedTuple
from cftool.ml import ModelPattern
from cftool.misc import register_core
from cftool.misc import LoggingMixin
from cfdata.tabular import data_type
from cfdata.tabular import batch_type
from cfdata.tabular import str_data_type
from cfdata.tabular import TaskTypes
from cfdata.tabular import DataTuple
from cfdata.tabular import TabularData
from cfdata.tabular.recognizer import Recognizer


class PipelineProtocol(LoggingMixin, metaclass=ABCMeta):
    def __init__(self) -> None:
        self.data = TabularData.simple("reg", simplify=True)

    def fit(
        self,
        x: np.ndarray,
        y: np.ndarray,
        x_cv: np.ndarray,
        y_cv: np.ndarray,
    ) -> "PipelineProtocol":
        self.data.read(x, y)
        return self._core(x, y, x_cv, y_cv)

    @abstractmethod
    def _core(
        self,
        x: np.ndarray,
        y: np.ndarray,
        x_cv: np.ndarray,
        y_cv: np.ndarray,
    ) -> "PipelineProtocol":
        pass

    @abstractmethod
    def predict(self, x: np.ndarray, **kwargs: Any) -> np.ndarray:
        pass

    def to_pattern(self, **predict_config: Any) -> ModelPattern:
        return ModelPattern(predict_method=lambda x: self.predict(x, **predict_config))


data_dict: Dict[str, Type["DataProtocol"]] = {}
sampler_dict: Dict[str, Type["SamplerProtocol"]] = {}
loader_dict: Dict[str, Type["DataLoaderProtocol"]] = {}


class DataSplit(NamedTuple):
    split: "DataProtocol"
    remained: "DataProtocol"
    split_indices: np.ndarray
    remained_indices: np.ndarray


class DataProtocol:
    is_ts: bool
    is_clf: bool
    is_simplify: bool
    raw_dim: int
    num_classes: int

    raw: DataTuple
    converted: DataTuple
    processed: DataTuple
    ts_indices: Set[int]
    recognizers: Dict[int, Optional[Recognizer]]

    _verbose_level: int
    _has_column_names: bool

    @abstractmethod
    def __init__(self, **kwargs: Any):
        self._verbose_level = kwargs.get("verbose_level", 2)

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def read_file(
        self,
        file_path: str,
        *,
        contains_labels: bool = True,
    ) -> Tuple[str_data_type, Optional[str_data_type]]:
        pass

    @abstractmethod
    def read(
        self,
        x: Union[str, data_type],
        y: Optional[Union[int, data_type]] = None,
        *,
        contains_labels: bool = True,
        **kwargs: Any,
    ) -> "DataProtocol":
        pass

    @abstractmethod
    def split(self, n: Union[int, float], *, order: str = "auto") -> DataSplit:
        pass

    @abstractmethod
    def split_with_indices(
        self,
        split_indices: np.ndarray,
        remained_indices: np.ndarray,
    ) -> DataSplit:
        pass

    @abstractmethod
    def transform(self, x: Union[str, data_type], y: data_type = None) -> DataTuple:
        pass

    @abstractmethod
    def transform_labels(self, y: data_type) -> np.ndarray:
        pass

    @abstractmethod
    def recover_labels(self, y: np.ndarray, *, inplace: bool = False) -> np.ndarray:
        pass

    @abstractmethod
    def copy_to(
        self,
        x: Union[str, data_type],
        y: data_type = None,
        *,
        contains_labels: bool = True,
    ) -> "DataProtocol":
        pass

    @abstractmethod
    def save(
        self,
        folder: str,
        *,
        compress: bool = True,
        retain_data: bool = True,
        remove_original: bool = True,
    ) -> "DataProtocol":
        pass

    @classmethod
    @abstractmethod
    def load(
        cls,
        folder: str,
        *,
        compress: bool = True,
        verbose_level: int = 0,
    ) -> "DataProtocol":
        pass

    @property
    def is_reg(self) -> bool:
        return not self.is_clf

    @property
    def task_type(self) -> TaskTypes:
        if not self.is_ts:
            if self.is_clf:
                return TaskTypes.CLASSIFICATION
            return TaskTypes.REGRESSION
        if self.is_clf:
            return TaskTypes.TIME_SERIES_CLF
        return TaskTypes.TIME_SERIES_REG

    @classmethod
    def get(cls, name: str) -> Type["DataProtocol"]:
        return data_dict[name]

    @classmethod
    def make(cls, name: str, **kwargs: Any) -> "DataProtocol":
        return cls.get(name)(**kwargs)

    @classmethod
    def register(cls, name: str) -> Callable[[Type], Type]:
        global data_dict

        def before(cls_: Type) -> None:
            cls_.__identifier__ = name

        return register_core(name, data_dict, before_register=before)


class SamplerProtocol:
    shuffle: bool

    @abstractmethod
    def __init__(self, data: DataProtocol, **kwargs: Any):
        self.data = data

    @classmethod
    def get(cls, name: str) -> Type["SamplerProtocol"]:
        return sampler_dict[name]

    @classmethod
    def make(cls, name: str, data: DataProtocol, **kwargs: Any) -> "SamplerProtocol":
        return cls.get(name)(data, **kwargs)

    @classmethod
    def register(cls, name: str) -> Callable[[Type], Type]:
        global sampler_dict

        def before(cls_: Type) -> None:
            cls_.__identifier__ = name

        return register_core(name, sampler_dict, before_register=before)


class DataLoaderProtocol:
    _num_siamese: int = 1

    data: DataProtocol
    sampler: SamplerProtocol
    enabled_sampling: bool
    return_indices: bool
    batch_size: int
    _verbose_level: int

    @abstractmethod
    def __init__(
        self,
        batch_size: int,
        sampler: SamplerProtocol,
        *,
        return_indices: bool = False,
        verbose_level: int = 2,
        **kwargs: Any,
    ):
        self.batch_size = batch_size
        self.sampler = sampler
        self.return_indices = return_indices
        self._verbose_level = verbose_level

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __iter__(self) -> "DataLoaderProtocol":
        pass

    @abstractmethod
    def __next__(self) -> batch_type:
        pass

    @abstractmethod
    def copy(self) -> "DataLoaderProtocol":
        pass

    @classmethod
    def get(cls, name: str) -> Type["DataLoaderProtocol"]:
        return loader_dict[name]

    @classmethod
    def make(cls, name: str, *args: Any, **kwargs: Any) -> "DataLoaderProtocol":
        return cls.get(name)(*args, **kwargs)

    @classmethod
    def register(cls, name: str) -> Callable[[Type], Type]:
        global loader_dict

        def before(cls_: Type) -> None:
            cls_.__identifier__ = name

        return register_core(name, loader_dict, before_register=before)


__all__ = [
    "PipelineProtocol",
    "DataSplit",
    "DataProtocol",
    "SamplerProtocol",
    "DataLoaderProtocol",
]
