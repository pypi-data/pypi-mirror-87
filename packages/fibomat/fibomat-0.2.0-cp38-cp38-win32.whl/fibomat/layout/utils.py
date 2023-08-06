from typing import List

from fibomat.shapes import Shape


def _have_same_type(objs: List) -> bool:
    objs_iter = iter(objs)
    first_elem = next(objs_iter)

    if isinstance(first_elem, Shape):
        base = Shape
    else:
        base = type(first_elem)

    return all(isinstance(obj, base) for obj in objs_iter)
