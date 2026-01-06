from uuid import UUID, uuid4
from typing import List
from .enums import OrderStatus
from .value_objects import Money


class OrderLine:
    def __init__(self, product_id: UUID, product_name: str, quantity: int, unit_price: Money):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def total_price(self) -> Money:
        return Money(self.unit_price.amount * self.quantity, self.unit_price.currency)


class Order:
    def __init__(self, id: UUID = None, customer_id: UUID = None):
        self.id = id or uuid4()
        self.customer_id = customer_id
        self._lines: List[OrderLine] = []
        self.status = OrderStatus.PENDING

    @property
    def lines(self) -> List[OrderLine]:
        return list(self._lines)

    @property
    def total_amount(self) -> Money:
        if not self._lines:
            return Money(0.0)

        total = self._lines[0].total_price
        for line in self._lines[1:]:
            total += line.total_price
        return total

    def add_line(self, line: OrderLine) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self._lines.append(line)

    def pay(self) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Order is already paid")

        if not self._lines:
            raise ValueError("Cannot pay empty order")

        self.status = OrderStatus.PAID