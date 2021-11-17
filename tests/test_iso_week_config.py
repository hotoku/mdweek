from datetime import date
import pytest

from mdweek.week import IsoWeekConfig


@pytest.fixture
def iwc() -> IsoWeekConfig:
    return IsoWeekConfig()


def test_first_date(iwc: IsoWeekConfig):
    assert iwc.first_date(2020) == date(2020, 1, 2)
    assert iwc.first_date(2021) == date(2021, 1, 7)
