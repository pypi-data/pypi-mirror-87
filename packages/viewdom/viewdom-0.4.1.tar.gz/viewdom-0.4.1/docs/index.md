# viewdom: View Layer for Python VDOMs

`viewdom` brings modern frontend templating patterns to Python:

- [tagged](https://github.com/jviide/tagged) to have language-centered templating (like JS tagged templates)
- [htm](https://github.com/jviide/htm.py) to generate virtual DOM structures from a template run (like the `htm` JS package)
- `viewdom` to render a VDOM to a markup string, along with other modern machinery

## Installation

Installation follows the normal Python packaging approach:

```bash
  $ pip install viewdom
```

```{note}
`viewdom` depends on `htm` (which depends on `tagged` which depends on nothing) and `markupsafe`.
```

## Quick Examples

In the ``htm.py`` approach, you generate a VDOM and then convert that to a string.
``viewdom`` does the latter, ``htm.py`` does the former, via a bound ``html`` function in ``viewdom``.
Let's first generate a VDOM:

```{literalinclude} ../examples/index/vdom.py
---
end-before: def test
---
```

This time we'll do both in one line: use `html` to generate a VDOM, then `render` to convert to a string:

```{literalinclude} ../examples/index/render.py
---
start-after: from viewdom
end-before: def test
---
```

If you'd like, you can split those into two steps:

```{literalinclude} ../examples/index/split.py
---
start-after: from viewdom
end-before: def test
---
```

Insert variables from the local or global scope:

```{literalinclude} ../examples/index/scope.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 3-3
---
```

Use HTML attributes as "props" which can have values or even expressions:

```{literalinclude} ../examples/index/props.py
---
start-after: from viewdom
end-before: def test
---
```


Expressions aren't some special language, it's just Python in inside curly braces:

```{literalinclude} ../examples/index/expressions.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 4-4
---
```

Strings with markup get escaped by `markupsafe`:

```{literalinclude} ../examples/index/escaping.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 3-3
---
```

But you can flag a string as safe using `markupsafe.Markup`:

```{literalinclude} ../examples/index/prevent_escaping.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 2-2
---
```

Rendering something conditionally is also "just Python":

```{literalinclude} ../examples/index/conditional.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 8-8
---
```

Looping? Yes, "just Python":

```{literalinclude} ../examples/index/looping.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 9-12
---
```

Reusable components and subcomponents, passing in props and children as arguments:

```{literalinclude} ../examples/index/components.py
---
start-after: from viewdom
end-before: def test
---
```

If your component is a callable instance, ``viewdom`` can detect that and call it:

```{literalinclude} ../examples/index/callable.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 7-8
---
```

Tired of passing props down a deep tree and want something like React context/hooks?

```{literalinclude} ../examples/index/context.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 7-7, 18-18
---
```

## Acknowledgments

The idea and code for `viewdom` -- the rendering, the idea of a theadlocal context, obviously `tagged` and `htm` --- essentially everything -- come from [Joachim Viide](https://github.com/jviide).

```{toctree}
---
hidden: true
---
what
why
how
examples/index
```
