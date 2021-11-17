from datetime import date, timedelta
import pytest

from mdweek.week import IsoWeekConfig, Week, WeekCalculator, WeekConfig, setup_week_config


@pytest.fixture
def wc() -> WeekCalculator:
    return WeekCalculator()


class SundayStartConfig(IsoWeekConfig):
    @property
    def first_dow(self) -> int:
        return 7


class TuesdayStartConfig(IsoWeekConfig):
    @property
    def first_dow(self) -> int:
        return 2


def test_move_to_first_day_of_week(wc: WeekCalculator):
    setup_week_config(IsoWeekConfig())
    for d in range(4, 11):
        d = date(2021, 1, d)
        assert date(2021, 1, 4) == wc.move_to_first_day_of_week(d)

    setup_week_config(TuesdayStartConfig())
    for d in range(5, 11):
        d = date(2021, 1, d)
        assert date(2021, 1, 5) == wc.move_to_first_day_of_week(d)

    setup_week_config(SundayStartConfig())
    for d in range(3, 10):
        d = date(2021, 1, d)
        assert date(2021, 1, 3) == wc.move_to_first_day_of_week(d)


def test_move_to_dow(wc: WeekCalculator):
    setup_week_config(IsoWeekConfig())
    for d in range(4, 11):
        assert date(2021, 1, 4) == wc.move_to_dow(date(2021, 1, d), 1)
        assert date(2021, 1, 5) == wc.move_to_dow(date(2021, 1, d), 2)
        assert date(2021, 1, 10) == wc.move_to_dow(date(2021, 1, d), 7)

    setup_week_config(SundayStartConfig())
    for d in range(3, 10):
        assert date(2021, 1, 4) == wc.move_to_dow(date(2021, 1, d), 1)
        assert date(2021, 1, 5) == wc.move_to_dow(date(2021, 1, d), 2)
        assert date(2021, 1, 3) == wc.move_to_dow(date(2021, 1, d), 7)


def test_date(wc: WeekCalculator):
    setup_week_config(IsoWeekConfig())
    for i in range(1, 8):
        d1 = wc.date(Week(2021, 1), i)
        d2 = date(2021, 1, 3) + timedelta(days=i)
        assert d1 == d2


def test_week(wc: WeekCalculator):
    setup_week_config(IsoWeekConfig())
    assert wc.week(date(2021, 1, 3)) == Week(2020, 53)
    assert wc.week(date(2021, 1, 4)) == Week(2021, 1)
