from contextlib import contextmanager
from typing import NoReturn, Type

from ._errors import KOError
from ._inspection_result import active_scope, new_scope
from ._message import debug, _push_indent, _pop_indent


def fail(message: str, error_kind: Type = KOError) -> NoReturn:
    """
    Fail unconditionally

    :param message:             a contextual message providing information about the failure
    :param error_kind:          the type of exception to raise (must be of or inherit from KOError and InternalError)
    """

    raise error_kind(message)


def assert_true(condition: bool, message: str, *, error_kind: Type = KOError):
    """
    Assert that a given condition is True (or raise an exception)

    :param condition:           the condition expected to be True
    :param message:             a contextual message providing information about how / why the assertion failed
    :param error_kind:          the type of exception to raise if the assertion fails (must be of or inherit from KOError and InternalError)
    """

    if not condition:
        fail(message, error_kind=error_kind)


def assert_false(condition: bool, message: str, *, error_kind: Type = KOError):
    """
    Assert that a given condition is False (or raise an exception)

    :param condition:           the condition expected to be False
    :param message:             a contextual message providing information about how / why the assertion failed
    :param error_kind:          the type of exception to raise if the assertion fails (must be of or inherit from KOError and InternalError)
    """

    return assert_true(not condition, message, error_kind=error_kind)


def assert_equal(a, b, message: str, *, error_kind: Type = KOError):
    """
    Assert that ``a == b`` is True (or raise an exception)

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message providing information about how / why the assertion failed
    :param error_kind:          the type of exception to raise if the assertion fails (must be of or inherit from KOError and InternalError)
    """

    return assert_true(a == b, message, error_kind=error_kind)


def assert_not_equal(a, b, message: str, *, error_kind: Type = KOError):
    """
    Assert that ``a != b`` is True (or raise an exception)

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message providing information about how / why the assertion failed
    :param error_kind:          the type of exception to raise if the assertion fails (must be of or inherit from KOError and InternalError)
    """

    return assert_true(a != b, message, error_kind=error_kind)


def assert_greater_than(a, b, message: str, *, error_kind: Type = KOError):
    """
    Assert that ``a > b`` is True (or raise an exception)

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message providing information about how / why the assertion failed
    :param error_kind:          the type of exception to raise if the assertion fails (must be of or inherit from KOError and InternalError)
    """

    return assert_true(a > b, message, error_kind=error_kind)


def assert_greater_or_equal(a, b, message: str, *, error_kind: Type = KOError):
    """
    Assert that ``a >= b`` is True (or raise an exception)

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message providing information about how / why the assertion failed
    :param error_kind:          the type of exception to raise if the assertion fails (must be of or inherit from KOError and InternalError)
    """

    return assert_true(a >= b, message, error_kind=error_kind)


def assert_less_than(a, b, message: str, *, error_kind: Type = KOError):
    """
    Assert that ``a < b`` is True (or raise an exception)

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message providing information about how / why the assertion failed
    :param error_kind:          the type of exception to raise if the assertion fails (must be of or inherit from KOError and InternalError)
    """

    return assert_true(a < b, message, error_kind=error_kind)


def assert_less_or_equal(a, b, message: str, *, error_kind: Type = KOError):
    """
    Assert that ``a <= b`` is True (or raise an exception)

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message providing information about how / why the assertion failed
    :param error_kind:          the type of exception to raise if the assertion fails (must be of or inherit from KOError and InternalError)
    """

    return assert_true(a <= b, message, error_kind=error_kind)


def _add_requirement(condition: bool, message: str):
    debug(f"requirement {'failed' if not condition else 'passed'}: {message}")
    active_scope().add_entry({"requirements": (condition, message)})


def fail_expectation(message: str):
    """
    Fail an expectation unconditionally

    :param message:             a contextual message describing the requirement and (optionally) providing feedback
    """

    _add_requirement(False, message)


def expect_true(condition: bool, message: str) -> bool:
    """
    Expect that a given condition is True to grant a given number of points

    :param condition:           if not True the requirement is considered failed
    :param message:             a contextual message describing the requirement and (optionally) providing feedback
    """

    _add_requirement(condition, message)
    return condition


def expect_false(condition: bool, message: str) -> bool:
    """
    Expect that a given condition is False to grant a given number of points

    :param condition:           if not True the requirement is considered failed
    :param message:             a contextual message describing the expectation and (optionally) providing feedback
    """

    return expect_true(not condition, message)


def expect_equal(a, b, message: str) -> bool:
    """
    Expect that ``a == b`` is True to grant a given number of points

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message describing the expectation and (optionally) providing feedback
    """

    return expect_true(a == b, message)


def expect_not_equal(a, b, message: str) -> bool:
    """
    Expect that ``a != b`` is True to grant a given number of points

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message describing the expectation and (optionally) providing feedback
    """

    return expect_true(a != b, message)


def expect_greater_than(a, b, message: str) -> bool:
    """
    Expect that ``a > b`` is True to grant a given number of points

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message describing the expectation and (optionally) providing feedback
    """

    return expect_true(a > b, message)


def expect_greater_or_equal(a, b, message: str) -> bool:
    """
    Expect that ``a >= b`` is True to grant a given number of points

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message describing the expectation and (optionally) providing feedback
    """

    return expect_true(a >= b, message)


def expect_less_than(a, b, message: str) -> bool:
    """
    Expect that ``a < b`` is True to grant a given number of points

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message describing the expectation and (optionally) providing feedback
    """

    return expect_true(a < b, message)


def expect_less_or_equal(a, b, message: str) -> bool:
    """
    Expect that ``a <= b`` is True to grant a given number of points

    :param a:                   the first object to consider
    :param b:                   the second object to consider
    :param message:             a contextual message describing the requirement and (optionally) providing feedback
    """

    return expect_true(a <= b, message)


@contextmanager
def testing(description: str, *, hidden: bool = False):
    """
    Create a scope to test a given feature

    :param description:         a description of the feature
    :param hidden:              whether or not the scope is marked as hidden
    """
    debug(f"Testing {description}")
    try:
        _push_indent()
        with new_scope(f"Testing {description}", hidden):
            yield
    finally:
        _pop_indent()


@contextmanager
def using(description: str, *, hidden: bool = False):
    """
    Create a scope for a given test case

    :param description:         a description of the test case
    :param hidden:              whether or not the scope is marked as hidden
    """
    debug(f"Using {description}")
    try:
        _push_indent()
        with new_scope(f"Using {description}", hidden):
            yield
    finally:
        _pop_indent()


test_case = using
