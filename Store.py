from Storage import Storage
from exceptions import NotEnoughSpace, NotEnoughProduct, InvalidProduct, ZeroQuantity, NegativeQuantity


class Store(Storage):
    """
    Parent main class. Inherited from abstract class 'Storage'
    Defines objects of the big warehouse type
    """

    def __init__(self, items: dict[str, int], capacity: int = 100, excess=0):
        """
        Class constructor
        :param items: items located in storage is dict {item, quantity}
        :param capacity: maximum storage capacity
        :param excess: Excess quantity of item to be returned to the sender due to lack of space at the recipient
        """
        self.excess = excess
        self._items = items
        self._capacity = capacity

    def add(self, name: str, quantity: int) -> None:
        """
        Adds items to the storage
        :param name: name of item to be added
        :param quantity: items' quantity
        """
        if not self.get_free_space:
            raise NotEnoughSpace
        elif quantity > self._capacity and self.get_free_space == 0:
            self._items[name] = self._items.get(name, 0) + self._capacity
            self.excess = 0
        elif self.get_free_space > 0:
            if quantity <= self.get_free_space:
                self._items[name] = self._items.get(name, 0) + quantity
                self.excess = 0
            else:
                self.excess = quantity - self.get_free_space
                self._items[name] = self._items.get(name, 0) + self.get_free_space
                print(f'Часть товаров \033[33m{name} ({self.excess} шт)\033[0m не будет отправлено\n'
                      f'потому что у получателя недостаточно места')

    def remove(self, name: str, quantity: int) -> None:
        """
        Removes items from the storage
        :param name: name of item to be removed
        :param quantity: items' quantity
        """
        if name not in self._items.keys():
            raise InvalidProduct
        quantity = self._calc_quantity_limits(name, quantity)
        if not quantity:
            raise ZeroQuantity
        elif quantity < 0:
            raise NegativeQuantity
        print('\nНужное количество товара есть у отправителя')
        self._items[name] = self._items.get(name, 0) - quantity
        if self._items[name] == 0:
            self._items.pop(name)

    @property
    def get_free_space(self) -> int:
        """
        Calculates free space of the storage considering the capacity
        """
        total = 0
        for quantity in self._items.values():
            total += quantity
        return self._capacity - total

    @property
    def get_items(self) -> dict:
        """
        Returns a dict with storage content {item, quantity}
        """
        return self._items

    def _calc_quantity_limits(self, name: str, quantity: int) -> int:
        """
        Calculates the maximum allowable quantity that can be removed from storage
        :param name: name of item
        :param quantity: requested quantity
        """
        current_qnt = self._items[name]
        if current_qnt < quantity:
            raise NotEnoughProduct
        return quantity

    @property
    def get_unique_items_count(self) -> int:
        """
        Calculates total number of items in storage
        """
        return len(self._items.keys())
