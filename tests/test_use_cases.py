import pytest
from uuid import uuid4
from domain.entities import Order, OrderLine
from domain.value_objects import Money
from domain.enums import OrderStatus
from application.use_cases import PayOrderUseCase
from infrasturcture.repositories import InMemoryOrderRepository
from infrasturcture.payment_gateways import FakePaymentGateway


def test_successful_payment():
    # Arrange
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(succeed=True)
    use_case = PayOrderUseCase(repo, gateway)

    order = Order()
    order.add_line(OrderLine(
        product_id=uuid4(),
        product_name="Laptop",
        quantity=1,
        unit_price=Money(1000.0)
    ))
    repo.save(order)

    # Act
    result = use_case.execute(order.id)

    # Assert
    assert result is True
    assert order.status == OrderStatus.PAID
    assert len(gateway.charges) == 1
    assert gateway.charges[0]['amount'] == 1000.0


def test_cannot_pay_empty_order():
    # Arrange
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(succeed=True)
    use_case = PayOrderUseCase(repo, gateway)

    order = Order()  # Пустой заказ
    repo.save(order)

    # Act & Assert
    with pytest.raises(ValueError, match="Cannot pay empty order"):
        use_case.execute(order.id)


def test_cannot_pay_already_paid_order():
    # Arrange
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(succeed=True)
    use_case = PayOrderUseCase(repo, gateway)

    order = Order()
    order.add_line(OrderLine(
        product_id=uuid4(),
        product_name="Mouse",
        quantity=1,
        unit_price=Money(50.0)
    ))
    repo.save(order)

    # Первая оплата
    use_case.execute(order.id)

    # Act & Assert - вторая оплата
    with pytest.raises(ValueError, match="Order is already paid"):
        use_case.execute(order.id)


def test_cannot_modify_after_payment():
    # Arrange
    order = Order()
    order.add_line(OrderLine(
        product_id=uuid4(),
        product_name="Keyboard",
        quantity=1,
        unit_price=Money(100.0)
    ))
    order.pay()

    # Act & Assert
    with pytest.raises(ValueError, match="Cannot modify paid order"):
        order.add_line(OrderLine(
            product_id=uuid4(),
            product_name="Mouse",
            quantity=1,
            unit_price=Money(50.0)
        ))


def test_correct_total_calculation():
    # Arrange
    order = Order()
    order.add_line(OrderLine(
        product_id=uuid4(),
        product_name="Laptop",
        quantity=1,
        unit_price=Money(1000.0)
    ))
    order.add_line(OrderLine(
        product_id=uuid4(),
        product_name="Mouse",
        quantity=2,
        unit_price=Money(50.0)
    ))

    # Act
    total = order.total_amount

    # Assert
    assert total.amount == 1100.0  # 1000 + 2*50
    assert total.currency == "USD"


def test_payment_gateway_failure():
    # Arrange
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(succeed=False)  # Всегда неуспешно
    use_case = PayOrderUseCase(repo, gateway)

    order = Order()
    order.add_line(OrderLine(
        product_id=uuid4(),
        product_name="Laptop",
        quantity=1,
        unit_price=Money(1000.0)
    ))
    repo.save(order)

    # Act
    result = use_case.execute(order.id)

    # Assert
    assert result is False
    assert order.status == OrderStatus.PENDING  # Статус не изменился


if __name__ == "__main__":
    pytest.main([__file__, "-v"])