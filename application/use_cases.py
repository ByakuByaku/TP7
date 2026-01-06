from uuid import UUID
from domain.interfaces import OrderRepository, PaymentGateway


class PayOrderUseCase:
    def __init__(self, order_repository: OrderRepository, payment_gateway: PaymentGateway):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway

    def execute(self, order_id: UUID) -> bool:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")

        order.pay()

        success = self.payment_gateway.charge(order_id, order.total_amount)

        if success:
            self.order_repository.save(order)

        return success