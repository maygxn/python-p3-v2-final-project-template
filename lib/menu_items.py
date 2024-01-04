class Menu:
    def __init__(self,item_number, name, price):
        self.item_number = item_number
        self.name = name
        self.price = price

# ----- Menu CONSTRAINTS------#
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is None:
            raise ValueError("Price cannot be null.")
        elif not isinstance(value,int):
            raise TypeError("Price must be a number.")
        elif value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = value
# ----- Menu CONSTRAINTS------#