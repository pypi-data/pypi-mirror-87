from nose.tools import assert_raises, raises

from zuper_commons.types import ZException


@raises(ZException)
def test_exception1():
    raise ZException()


@raises(ZException)
def test_exception2():
    raise ZException("h")


@raises(ZException)
def test_exception3():

    raise ZException("h", a=2)


def test_exception4():
    a = ZException("h", a=2)
    str(a)
    repr(a)


def test_zexception_uses_repr1():
    class A:
        def __str__(self):
            raise ValueError()

    e = ZException("mah", a=A())

    s = str(e)
    print(s)
    assert "!!!" not in s


def test_zexception_uses_repr2():
    class A:
        def __repr__(self):
            raise ValueError()

    e = ZException("mah", a=A())

    s = str(e)

    print(s)
    assert "!!!" in s
