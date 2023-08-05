from nose.tools import assert_raises

from zuper_commons.text.zc_wildcards import expand_string, expand_wildcard


def test_wildcards0():
    assert_raises(ValueError, expand_wildcard, "a", ["a"])


def test_wildcards1():
    expand_wildcard("a*", ["a", "b", "ca"])
    assert_raises(ValueError, expand_wildcard, "a*", ["b"])


def test_wildcards2():
    U = ["a", "b", "c1"]
    expand_string(["a", "b", "c*"], U)
    expand_string(["a,b,c*"], U)
