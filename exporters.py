from tabulate import (
    tabulate,
)


class PaymentScheduleConsoleExporter:
    """
    Экспортер графика платежей в консоль в виде таблицы
    """

    def __init__(
        self,
        payment_schedule,
    ):
        self._payment_schedule = payment_schedule

        self._headers = (
            'Дата платежа',
            'Аннуетентный платеж',
            'Процентная ставка',
            'Проценты по платежу',
            'Погашение основного долга',
            'Остаток по основному долгу',
        )

    def export(self):
        print(
            tabulate(
                tabular_data=self._payment_schedule,
                headers=self._headers,
                floatfmt='.2f',
            )
        )