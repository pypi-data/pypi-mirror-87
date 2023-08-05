import pytest

from verspec.infinity import Infinity, NegativeInfinity


def test_infinity_repr():
    repr(Infinity) == "Infinity"


def test_negative_infinity_repr():
    repr(NegativeInfinity) == "-Infinity"


def test_infinity_hash():
    assert hash(Infinity) == hash(Infinity)


def test_negative_infinity_hash():
    assert hash(NegativeInfinity) == hash(NegativeInfinity)


@pytest.mark.parametrize("left", [1, "a", ("b", 4)])
def test_infinity_comparison(left):
    assert left < Infinity
    assert left <= Infinity
    assert not left == Infinity
    assert left != Infinity
    assert not left > Infinity
    assert not left >= Infinity


@pytest.mark.parametrize("left", [1, "a", ("b", 4)])
def test_negative_infinity_lesser(left):
    assert not left < NegativeInfinity
    assert not left <= NegativeInfinity
    assert not left == NegativeInfinity
    assert left != NegativeInfinity
    assert left > NegativeInfinity
    assert left >= NegativeInfinity


def test_infinty_equal():
    assert Infinity == Infinity


def test_negative_infinity_equal():
    assert NegativeInfinity == NegativeInfinity


def test_negate_infinity():
    assert isinstance(-Infinity, type(NegativeInfinity))


def test_negate_negative_infinity():
    assert isinstance(-NegativeInfinity, type(Infinity))
