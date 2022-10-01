from abc import ABC, abstractmethod


class Storage(ABC):
    """
    Abstract class of Storage.
    Defines a common interface for child classes
    """

    @abstractmethod
    def add(self, name: str, quantity: int):
        pass

    @abstractmethod
    def remove(self, name: str, quantity: int):
        pass

    @property
    @abstractmethod
    def get_free_space(self) -> int:
        pass

    @abstractmethod
    def get_items(self) -> dict:
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self) -> int:
        pass
