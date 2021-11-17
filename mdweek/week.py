from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
import datetime
from typing import Union, overload


@dataclass(frozen=True)
class Week:
    year: int
    week: int

    @staticmethod
    def parse(s: str) -> Week:
        return _WC.parse(s)

    def date(self, dow: int) -> datetime.date:
        return _WC.date(self, dow)

    def __str__(self) -> str:
        return _WC.to_str(self)

    def __lt__(self, other: Week) -> bool:
        if self.year < other.year:
            return True
        if self.year > other.year:
            return False
        return self.week < other.week

    def __gt__(self, other: Week) -> bool:
        if self.year > other.year:
            return True
        if self.year < other.year:
            return False
        return self.week > other.week

    def __le__(self, other: Week) -> bool:
        if self.year < other.year:
            return True
        if self.year > other.year:
            return False
        return self.week <= other.week

    def __ge__(self, other: Week) -> bool:
        if self.year > other.year:
            return True
        if self.year < other.year:
            return False
        return self.week >= other.week

    def __add__(self, n: int) -> Week:
        sun = _WC.date(self, 0)
        day = sun + datetime.timedelta(days=7 * n)
        return _WC.week(day)

    @overload
    def __sub__(self, arg: int) -> Week:
        ...

    @overload
    def __sub__(self, arg: Week) -> int:
        ...

    def __sub__(self, arg: Union[int, Week]):
        if isinstance(arg, int):
            return self + (-arg)
        if isinstance(arg, Week):
            s1 = _WC.date(self, 0)
            s2 = _WC.date(arg, 0)
            return (s1 - s2).days // 7


class WeekConfig(ABC):
    @abstractmethod
    def first_date(self, year: int) -> datetime.date:
        """
        西暦year年の第１週目を決める日付を返す。
        """
        return NotImplemented

    @property
    def first_dow(self) -> int:
        """
        週の始まりが何曜日かを返す。
        曜日の符号は、ISOに準じて、1=月曜日, ... , 7=日曜日とする。
        デフォルトでは、月曜日始まりとしておく。
        """
        return 1

    def parse(self, s: str) -> Week:
        y, w = map(int, s.split("/"))
        return Week(y, w)

    def to_str(self, w: Week) -> str:
        return f"{w.year}/{w.week}"


class IsoWeekConfig(WeekConfig):
    def first_date(self, year: int) -> datetime.date:
        """
        西暦year年の最初の木曜日を返す        
        """
        jan1 = datetime.date(year, 1, 1)
        if jan1.isoweekday() <= 4:
            # year-01-01が月〜木曜日なら、同じ週の木曜日
            return jan1 + datetime.timedelta(days=4 - jan1.isoweekday())
        else:
            # year-01-01が金〜日曜日なら、翌週の木曜日
            return jan1 + datetime.timedelta(days=7 + 4 - jan1.isoweekday())


class WeekCalculator:
    def parse(self, s: str) -> Week:
        return _WEEK_CONFIG.parse(s)

    def to_str(self, w: Week) -> str:
        return _WEEK_CONFIG.to_str(w)

    def move_to_dow(self, d: datetime.date, target_dow: int) -> datetime.date:
        """
        同じ週の特定の曜日の日付を返す。
        """
        old_dow = d.isoweekday()
        first_dow = _WEEK_CONFIG.first_dow

        diff1 = first_dow - old_dow
        d1 = d + datetime.timedelta(days=diff1)

        diff2 = target_dow - first_dow
        d2 = d1 + datetime.timedelta(days=diff2)

        return d2

    def date(self, w: Week, dow: int) -> datetime.date:
        """
        w週のdow曜日の日付を返す。
        """
        d1 = _WEEK_CONFIG.first_date(w.year)
        d2 = self.move_to_dow(d1, _WEEK_CONFIG.first_dow)
        d3 = d2 + datetime.timedelta(days=7 * (w.week - 1))
        return self.move_to_dow(d3, dow)

    def week(self, d: datetime.date) -> Week:
        """
        日付dに対応するWeekを返す。
        """
        d1 = _WEEK_CONFIG.first_date(d.year)
        d12 = self.move_to_dow(d1, _WEEK_CONFIG.first_dow)
        d13 = self.move_to_dow(d, _WEEK_CONFIG.first_dow)
        if d13 >= d12:
            year = d.year
        else:
            year = d.year - 1
        d2 = _WEEK_CONFIG.first_date(year)
        d3 = self.move_to_dow(d2, _WEEK_CONFIG.first_dow)
        d4 = self.move_to_dow(d, _WEEK_CONFIG.first_dow)
        week = (d4 - d3).days // 7
        return Week(year, week + 1)


_WC: WeekCalculator = WeekCalculator()
_WEEK_CONFIG = IsoWeekConfig()


def setup_week_config(wc: WeekConfig) -> None:
    global _WEEK_CONFIG
    _WEEK_CONFIG = wc
