from datetime import datetime, timedelta

from wti.tfsa import TFSA


class Simulator:
    _age: int

    _year: int
    _year_count: int

    _month_count: int

    _monthly_investment_amount: float

    _total_portfolio: float

    _tfsa: TFSA

    def __init__(self, age: int, monthly_investment_amount: float, year=None):
        if year is None:
            self._year = datetime.now().year

        self._age = age
        self._monthly_investment_amount = monthly_investment_amount
        self._year_count = 0
        self._month_count = 0
        self._total_portfolio = 0.00

        self._tfsa = TFSA()

    def run_one_year(self):
        self.run_months(months=12)

    def run_months(self, months=1):
        for x in range(months):
            self.run_one_month()

    def run_one_month(self):
        self._month_count += 1

        if self._month_count == 12 + 1:
            self._year_count += 1
            self._month_count = 1
            self._tfsa.reset_tax_year()

        self._invest_monthly()
        self._grow_monthly()

    def get_summary(self) -> dict:
        year_delta = self._year + self._year_count
        year = datetime(year=year_delta, month=1, day=1).year
        return {
            "start_year": self._year,
            "year": year,
            "age": self._age + self._year_count,
            "year_count": self._year_count,
            "month_count": self._month_count,
            "total_portfolio": self._total_portfolio,
        }

    def get_total_portfolio(self):
        return self._total_portfolio

    def _invest_monthly(self):
        if self._tfsa.can_invest(self._monthly_investment_amount):
            self._tfsa.invest(self._monthly_investment_amount)
        self._total_portfolio = self._get_total_portfolio_accross_all_vehicles()

    def _grow_monthly(self):
        self._tfsa.grow()
        self._total_portfolio = self._get_total_portfolio_accross_all_vehicles()

    def _get_total_portfolio_accross_all_vehicles(self):
        return self._tfsa.total
