from datetime import datetime
import logging

from wti.tfsa import TFSA
from wti.discretionary import Discretionary
import wti.conf as conf

_log = logging.getLogger(__name__)


class Simulator:
    _age: int

    _year: int
    _year_count: int

    _month_count: int

    _monthly_investment_amount: float

    _total_portfolio: float

    _tfsa: TFSA
    _discretionary: Discretionary

    def __init__(self, age: int, monthly_investment_amount: float, year=None):
        if year is None:
            self._year = datetime.now().year

        self._age = age
        self._monthly_investment_amount = monthly_investment_amount
        self._year_count = 0
        self._month_count = 0
        self._total_portfolio = 0.00

        self._tfsa = TFSA(
            starting_balance=conf.tfsa_starting_balance,
            yearly_growth=conf.tfsa_growth,
            yearly_contributions=conf.tfsa_yearly_contributions,
            lifetime_contributions=conf.tfsa_lifetime_contributions,
        )
        self._discretionary = Discretionary(
            "offshore", yearly_growth=conf.discretionary_growth
        )

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
            self._age += 1
            self._tfsa.reset_tax_year()
            self._escalate_monthly_investment_amount()

        _log.debug(
            f"Running simulation for year = {self._year_count} month = {self._month_count}"
        )
        self._invest_monthly()
        self._grow_monthly()

    def run_until_portfolio_is(self, amount: float):
        while self._total_portfolio < amount:
            self.run_one_month()

        return {
            "year": self._year_count,
            "month": self._month_count,
            "age": self._age,
            "porfolio": {
                "total": self._total_portfolio,
                "tfsa": self._tfsa.total,
                "offshore": self._discretionary.total,
            },
        }

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

    def _escalate_monthly_investment_amount(self):
        self._monthly_investment_amount = self._monthly_investment_amount * (
            1 + conf.yearly_investment_amount_escalation
        )
        _log.debug(
            f"Monthly investment amount has been increased to {self._monthly_investment_amount:.2f}"
        )

    def _invest_monthly(self):
        amount_can_invest = self._tfsa.how_much_can_invest(
            self._monthly_investment_amount
        )
        _log.debug(f"Can invest {amount_can_invest:.2f} into TFSA this month")
        if amount_can_invest > 0.00:
            self._tfsa.invest(amount_can_invest)

        remaining_amount_to_invest = self._monthly_investment_amount - amount_can_invest
        if remaining_amount_to_invest > 0.00:
            _log.debug(
                f"Funds remaining = {remaining_amount_to_invest:.2f}. Will need to allocate to another vehicle."
            )
            self._discretionary.invest(remaining_amount_to_invest)

        self._total_portfolio = self._get_total_portfolio_across_all_vehicles()

    def _grow_monthly(self):
        self._tfsa.grow()
        self._discretionary.grow()
        self._total_portfolio = self._get_total_portfolio_across_all_vehicles()

    def _get_total_portfolio_across_all_vehicles(self):
        return self._tfsa.total + self._discretionary.total

    @property
    def portfolio(self) -> dict:
        return {
            "tfsa": {"balance": self._tfsa.total},
            "offshore": {"balance": self._discretionary.total},
        }
