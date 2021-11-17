from __future__ import annotations
from abc import ABC, abstractmethod
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


class WeekCalculator(ABC):
    @abstractmethod
    def parse(self, s: str) -> Week:
        return NotImplemented

    @abstractmethod
    def to_str(self, w: Week) -> str:
        return NotImplemented

    @abstractmethod
    def date(self, w: Week, n: int) -> datetime.date:
        """
        その週の特定の曜日を返す。
        曜日とintの対応は、ISOに準じる。
        1 = 月曜日, ... , 6 = 土曜日, 7 = 日曜日
        """
        return NotImplemented

    @abstractmethod
    def week(self, d: datetime.date) -> Week:
        return NotImplemented


class IsoWeekCalculator(WeekCalculator):
    def parse(self, s: str) -> Week:
        y, w = s.split("/")
        return Week(int(y), int(w))

    def to_str(self, w: Week) -> str:
        return f"{w.year}/{w.week}"

    def date(self, w: Week, n: int) -> datetime.date:
        if n == 0:
            n = 7
        ret = datetime.datetime.fromisocalendar(w.year, w.week, n)
        return ret.date()

    def week(self, d: datetime.date) -> Week:
        d2 = datetime.datetime(d.year, d.month, d.day)
        iso = d2.isocalendar()
        return Week(iso.year, iso.week)


_WC: WeekCalculator = IsoWeekCalculator()


def setup_week_calculator(wc: WeekCalculator) -> None:
    global _WC
    _WC = wc
