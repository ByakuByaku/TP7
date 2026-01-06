# Лабораторная работа 7: Архитектура, слои и DDD-lite

Реализация системы оплаты заказа с использованием слоистой архитектуры и DDD-lite.

## Структура проекта

- `domain/` - доменная модель и бизнес-правила
  - `entities.py` - сущности Order и OrderLine
  - `value_objects.py` - value object Money
  - `enums.py` - перечисление OrderStatus
  - `interfaces.py` - интерфейсы репозитория и платежного шлюза
- `application/` - use case слой
  - `use_cases.py` - PayOrderUseCase
- `infrastructure/` - реализации интерфейсов
  - `repositories.py` - InMemoryOrderRepository
  - `payment_gateways.py` - FakePaymentGateway
- `tests/` - тесты use case без базы данных
  - `test_use_cases.py` - тесты для PayOrderUseCase и доменной модели

## Реализованные инварианты
- Нельзя оплатить пустой заказ
- Нельзя оплатить заказ повторно
- После оплаты нельзя менять строки заказа
- Итоговая сумма равна сумме строк заказа

## Требования

- Python 3.8+
- pytest

## Запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
