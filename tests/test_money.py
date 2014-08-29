import copy
import pickle
from decimal import Decimal

from mock import patch

from easymoney import Money


def test_create():
    assert Money(3) == Decimal('3')

    assert Money(3.14) == Decimal('3.14')
    assert Money(3.141) == Decimal('3.14')
    assert Money(3.145) == Decimal('3.15')

    assert Money('3.14') == Decimal('3.14')
    assert Money('3.141') == Decimal('3.14')
    assert Money('3.145') == Decimal('3.15')

    assert Money(Decimal('3.14')) == Decimal('3.14')
    assert Money(Decimal('3.141')) == Decimal('3.14')
    assert Money(Decimal('3.145')) == Decimal('3.15')


def test_str():
    assert str(Money(3.14)) == '$3.14'
    assert str(Money(3)) == '$3.00'
    with patch('easymoney.CURRENCY_CODE', 'EUR'):
        assert str(Money(3.14)) == '\xe2\x82\xac3.14'
        assert str(Money(3)) == '\xe2\x82\xac3.00'


def test_arithmetic():
    pi = Money(3.14)
    e = Money(2.78)

    # NOTE: we test this way to check that bools are returned
    assert (pi == 3.14) is True
    assert (pi == Decimal('3.14')) is True
    assert (pi == 3) is False
    assert (pi != 3) is True
    assert (Money(3) == 3) is True

    assert (3 == pi) is False
    assert (3 != pi) is True

    assert pi + e == 5.92
    assert pi - e == 0.36


def test_precision():
    assert Money(1000) * 1.001 == 1001


def test_int_arithmetic():
    pi = Money(3.14)

    assert pi + 1 == 4.14
    assert pi - 1 == 2.14
    assert pi * 2 == 6.28
    assert pi / 3 == 1.05

    assert 1 + pi == 4.14
    assert 1 - pi == -2.14
    assert 2 * pi == 6.28
    assert 9 / pi == 2.87


def test_float_arithmetic():
    pi = Money(3.14)

    assert pi + 0.2 == 3.34
    assert pi - 0.2 == 2.94
    assert pi * 0.2 == 0.63
    assert pi / 1.5 == 2.09

    # We coerse to 2 digits before operation
    assert pi + 0.005 == 3.15
    assert pi - 0.005 == 3.13


def test_copy():
    pi = Money(3.14)
    assert pi == copy.copy(pi)
    assert pi == copy.deepcopy(pi)


def test_pickle():
    pi = Money(3.14)
    assert pickle.loads(pickle.dumps(pi)) == pi
    assert pickle.loads(pickle.dumps(pi, -1)) == pi
