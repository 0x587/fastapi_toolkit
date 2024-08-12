from typing import Type, Union
from pydantic import BaseModel


def is_builtin(t: Type):
    return t in [str, int, float, bool, bytes]


def is_model(t: Type):
    if is_builtin(t):
        return False
    return isinstance(t, type) and BaseModel.__subclasscheck__(t)


def is_optional(t: Type):
    if is_builtin(t):
        return False
    if not hasattr(t, "__origin__"):
        return False
    origin = getattr(t, "__origin__")
    if origin is not Union:
        return False
    if not hasattr(t, "__args__"):
        return False
    args = getattr(t, "__args__")
    if len(args) != 2:
        return False
    if args[1] is not type(None):
        return False
    return True


def is_batch(t: Type):
    if is_builtin(t):
        return False
    if not hasattr(t, "__origin__"):
        return False
    origin = getattr(t, "__origin__")
    if origin is not list:
        return False
    return True


def is_batch_model(t: Type):
    if not is_batch(t):
        return False
    if not hasattr(t, "__args__"):
        return False
    args = getattr(t, "__args__")
    return len(args) == 1 and is_model(args[0])
