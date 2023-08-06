import os
import inspect


__all__ = ()


SEPARATOR = '.'


def join(*names):

    return SEPARATOR.join(map(str, names))


def split(qual, *args, **kwargs):

    return qual.rsplit(SEPARATOR, *args, **kwargs)


INIT = '__init__.py'


def get_package_path(directory):

    result = os.path.join(directory, INIT)

    return result


def is_package(path):

    name = os.path.basename(path)

    result = name == INIT

    return result


def get_module_directory(path):

    if is_package(path):
        path = os.path.dirname(path)

    result = os.path.dirname(path)

    return result


def get_module_name(path):

    if is_package(path):
        path = os.path.dirname(path)

    filename = os.path.basename(path)

    (result, extension) = os.path.splitext(filename)

    return result


async def async_noop(*args, **kwargs):
    pass


def execute_before(result, func):

    if inspect.iscoroutine(result):
        coroutine = result
        async def execute():
            result = await coroutine
            func()
            return result
    else:
        def execute():
            func()
            return result

    return execute()
