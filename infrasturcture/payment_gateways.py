from uuid import UUID
from domain.interfaces import PaymentGateway
from domain.value_objects import Money


class FakePaymentGateway(PaymentGateway):
    def __init__(self, succeed: bool = True):
        self.succeed = succeed
        self.charges = []

    def charge(self, order_id: UUID, money: Money) -> bool:
        self.charges.append({
            'order_id': order_id,
            'amount': money.amount,
            'currency': money.currency
        })
        return self.succeed

