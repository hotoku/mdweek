from datetime import datetime, date

import pandas as pd
import pytest

from mdweek.week import Week, WeekConfig, setup_week_config


class TestWeekConfig(WeekConfig):
    """
    3/1が第一週となる設定
    """

    def first_date(self, year: int) -> date:
        return date(year, 3, 1)


@pytest.fixture
def df() -> pd.DataFrame:
    return pd.read_csv("tests/resources/calendar2.csv")  # type: ignore


@pytest.fixture
def wc() -> WeekConfig:
    return TestWeekConfig()


def test_fromdate(df: pd.DataFrame, wc: WeekConfig):
    setup_week_config(wc)
    dates = [
        datetime.strptime(s, "%Y-%m-%d").date() for s in df.date
    ]
    for d, y, w in zip(dates, df.year, df.week):
        if y == 2032 and w == 53:  # この範囲のレコードはテスト用データが間違っているので調整
            assert Week.from_date(d) == Week(2031, 53)
        else:
            assert Week.from_date(d) == Week(y, w)


def test_todate(df: pd.DataFrame, wc: WeekConfig):
    setup_week_config(wc)
    weeks = [
        Week(y, w) for y, w in zip(df.year, df.week)
    ]
    dates = [
        datetime.strptime(s, "%Y-%m-%d").date() for s in df.date
    ]
    w203153 = Week(2031, 53)
    for week, dow, dt in zip(weeks, df.dow, dates):
        if week.year == 2032 and week.week == 53:  # この範囲のレコードはテスト用データが間違っているので調整
            assert w203153.date(dow) == dt
        else:
            assert week.date(dow) == dt


def test_add():
    d1 = Week(2020, 1)
    assert d1 + 1 == Week(2020, 2)
    assert d1 + 52 == Week(2020, 53)
    assert d1 + 53 == Week(2021, 1)
    assert d1 + 53 + 51 == Week(2021, 52)
    assert d1 + 53 + 51 + 1 == Week(2022, 1)
    assert d1 - 1 == Week(2019, 52)
    assert d1 - 53 == Week(2018, 52)


def test_sub():
    d1 = Week(2020, 1)
    assert Week(2020, 2) - d1 == 1
    assert Week(2020, 53) - d1 == 52
    assert Week(2021, 1) - d1 == 53
    assert Week(2021, 52) - d1 == 53 + 51
    assert Week(2022, 1) - d1 == 53 + 51 + 1
