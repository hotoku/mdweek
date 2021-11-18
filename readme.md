# mdweek

## 概要

ISO Week Numberのような週番号を管理するためのライブラリです。
週番号を定義する際には、

1. 週の始まりを何曜日にするか
1. 各年の第一週を、どこにするか

という点に自由度があり、目的によって様々な定義があり得ます。

このパッケージは、上記のような定義を自由にカスタマイズしながら、
週単位での加減算や差分を計算する機能を提供します。

## インストール

特に依存するライブラリはありません。`pip install mdweek`を実行して下さい。

## 使い方

`WeekConfig`を継承したクラスを定義することで、週の定義がカスタマイズ可能になります。

```python
class SundayMar1Config(WeekConfig):
    """
    - 週の始まりが日曜日
    - 3/1を含む週が第一週
    という定義の週番号を行うためのカスタマイズ用クラス。
    """
    def first_date(self, year):
        return date(year, 3, 1)

    @property
    def first_dow(self, ):
        return 7
```

上記のクラスのインスタンスを引数に、`setup_week_config`を呼び出して下さい。

```python
setup_week_config(SundayMar1Config())
```

これ以降、週番号の計算は、

- 週の始まりが日曜日
- 3/1を含む週が第一週

というポリシーで行われます。

### 日付 → 週の変換

`Week.from_date`関数を使います。これは**staticmethod**です。

```python
for i in range(-10, 10):
    d = date(2021, 3, 1) + timedelta(days=i)
    print(f"{d} -> {Week.from_date(d)}")
```

```
2021-02-19 -> 2020/51
2021-02-20 -> 2020/51
2021-02-21 -> 2020/52
2021-02-22 -> 2020/52
2021-02-23 -> 2020/52
2021-02-24 -> 2020/52
2021-02-25 -> 2020/52
2021-02-26 -> 2020/52
2021-02-27 -> 2020/52
2021-02-28 -> 2021/1
2021-03-01 -> 2021/1
2021-03-02 -> 2021/1
2021-03-03 -> 2021/1
2021-03-04 -> 2021/1
2021-03-05 -> 2021/1
2021-03-06 -> 2021/1
2021-03-07 -> 2021/2
2021-03-08 -> 2021/2
2021-03-09 -> 2021/2
2021-03-10 -> 2021/2
```

### 週, 曜日 → 日付の変換

`Week.date`関数を使います。

```python
week = Week(2021, 1)
for i in range(1, 8):
    print(f"{week} {i} -> {week.date(i)}")
```

```
2021/1 1 -> 2021-03-01 # 月
2021/1 2 -> 2021-03-02 # 火
2021/1 3 -> 2021-03-03 # 水
2021/1 4 -> 2021-03-04 # 木
2021/1 5 -> 2021-03-05 # 金
2021/1 6 -> 2021-03-06 # 土
2021/1 7 -> 2021-02-28 # 日 注意：日曜日始まりの定義なので2/28で正しい
```

### 週と整数の加減算

```python
week2 = Week(2021, 50)

print("引き算")
for i in range(5, 0, -1):
    print(f"{week2} - {i} = {week2 - i}")

print("足し算")
for i in range(1, 5):
    print(f"{week2} + {i} = {week2 + i}")
```

```
引き算
2021/50 - 5 = 2021/45
2021/50 - 4 = 2021/46
2021/50 - 3 = 2021/47
2021/50 - 2 = 2021/48
2021/50 - 1 = 2021/49
足し算
2021/50 + 1 = 2021/51
2021/50 + 2 = 2021/52
2021/50 + 3 = 2022/1
2021/50 + 4 = 2022/2
```

### 週同士の引き算

```python
print(f"1998年30週〜2030年4週は -> {Week(2030, 4) - Week(1998, 30)}週間")
```

```
1998年30週〜2030年4週は -> 1643週間
```
