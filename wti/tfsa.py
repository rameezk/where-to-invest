class TFSA:
    _total: float

    _yearly_growth: float

    _lifetime_max: float
    _yearly_max: float

    _yearly_contributions: float
    _lifetime_contributions: float

    def __init__(self, starting_balance=0.00, yearly_growth=None):
        self._total = starting_balance

        if yearly_growth is None:
            self._yearly_growth = 0.15

        self._lifetime_max = 500000
        self._yearly_max = 36000
        self._yearly_contributions = 0.00
        self._lifetime_contributions = 0.00

    def invest(self, amount: float):
        self._yearly_contributions += amount
        self._lifetime_contributions += amount

        self._total += amount

    def can_invest(self, amount: float):
        if self._lifetime_contributions + amount > self._lifetime_max:
            return False

        if self._yearly_contributions + amount > self._yearly_max:
            return False

        return True

    def grow(self):
        self._total = self._total * (1.00 + (self._yearly_growth / 12))

    def reset_tax_year(self):
        self._yearly_contributions = 0.00

    @property
    def total(self):
        return self._total
