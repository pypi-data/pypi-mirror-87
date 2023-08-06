from __future__ import annotations

import functools
import threading
from collections import ChainMap
from collections.abc import Iterable, ByteString
from dataclasses import dataclass
from inspect import signature, Parameter
from typing import Union, Mapping, List, Callable

from htm import htm_parse, htm_eval
from markupsafe import escape
from tagged import tag

# "void" elements are allowed to be self-closing
# https://html.spec.whatwg.org/multipage/syntax.html#void-elements
VOIDS = (
    'area',
    'base',
    'br',
    'col',
    'embed',
    'hr',
    'img',
    'input',
    'keygen',
    'link',
    'meta',
    'param',
    'source',
    'track',
    'wbr',
)


@dataclass(frozen=True)
class VDOMNode:
    __slots__ = ['tag', 'props', 'children']
    tag: str
    props: Mapping
    children: List[Union[str, VDOMNode]]


VDOM = Union[List[VDOMNode], VDOMNode]


def htm(func=None, *, cache_maxsize=128) -> Callable[[str], VDOM]:
    cached_parse = functools.lru_cache(maxsize=cache_maxsize)(htm_parse)

    def _htm(h):
        @tag
        @functools.wraps(h)
        def __htm(strings, values):
            ops = cached_parse(strings)
            return htm_eval(h, ops, values)

        return __htm

    if func is not None:
        return _htm(func)
    return _htm


html = htm(VDOMNode)


def flatten(value):
    if isinstance(value, Iterable) and not isinstance(
        value, (VDOMNode, str, ByteString)
    ):
        for item in value:
            yield from flatten(item)
    elif callable(value):
        # E.g. a dataclass with an __call__
        vdom = value()
        yield vdom
    else:
        yield value


def relaxed_call(callable_, **kwargs):
    sig = signature(callable_)
    parameters = sig.parameters

    if not any(p.kind == p.VAR_KEYWORD for p in parameters.values()):
        extra_key = "_"
        while extra_key in parameters:
            extra_key += "_"

        sig = sig.replace(
            parameters=[
                *parameters.values(),
                Parameter(extra_key, Parameter.VAR_KEYWORD),
            ]
        )
        kwargs = dict(sig.bind(**kwargs).arguments)
        kwargs.pop(extra_key, None)

    return callable_(**kwargs)


def render(value: VDOM, **kwargs) -> str:
    return "".join(render_gen(Context(value, **kwargs)))


def render_gen(value):
    for item in flatten(value):
        if isinstance(item, VDOMNode):
            tag, props, children = item.tag, item.props, item.children
            if callable(tag):
                yield from render_gen(
                    relaxed_call(tag, children=children, **props)
                )
                continue

            yield f"<{escape(tag)}"
            if props:
                pi = props.items()
                yield f" {' '.join(encode_prop(k, v) for (k, v) in pi)}"

            if children:
                yield ">"
                yield from render_gen(children)
                yield f'</{escape(tag)}>'
            elif tag.lower() in VOIDS:
                yield '/>'
            else:
                yield f'></{tag}>'
        elif item not in (True, False, None):
            yield escape(item)


def encode_prop(k, v):
    if v is True:
        return escape(k)
    return f'{escape(k)}="{escape(v)}"'


_local = threading.local()


def Context(children=None, **kwargs):
    context = getattr(_local, "context", ChainMap())
    try:
        _local.context = context.new_child(kwargs)
        yield children
    finally:
        _local.context = context


def use_context(key, default=None):
    context = getattr(_local, "context", ChainMap())
    return context.get(key, default)
