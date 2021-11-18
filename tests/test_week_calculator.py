from datetime import date

from mdweek.week import (
    IsoWeekConfig,
    Week,
    setup_week_config,
    WeekCalculation as wc
)




class SundayStartConfig(IsoWeekConfig):
    @property
    def first_dow(self) -> int:
        return 7


class TuesdayStartConfig(IsoWeekConfig):
    @property
    def first_dow(self) -> int:
        return 2


def test_move_to_first_day_of_week():
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


def test_move_to_dow():
    base = date(2021, 1, 6)
    setup_week_config(IsoWeekConfig())
    for i in range(1, 8):
        assert wc.move_to_dow(base, i) == date(2021, 1, 3 + i)

    setup_week_config(SundayStartConfig())
    for i in range(1, 8):
        assert wc.move_to_dow(base, i) == date(2021, 1, 3 + (i % 7))

    setup_week_config(TuesdayStartConfig())
    assert wc.move_to_dow(base, 1) == date(2021, 1, 11)
    assert wc.move_to_dow(base, 2) == date(2021, 1, 5)
    assert wc.move_to_dow(base, 3) == date(2021, 1, 6)
    assert wc.move_to_dow(base, 4) == date(2021, 1, 7)
    assert wc.move_to_dow(base, 5) == date(2021, 1, 8)
    assert wc.move_to_dow(base, 6) == date(2021, 1, 9)
    assert wc.move_to_dow(base, 7) == date(2021, 1, 10)


def test_date():
    week = Week(2021, 1)

    setup_week_config(IsoWeekConfig())
    for i in range(1, 8):
        d = wc.date(week, i)
        assert d == date(2021, 1, 3 + i)

    setup_week_config(SundayStartConfig())
    for i in range(1, 8):
        d = wc.date(week, i)
        assert d == date(2021, 1, 3 + (i % 7))

    setup_week_config(TuesdayStartConfig())
    assert wc.date(week, 1) == date(2021, 1, 11)
    assert wc.date(week, 2) == date(2021, 1, 5)
    assert wc.date(week, 3) == date(2021, 1, 6)
    assert wc.date(week, 4) == date(2021, 1, 7)
    assert wc.date(week, 5) == date(2021, 1, 8)
    assert wc.date(week, 6) == date(2021, 1, 9)
    assert wc.date(week, 7) == date(2021, 1, 10)


def test_week():
    setup_week_config(IsoWeekConfig())
    assert wc.week(date(2021, 1, 3)) == Week(2020, 53)
    assert wc.week(date(2021, 1, 4)) == Week(2021, 1)

    setup_week_config(SundayStartConfig())
    assert wc.week(date(2021, 1, 2)) == Week(2020, 53)
    assert wc.week(date(2021, 1, 3)) == Week(2021, 1)
    assert wc.week(date(2021, 1, 4)) == Week(2021, 1)

    setup_week_config(TuesdayStartConfig())
    assert wc.week(date(2021, 1, 2)) == Week(2020, 53)
    assert wc.week(date(2021, 1, 3)) == Week(2020, 53)
    assert wc.week(date(2021, 1, 4)) == Week(2020, 53)
    assert wc.week(date(2021, 1, 5)) == Week(2021, 1)
