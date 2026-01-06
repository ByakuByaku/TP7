from uuid import uuid4
from domain.entities import Order, OrderLine
from domain.value_objects import Money
from application.use_cases import PayOrderUseCase
from infrasturcture.payment_gateways import FakePaymentGateway
from infrasturcture.repositories import InMemoryOrderRepository


def main():
    print("=== Система оплаты заказов ===\n")

    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(succeed=True)
    use_case = PayOrderUseCase(repo, gateway)

    print("1. Создаем заказ...")
    order = Order(customer_id=uuid4())
    order.add_line(OrderLine(
        product_id=uuid4(),
        product_name="Ноутбук",
        quantity=1,
        unit_price=Money(1000.0)
    ))
    order.add_line(OrderLine(
        product_id=uuid4(),
        product_name="Мышь",
        quantity=2,
        unit_price=Money(50.0)
    ))
    order.add_line(OrderLine(
        product_id=uuid4(),
        product_name="Клавиатура",
        quantity=1,
        unit_price=Money(100.0)
    ))

    repo.save(order)

    print(f"   ID заказа: {order.id}")
    print(f"   Товаров в заказе: {len(order.lines)}")
    print(f"   Общая сумма: {order.total_amount}")
    print(f"   Статус: {order.status.value}\n")

    print("2. Оплачиваем заказ...")
    try:
        success = use_case.execute(order.id)
        if success:
            print("   ✅ Оплата прошла успешно!")
        else:
            print("   ❌ Оплата не удалась")
    except ValueError as e:
        print(f"   ❌ Ошибка: {e}")

    print(f"   Статус после оплаты: {order.status.value}\n")

    print("3. Пробуем оплатить еще раз...")
    try:
        success = use_case.execute(order.id)
        if success:
            print("   ✅ Оплата прошла успешно!")
        else:
            print("   ❌ Оплата не удалась")
    except ValueError as e:
        print(f"   ❌ Ошибка: {e}")

    print(f"\n4. Платежи в шлюзе: {gateway.charges}")


if __name__ == "__main__":
    main()