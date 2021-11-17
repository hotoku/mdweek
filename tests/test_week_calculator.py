from datetime import date, timedelta
import pytest

from mdweek.week import Week, WeekCalculator


@pytest.fixture
def wc() -> WeekCalculator:
    return WeekCalculator()


def test_move_to_dow(wc: WeekCalculator):
    for d in range(4, 11):
        assert date(2021, 1, 4) == wc.move_to_dow(date(2021, 1, d), 1)
        assert date(2021, 1, 5) == wc.move_to_dow(date(2021, 1, d), 2)

    for d in range(5, 12):
        assert date(2021, 4, 5) == wc.move_to_dow(date(2021, 4, d), 1)
        assert date(2021, 4, 6) == wc.move_to_dow(date(2021, 4, d), 2)
        assert date(2021, 4, 11) == wc.move_to_dow(date(2021, 4, d), 7)


def test_date(wc: WeekCalculator):
    for i in range(1, 8):
        d1 = wc.date(Week(2021, 1), i)
        d2 = date(2021, 1, 3) + timedelta(days=i)
        assert d1 == d2
