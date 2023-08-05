from nose.tools import assert_equal, assert_raises

from zuper_commons.text import get_md5, get_sha1


def test_hashes1():
    a = get_md5("a\n")
    print(a)
    assert_equal(a, "60b725f10c9c85c70d97880dfe8191b3")


def test_hashes2():
    a = get_md5(b"a\n")
    print(a)
    assert_equal(a, "60b725f10c9c85c70d97880dfe8191b3")


def test_hashes3_no_str():
    assert_raises(ValueError, get_sha1, "a\n")


def test_hashes4():
    a = get_sha1(b"a\n")
    print(a)
    assert_equal(a, "3f786850e387550fdab836ed7e6dc881de23001b")
