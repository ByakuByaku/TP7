class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        if not isinstance(other, Money):
            raise TypeError(f"Cannot add Money to {type(other)}")
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} to {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self):
        return f"{self.amount} {self.currency}"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency