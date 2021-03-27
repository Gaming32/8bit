from importlib import import_module
from typing import Optional


def getattr_recursive(obj: object, attr: str) -> object:
    parts = attr.split('.')
    for part in parts:
        obj = getattr(obj, part)
    return obj


def get_module_object(modname: str, attr: str, package: Optional[str] = None) -> object:
    return getattr_recursive(import_module(modname, package), attr)


def colonimport(path: str) -> object:
    return get_module_object(*path.split(':', 1))
