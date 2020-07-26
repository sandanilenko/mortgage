from exporters import (
    PaymentScheduleConsoleExporter,
)
from methods import (
    AnnuityCalculateMethod,
)
from settings import (
    CREDIT_PERIOD,
    EARLY_REPAYMENTS,
    FIRST_PAYMENT_DATE,
    INITIAL_INSTALMENT,
    MONTHLY_PAYMENT_CHANGES,
    PERCENTS_RATE,
    REALTY_COST,
)


if __name__ == '__main__':
    calculated_method = AnnuityCalculateMethod(
        realty_cost=REALTY_COST,
        initial_instalment=INITIAL_INSTALMENT,
        first_payment_date=FIRST_PAYMENT_DATE,
        percents_rate=PERCENTS_RATE,
        monthly_payment_changes=MONTHLY_PAYMENT_CHANGES,
        early_repayments=EARLY_REPAYMENTS,
        credit_period=CREDIT_PERIOD,
    )

    calculated_method.calculate()

    exporter = PaymentScheduleConsoleExporter(
        payment_schedule=calculated_method.result,
    )
    exporter.export()
