from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from .entities import Order
from .value_objects import Money


class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, order_id: UUID, money: Money) -> bool:
        pass
