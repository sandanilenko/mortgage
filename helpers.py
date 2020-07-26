import calendar


def get_year_days_count(year):
    """
    Выдает количество дней в зависимости от того, является год високосным или
    нет
    """
    return 366 if calendar.isleap(year) else 365
