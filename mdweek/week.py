from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
from typing import Union, overload


class WeekCalculation:
    """
    週単位の演算を補助するクラス。
    このクラスの関数の挙動は、_WEEK_CONFIGオブジェクトによってカスタマイズできる。
    """
    @staticmethod
    def parse(s: str) -> Week:
        return _WEEK_CONFIG.parse(s)

    @staticmethod
    def to_str(w: Week) -> str:
        return _WEEK_CONFIG.to_str(w)

    @staticmethod
    def move_to_first_day_of_week(d: datetime.date) -> datetime.date:
        diff = (d.isoweekday() - _WEEK_CONFIG.first_dow) % 7
        return d - datetime.timedelta(days=diff)

    @classmethod
    def move_to_dow(cls, d: datetime.date, target_dow: int) -> datetime.date:
        """
        同じ週の特定の曜日の日付を返す。
        """
        diff = target_dow - d.isoweekday()
        d1 = d + datetime.timedelta(days=diff)
        d2 = cls.move_to_first_day_of_week(d1)
        d3 = cls.move_to_first_day_of_week(d)
        diff2 = d3 - d2
        return d1 + diff2

    @classmethod
    def date(cls, w: Week, dow: int) -> datetime.date:
        """
        w週のdow曜日の日付を返す。
        """
        d1 = _WEEK_CONFIG.first_date(w.year)
        d2 = cls.move_to_dow(d1, _WEEK_CONFIG.first_dow)
        d3 = d2 + datetime.timedelta(days=7 * (w.week - 1))
        return cls.move_to_dow(d3, dow)

    @classmethod
    def week(cls, d: datetime.date) -> Week:
        """
        日付dに対応するWeekを返す。
        """

        # this: 引数の週
        # b: 引数の年の最初の週
        # c: 引数の翌年の最初の週
        # this < b < c
        # b <= this < c
        # b < c <= this 
        # の3パターンがあり得る
        this = cls.move_to_first_day_of_week(d)
        b = cls.move_to_first_day_of_week(_WEEK_CONFIG.first_date(d.year))
        c = cls.move_to_first_day_of_week(_WEEK_CONFIG.first_date(d.year + 1))
        if this < b:
            year = d.year - 1
        elif b <= this < c:
            year = d.year
        else:
            year = d.year + 1

        d2 = _WEEK_CONFIG.first_date(year)
        d3 = cls.move_to_dow(d2, _WEEK_CONFIG.first_dow)
        d4 = cls.move_to_dow(d, _WEEK_CONFIG.first_dow)
        week = (d4 - d3).days // 7
        return Week(year, week + 1)


@dataclass(frozen=True)
class Week:
    year: int
    week: int

    @staticmethod
    def parse(s: str) -> Week:
        return WeekCalculation.parse(s)

    @staticmethod
    def from_date(d: datetime.date) -> Week:
        return WeekCalculation.week(d)

    def date(self, dow: int) -> datetime.date:
        return WeekCalculation.date(self, dow)

    def __str__(self) -> str:
        return WeekCalculation.to_str(self)

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
        sun = WeekCalculation.date(self, 0)
        day = sun + datetime.timedelta(days=7 * n)
        return WeekCalculation.week(day)

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
            s1 = WeekCalculation.date(self, 0)
            s2 = WeekCalculation.date(arg, 0)
            return (s1 - s2).days // 7


class WeekConfig(ABC):
    """
    週の定義をカスタマイズするためのインターフェイスを定義する抽象クラス。
    1. 年間の第一週目を決める日付
    2. 週の始まりの曜日
    を設定できる。
    """
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


"""
週の定義の詳細を保持する変数
"""
_WEEK_CONFIG = IsoWeekConfig()


def setup_week_config(wc: WeekConfig) -> None:
    """
    週の定義のカスタマイズを反映させる関数
    """
    global _WEEK_CONFIG
    _WEEK_CONFIG = wc
