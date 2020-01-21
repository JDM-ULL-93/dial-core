# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Classes for loading datasets.
"""

from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from tensorflow.keras.datasets import boston_housing, cifar10, fashion_mnist, mnist

from dial.datasets import Dataset, datatype
from dial.utils import Timer, log

LOGGER = log.get_logger(__name__)


class DatasetLoader(metaclass=ABCMeta):
    """
    Abstract class for loading any dataset.
    """

    def __init__(
        self,
        name: str,
        brief: str,
        x_type: datatype.DataType,
        y_type: datatype.DataType,
    ):
        self.name = name
        self.brief = brief
        self.x_type = x_type
        self.y_type = y_type

    def load(self) -> Tuple[Dataset, Dataset]:
        """
        Load and return the train/test dataset objects.
        """
        with Timer() as timer:
            (x_train, y_train), (x_test, y_test) = self._load_data()

        LOGGER.info("Fetched dataset data in %s ms", timer.elapsed())

        train_dataset = Dataset(x_train, y_train, self.x_type, self.y_type)
        test_dataset = Dataset(x_test, y_test, self.x_type, self.y_type)

        return train_dataset, test_dataset

    @abstractmethod
    def _load_data(self):
        """
        Return the train/test pairs.
        """

    def __str__(self) -> str:
        return self.name


class MnistLoader(DatasetLoader):
    """
    Mnist dataset loader.
    """

    def __init__(self):
        super().__init__(
            "MNIST",
            "Handwritten digit numbers",
            datatype.ImageArray(),
            datatype.Numeric(),
        )

    def _load_data(self):
        return mnist.load_data()


class FashionMnistLoader(DatasetLoader):
    """
    Fashion Mnist dataset loader.
    """

    def __init__(self):
        super().__init__(
            "Fashion-MNIST",
            "Categorized set of clothing images",
            datatype.ImageArray(),
            datatype.Categorical(),
        )

        self.y_type.categories = [
            "T-shirt/top",
            "Trouser",
            "Pullover",
            "Dress",
            "Coat",
            "Sandal",
            "Shirt",
            "Sneaker",
            "Bag",
            "Ankle boot",
        ]

    def _load_data(self):
        return fashion_mnist.load_data()

    @property
    def categories(self) -> List[str]:
        """
        Return the list of classes identified by Fashion-MNIST
        """
        return self.y_type.categories


class Cifar10Loader(DatasetLoader):
    """
    Cifar10 dataset loader.
    """

    def __init__(self):
        super().__init__(
            "CIFAR10",
            "Categorized images.",
            datatype.ImageArray(),
            datatype.Categorical(),
        )

        self.y_type.categories = [
            "airplane",
            "automobile",
            "bird",
            "cat",
            "deer",
            "dog",
            "frog",
            "horse",
            "ship",
            "truck",
        ]

    def _load_data(self):
        return cifar10.load_data()

    @property
    def categories(self) -> List[str]:
        """
        Return the list of classes identified by CIFAR10
        """
        return self.y_type.categories


class BostonHousingLoader(DatasetLoader):
    """
    Boston Housing dataset loader.
    """

    def __init__(self):
        super().__init__(
            "Boston Housing",
            "Boston House prices.",
            datatype.NumericArray(),
            datatype.Numeric(),
        )

    def _load_data(self):
        return boston_housing.load_data()