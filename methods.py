from datetime import (
    date,
)
from decimal import (
    Decimal,
)
from typing import (
    Dict,
    List,
    Tuple,
    Union,
)

from helpers import (
    get_year_days_count,
)


class CalculateMethod:
    """
    Метод расчета графика платежей по кредиту
    """

    def __init__(
        self,
        realty_cost: Decimal,
        initial_instalment: Decimal,
        first_payment_date: date,
        percents_rate: Decimal,
        credit_period: int,
    ):
        self._realty_cost = realty_cost
        self._initial_instalment = initial_instalment
        self._first_payment_date = first_payment_date
        self._percents_rate = percents_rate
        self._credit_sum = realty_cost - initial_instalment
        self._credit_period = credit_period

        self._result: List[Tuple[Union[str, Decimal], ...]] = []

    @property
    def result(self):
        return self._result

    def calculate(self):
        """
        Метод запуска подсчета графика платежей
        """
        raise NotImplementedError


class AnnuityCalculateMethod(CalculateMethod):
    """
    Аннуитентный метод расчета платежей по кредиту
    """

    def __init__(
        self,
        *args,
        monthly_payment_changes: Dict[date, Decimal],
        early_repayments: Dict[date, Decimal],
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )

        self._monthly_payment_changes = monthly_payment_changes
        self._early_repayments = early_repayments

        self._percent_payment = Decimal()
        self._date_next = None
        self._changed_regular_payment = Decimal()
        self._main_month_main_payment = Decimal()
        self._all_payment = 0

        self._index = Decimal(self._percents_rate / 100 / 12)

    def _calculate_percent_payment(self):
        """
        Расчет суммы процентов кредита за месяц
        """
        if self._first_payment_date.month == 12:
            month_next = 1
            year_next = self._first_payment_date.year + 1
            self._date_next = date(
                year=year_next,
                month=month_next,
                day=self._first_payment_date.day,
            )

            next_year_first_day = date(year_next, 1, 1)
            year_prev_days_count = get_year_days_count(
                year=self._first_payment_date.year,
            )
            year_next_days_count = get_year_days_count(year_next)

            self._percents_payment = Decimal(
                self._credit_sum *
                self._percents_rate * (
                    next_year_first_day - self._first_payment_date
                ).days /
                100 /
                year_prev_days_count +
                self._credit_sum *
                self._percents_rate * (
                    self._date_next - next_year_first_day
                ).days /
                100 /
                year_next_days_count
            )

        else:
            month_next = self._first_payment_date.month + 1
            self._date_next = date(
                year=self._first_payment_date.year,
                month=month_next,
                day=self._first_payment_date.day,
            )
            year_days_count = get_year_days_count(
                year=self._first_payment_date.year,
            )
            self._percents_payment = Decimal(
                self._credit_sum *
                self._percents_rate * Decimal(
                    (self._date_next - self._first_payment_date).days /
                    100 /
                    year_days_count
                )
            )

    def _calculate_month_payment(self):
        """
        Подсчет платежа за месяц
        """
        annuity_payment = Decimal(
            self._credit_sum *
            self._index *
            pow(self._index + 1, self._credit_period) /
            (pow(self._index + 1, self._credit_period) - 1)
        )

        self._calculate_percent_payment()

        if self._date_next in self._monthly_payment_changes:
            self._changed_regular_payment = (
                self._monthly_payment_changes[self._date_next]
            )

        if self._changed_regular_payment:
            self._main_month_main_payment = (
                self._changed_regular_payment - self._percents_payment
            )
        else:
            self._main_month_main_payment = (
                annuity_payment - self._percents_payment
            )

        if self._date_next in self._early_repayments:
            self._main_month_main_payment = (
                self._early_repayments[self._date_next] - self._percents_payment
            )

        self._all_payment = (
            self._all_payment +
            self._main_month_main_payment +
            self._percents_payment
        )

        self._credit_sum -= self._main_month_main_payment

        self._result.append(
            (
                self._date_next.strftime('%b/%d/%Y'),
                annuity_payment,
                self._percents_payment,
                self._main_month_main_payment,
                self._credit_sum,
            )
        )

        self._first_payment_date = self._date_next
        self._credit_period -= 1

    def calculate(self):
        """
        Расчет графика платежей для аннуитентного метода
        """
        for _ in range(self._credit_period):
            self._calculate_month_payment()

            if self._credit_sum <= 0:
                break
