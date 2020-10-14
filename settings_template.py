from datetime import (
    date,
)
from decimal import (
    Decimal,
)
from typing import (
    Dict,
)


# Стоимость объекта недвижимости
REALTY_COST: Decimal = Decimal(5_000_000)

#  Первоначальный взнос
INITIAL_INSTALMENT: Decimal = Decimal(1_000_000)

# Срок кредитования. Количество месяцев
CREDIT_PERIOD = 300

# Дата первого платежа. Считается, что дальнейшие платежи будут осуществляться
# в этот же день, например, 15 число каждого месяца
FIRST_PAYMENT_DATE: date = date(2020, 8, 15)

# Процентные ставки с возможным рефинансированием
PERCENTS_RATES: Dict[date, Decimal] = {
    FIRST_PAYMENT_DATE: Decimal(9.1),
    date(2020, 11, 15): Decimal(8.0),
}

# Изменения ежемесячного платежа. Ежемесячный платеж включает в себя
# обязательный платеж по кредиту + средства по досрочному погашению
MONTHLY_PAYMENT_CHANGES: Dict[date, Decimal] = {
    date(2021, 10, 15): Decimal(60_000),
}

# Досрочные погашения. Предполагается, что досрочные погашения в дату
# погашения кредита. Досрочные платеж включает в себя сумму ежемесячного
# платежа, будь то платеж по графику или увеличенный ежемесячный платеж
EARLY_REPAYMENTS: Dict[date, Decimal] = {
    date(2023, 6, 15): Decimal(200_000),
}
