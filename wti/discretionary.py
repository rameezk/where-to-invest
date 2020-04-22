class Discretionary:
    _name: str
    _total: float
    _contributions: float
    _yearly_growth: float

    def __init__(
        self,
        name: str,
        starting_balance=0.00,
        yearly_growth=0.15,
        contributions: float = 0.00,
    ):
        self._name = name
        self._total = starting_balance
        self._yearly_growth = yearly_growth
        self._contributions = contributions

    def invest(self, amount: float):
        self._contributions += amount
        self._total += amount

    def grow(self):
        self._total = self._total * (1.00 + (self._yearly_growth / 12))

    @property
    def total(self):
        return self._total

    @property
    def name(self):
        return self.name
