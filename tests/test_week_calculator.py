from datetime import date, timedelta

from mdweek.week import (
    IsoWeekConfig,
    Week,
    WeekConfig,
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

class SundayJan1Config(WeekConfig):
    @property
    def first_dow(self) -> int:
        return 7

    def first_date(self, year: int) -> date:
        return date(year, 1, 1)

class MondayDec31Config(WeekConfig):
    def first_date(self, year: int) -> date:
        return date(year, 12, 31)

class SundayDec31Config(WeekConfig):
    def first_date(self, year: int) -> date:
        return date(year, 12, 31)

    @property
    def first_dow(self) -> int:
        return 7

def test_move_to_first_day_of_week():
    setup_week_config(IsoWeekConfig())
    for d in range(4, 11):
        d = date(2021, 1, d)
        assert date(2021, 1, 4) == wc.move_to_first_day_of_week(d), d

    setup_week_config(TuesdayStartConfig())
    for d in range(5, 11):
        d = date(2021, 1, d)
        assert date(2021, 1, 5) == wc.move_to_first_day_of_week(d), d

    setup_week_config(SundayStartConfig())
    for d in range(3, 10):
        d = date(2021, 1, d)
        assert date(2021, 1, 3) == wc.move_to_first_day_of_week(d), d


def test_move_to_dow():
    base = date(2021, 1, 6)
    setup_week_config(IsoWeekConfig())
    for i in range(1, 8):
        assert wc.move_to_dow(base, i) == date(2021, 1, 3 + i), i

    setup_week_config(SundayStartConfig())
    for i in range(1, 8):
        assert wc.move_to_dow(base, i) == date(2021, 1, 3 + (i % 7)), i

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
        assert d == date(2021, 1, 3 + i), i

    setup_week_config(SundayStartConfig())
    for i in range(1, 8):
        d = wc.date(week, i)
        assert d == date(2021, 1, 3 + (i % 7)), i

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

def test_week2():
    setup_week_config(SundayJan1Config())
    base = date(2020, 12, 27)
    for i in range(7):
        assert wc.week(base + timedelta(days=i)) == Week(2021, 1), i
    for i in range(7, 14):
        assert wc.week(base + timedelta(days=i)) == Week(2021, 2), i

def test_week3():
    setup_week_config(MondayDec31Config())
    base = date(2020, 12, 28)
    for i in range(-7, 0):
        assert wc.week(base + timedelta(days=i)) == Week(2019, 52), i
    for i in range(7):
        assert wc.week(base + timedelta(days=i)) == Week(2020, 1), i
    for i in range(7, 14):
        assert wc.week(base + timedelta(days=i)) == Week(2020, 2), i

def test_week4():
    setup_week_config(SundayDec31Config())
    base = date(2020, 12, 27)
    for i in range(-7, 0):
        assert wc.week(base + timedelta(days=i)) == Week(2019, 52), i
    for i in range(7):
        assert wc.week(base + timedelta(days=i)) == Week(2020, 1), i
    for i in range(7, 14):
        assert wc.week(base + timedelta(days=i)) == Week(2020, 2), i
        
