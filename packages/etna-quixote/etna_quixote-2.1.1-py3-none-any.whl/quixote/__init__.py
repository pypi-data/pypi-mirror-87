from collections import ChainMap
from contextlib import contextmanager
from typing import Any, Mapping, Callable

from .inspection import KOError, InternalError, TimeoutError, CriticalFailureError, BailOutError, active_scope

_context = ChainMap()


def get_context() -> Mapping[str, Any]:
    """
    Retrieve the current build context

    :return:                        a mapping describing the current context
    """
    return _context


@contextmanager
def new_context(**kwargs: Any) -> Mapping[str, Any]:
    """
    Create a new context for the duration of a with-block

    :param kwargs:                  entries to initialize the context with
    :return:                        the context
    """
    global _context
    try:
        _context = _context.new_child(kwargs)
        yield get_context()
    finally:
        _context = _context.parents


class Builder:
    """
    Class wrapping a builder function, along with its configuration
    """

    def __init__(self, wrapped_function, **kwargs):
        self.wrapped_function = wrapped_function
        self.options = kwargs

    def __call__(self, *args, **kwargs):
        return self.wrapped_function(*args, **kwargs)


class Fetcher:
    """
    Class wrapping a fetcher function, along with its configuration
    """

    def __init__(self, wrapped_function, *, cached: bool = True, **kwargs):
        self.wrapped_function = wrapped_function
        self.cached = cached
        self.options = kwargs

    def __call__(self, *args, **kwargs):
        return self.wrapped_function(*args, **kwargs)


class Inspector:
    """
    Class wrapping an inspector function, along with its configuration
    """

    def __init__(
            self, wrapped_function,
            critical: bool = False,
            post_process: Callable[[], None] = None,
            checklist_entry: str = None,
            **kwargs
    ):
        self.wrapped_function = wrapped_function
        self.is_critical = critical
        self.post_process = post_process
        self.checklist_entry = checklist_entry
        self.options = kwargs

    def __call__(self, *args, **kwargs):
        try:
            return self.wrapped_function(*args, **kwargs)
        except BailOutError as e:
            # an error occurred and was already handled (e.g. by an inner scope)
            if self.is_critical:
                raise CriticalFailureError(e)
        except (KOError, InternalError, AssertionError, TimeoutError) as e:
            # an error occurred in the root scope and has yet to be handled
            active_scope().add_entry({"assertion_failure": str(e)})
            if self.is_critical:
                raise CriticalFailureError(e)


_builders = []
_fetchers = []
_inspectors = []


def _reset_registries():
    global _builders
    global _fetchers
    global _inspectors
    _builders = []
    _fetchers = []
    _inspectors = []


@contextmanager
def create_registries():
    """
    Create registries for functions marked as builders, fetchers, and inspectors, for the duration of a with-block

    :return:                        a tuple containing the three registries
    """
    try:
        yield _builders, _fetchers, _inspectors
    finally:
        _reset_registries()


def builder(*args, **kwargs):
    """
    Decorator used to mark a function as a builder
    """
    if len(args) > 0:
        if len(args) != 1:
            raise ValueError("only keyword arguments can be passed to quixote.builder")
        f = args[0]
        _builders.append(Builder(f, **kwargs))
        return f
    else:
        return lambda f: _builders.append(Builder(f, **kwargs))


def fetcher(*args, **kwargs):
    """
    Decorator used to mark a function as a fetcher

    :param cached:                  whether or not the data fetched should be cached (default is False)
    """
    if len(args) > 0:
        if len(args) != 1:
            raise ValueError("only keyword arguments can be passed to quixote.fetcher")
        f = args[0]
        _fetchers.append(Fetcher(f, **kwargs))
        return f
    else:
        return lambda f: _fetchers.append(Fetcher(f, **kwargs))


def inspector(*args, **kwargs):
    """
    Decorator used to mark a function as an inspector

    :param critical:                whether or not the inspection phase should be aborted if this step fails (default is False)
    """
    if len(args) > 0:
        if len(args) != 1:
            raise ValueError("only keyword arguments can be passed to quixote.inspector")
        f = args[0]
        _inspectors.append(Inspector(f, **kwargs))
        return f
    else:
        return lambda f: _inspectors.append(Inspector(f, **kwargs))


class Blueprint:
    """
    Class representing the blueprint of an automated-test job
    """

    def __init__(
            self,
            name: str,
            author: str,
            inspection_file: str = None,
            allow_docker: bool = False,
            metadata: Any = None,
    ):
        """
        Create a blueprint

        :param name:                the name of the blueprint
        :param author:              the author of the blueprint
        :param inspection_file:     the file containing additional inspector functions (deprecated since 2.0)
        :param allow_docker:        whether a docker engine should be made available in the inspection step
        :param metadata:            custom metadata to attach to the blueprint
        """
        self.name = name
        self.author = author
        self.inspection_file = inspection_file
        self.allow_docker = allow_docker
        self.metadata = metadata
        self.builders = []
        self.fetchers = []
        self.inspectors = []

    def register_functions(self, builders=None, fetchers=None, inspectors=None):
        """
        Register functions marked as builders, fetchers, or inspectors in the blueprint

        :param builders:            the list of collected builders
        :param fetchers:            the list of collected fetchers
        :param inspectors:          the list of collected inspectors
        """
        self.builders = builders or []
        self.fetchers = fetchers or []
        self.inspectors = inspectors or []
        return self
