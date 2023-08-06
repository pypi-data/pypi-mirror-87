Changelog
=========

Unreleased
==========

- Allow VDOM to contain any kind of sequence

0.4.1
=====

- Change typing: ``VDOM`` is now the list/node at the top, ``VDOMNode`` is the factory and an individual triple

- Re-organize the examples

0.4.0
=====

- Switch to a dataclass (frozen, slots) data structure for VDOMs, making it easy to assign type hints, do autocomplete, and have mypy get involved.

- Add more examples and docs

0.3.0
=====

- Allow callable subcomponents, e.g. dataclasses with an ``__call__``, to be rendered in ``html()`` calls

0.2.0
=====

- Switch docs to ``sphinx-book-theme`` and MyST

- Publish to PyPI

0.1.0
=====

- First release.
