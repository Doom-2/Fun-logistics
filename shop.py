from store import Store


class Shop(Store):
    """
    Child class. Inherited from parent class 'Store'
    Defines objects of small warehouses like shop.
    """

    def __init__(self, items: dict[str, int], capacity: int = 20, excess=0):
        """
        Overrides only default value of the 'capacity' field.
        """
        self._capacity = capacity
        self.excess = excess
        super().__init__(items, capacity, excess)
