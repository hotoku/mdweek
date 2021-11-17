from mdweek.week import Week


def test_add():
    d1 = Week(2020, 1)
    assert d1 + 53 == Week(2021, 1)

    assert d1 + 1 == Week(2020, 2)
    assert d1 + 52 == Week(2020, 53)
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
