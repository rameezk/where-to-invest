import logging

_log = logging.getLogger(__name__)


class TFSA:
    _total: float

    _yearly_growth: float

    _lifetime_max: float
    _yearly_max: float

    _yearly_contributions: float
    _lifetime_contributions: float

    def __init__(
        self,
        starting_balance=0.00,
        yearly_growth=0.15,
        yearly_contributions: float = 0.00,
        lifetime_contributions: float = 0.00,
    ):
        self._total = starting_balance

        self._yearly_growth = yearly_growth
        self._lifetime_max = 500000
        self._yearly_max = 36000

        self._yearly_contributions = yearly_contributions
        self._lifetime_contributions = lifetime_contributions

    def invest(self, amount: float):
        self._yearly_contributions += amount
        self._lifetime_contributions += amount

        self._total += amount

    def how_much_can_invest(self, amount: float):
        if self._lifetime_contributions + amount > self._lifetime_max:
            _log.debug(
                f"TFSA lifetime limit may be succeeded if you invest {amount:.2f}"
            )
            amount_can_invest = self._lifetime_max - self._lifetime_contributions
            if amount_can_invest < 0:
                amount_can_invest = 0
            return amount_can_invest

        if self._yearly_contributions + amount > self._yearly_max:
            _log.debug(f"TFSA yearly limit may be succeeded if you invest {amount:.2f}")
            amount_can_invest = self._yearly_max - self._yearly_contributions
            if amount_can_invest < 0:
                amount_can_invest = 0
            return amount_can_invest

        return amount

    def grow(self):
        self._total = self._total * (1.00 + (self._yearly_growth / 12))

    def reset_tax_year(self):
        self._yearly_contributions = 0.00

    @property
    def total(self):
        return self._total
