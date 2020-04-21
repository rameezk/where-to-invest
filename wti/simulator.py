from datetime import datetime, timedelta


class Simulator:
    _age: int

    _year: int
    _year_count: int

    _month_count: int

    _monthly_investment_amount: float

    _total_portfolio: float

    def __init__(self, age: int, monthly_investment_amount: float, year=None):
        if year is None:
            self._year = datetime.now().year

        self._age = age
        self._monthly_investment_amount = monthly_investment_amount
        self._year_count = 0
        self._month_count = 0
        self._total_portfolio = 0.00

    def run_one_year(self):
        self._year_count += 1

    def run_one_month(self):
        self._invest_monthly()

        self._month_count += 1

        if self._month_count == 12 + 1:
            self._year_count += 1
            self._month_count = 1

    def get_summary(self) -> dict:
        year_delta = self._year + self._year_count
        year = datetime(year=year_delta, month=1, day=1).year
        return {
            "start_year": self._year,
            "year": year,
            "age": self._age + self._year_count,
            "year_count_from_start": self._year_count,
            "month_count_from_start": self._month_count,
            "total_portfolio": self._total_portfolio,
        }

    def get_total_portfolio(self):
        return self._total_portfolio

    def _invest_monthly(self):
        self._total_portfolio += self._monthly_investment_amount
