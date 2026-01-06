from typing import Dict, Optional
from uuid import UUID
from domain.entities import Order
from domain.interfaces import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._storage: Dict[UUID, Order] = {}

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        return self._storage.get(order_id)

    def save(self, order: Order) -> None:
        self._storage[order.id] = order

