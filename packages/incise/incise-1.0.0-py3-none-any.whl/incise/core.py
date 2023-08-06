import os
import sys
import inspect
import importlib
import collections
import itertools

from . import helpers


__all__ = ('origin', 'load', 'drop')


_modules = []


def _voyance():

    stack = inspect.stack()

    for info in stack:
        space = info.frame.f_globals
        for module in _modules:
            if not space is module.__dict__:
                continue
            break
        else:
            continue
        yield module


def _origin(limit):

    generate = _voyance()

    while not limit < 0:
        try:
            result = next(generate)
        except StopIteration:
            raise ModuleNotFoundError('missing loaded module') from None
        limit -= 1

    return result


def origin():

    """
    Return the loaded module of the function this is called in.
    """

    result = _origin(1)

    return result


_uniques = collections.defaultdict(itertools.count)


_source = helpers.join(__name__, '_')


def _analyze(path, core = 'core', extension = '.py'):

    try:
        parent = _origin(0)
    except ModuleNotFoundError:
        parent = None
    else:
        subpath = parent.__file__
        directory = helpers.get_module_directory(subpath)
        path = os.path.join(directory, path)

    entry = helpers.get_package_path(path)

    if os.path.isdir(path):
        entry = helpers.get_package_path(path)
        if not os.path.exists(entry):
            return _analyze(os.path.join(path, core))
        path = entry

    if not os.path.exists(path):
        path = path + extension

    name = helpers.get_module_name(path)

    return (parent, path, name)


def load(path):

    """
    Import a module and call its ``load`` function if it exists.

    .. note::

        - If no extension is provided ``.py`` is used.
        - Packages are valid targets and relative imports are allowed.
        - Calling in another loaded module prepends the current directory.
        - Targeting non-package directories uses their ``core`` entry.

    Calling this multiple times with the same arguments will load different
    modules.

    Returns the result of the ``load`` function or a no-op coroutine.
    """

    (parent, path, name) = _analyze(path)

    source = parent.__name__ if parent else _source

    unique = next(_uniques[parent])

    name = helpers.join(source, unique, name)

    spec = importlib.util.spec_from_file_location(name, path)

    module = importlib.util.module_from_spec(spec)

    _modules.append(module)

    sys.modules[module.__name__] = module

    module.__loader__.exec_module(module)

    try:
        func = module.load
    except AttributeError:
        func = helpers.async_noop

    result = func()

    return result


def drop(path, limit = 0):

    """
    Forget a module after calling its ``drop`` function.

    Uses the same target methods as in :func:`load`. Only works for modules
    imported through there.

    If multiple modules of the same info have been loaded, they are targetted by
    loading order.

    Returns the result of the ``drop`` function or a no-op coroutine.
    """

    (parent, path, name) = _analyze(path)

    source = parent.__name__ if parent else _source

    for module in _modules:
        (msource, _, mname) = helpers.split(module.__name__, 2)
        if not (msource == source and mname == name):
            continue
        if not limit:
            break
        limit -= 1
    else:
        raise ModuleNotFoundError(path)

    try:
        func = module.drop
    except AttributeError:
        func = helpers.async_noop

    def cleanup():
        for key in tuple(sys.modules):
            if not key.startswith(module.__name__):
                continue
            del sys.modules[key]
        del _uniques[module]
        # we can't use index as the module's `drop` may
        # subsequently rid others, invalidating indexes
        _modules.remove(module)

    result = func()

    result = helpers.execute_before(result, cleanup)

    return result
