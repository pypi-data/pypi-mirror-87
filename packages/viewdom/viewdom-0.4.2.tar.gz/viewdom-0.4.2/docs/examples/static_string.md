# Static Strings

Let's look at some non-dynamic uses of templating to learn the basics.

## No Markup

Let's start with the simplest form of templating: just a string, no tags, no attributes:
For the purposes of illustration, we do the VDOM in one step and the rendering in a second.

```{literalinclude} ../../examples/usage/static_stringLiteral.py
---
end-before: def test
---
```

## Simple Template with Markup

Same thing, but in a `<div>`: nothing dynamic, just "template" a string of HTML, but done in one step:

```{literalinclude} ../../examples/usage/static_string.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 2-2
---
```

We start by importing the `html` function from `viewdom`.
This is, essentially, `htm.py` in action.
It takes a "tagged" template string and returns a VDOM.
The `render` function, imported from `vdom`, does the rendering.

Which we then do to get a result.
The rendered result matches the `expected` value.

## Show VDOM

Let's try that again, looking at the VDOM:

```{literalinclude} ../../examples/usage/static_stringB.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 3-7
---
```

We get back a `VDOM` -- an optimized dataclass -- with:

- The name of the "tag" (`<div>`)

- The properties passed to that tag (in this case, an empty dict)

- The children of this tag (in this case, a text node of `Hello World`)

The second item in the VDOM tuple -- the props dictionary -- now has a key of 'class' with the assigned class name value.

## Expressions

We can go one step further with this and use a little bit of "expressions".
Let's pass in a Python symbol as part of the template, inside curly braces:

```{literalinclude} ../../examples/usage/static_stringC.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 2-2
---
```

Everything is the same, except the value of the `class` prop now has a Python `int` included in the string.
If it looks like Python f-strings, well, that's the point.
We did an expression *inside* that prop value, using a Python expression that evaluated to just the number `1`.

## Shorthand Syntax for Attribute Value

As a shorthand, when the entire attribute value is an expression, you can just use curly braces instead of putting in double quotes:

```{literalinclude} ../../examples/usage/static_stringC2.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 3-3
---
```


The VDOM's third item contains the "children".

## Children

Let's look at what more nesting would look like:

```{literalinclude} ../../examples/usage/static_stringD.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 2-2
---
```

## HTML "collapsed" values

The renderer also knows to collapse truthy-y values into simplified HTML attributes.
Thus, instead of `editable="1"` you just get the attribute *name* without a *value*:

```{literalinclude} ../../examples/usage/static_stringE.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 2-2
---
```

## Doctype

One last point: the HTML doctype is a tricky one to get into the template itself as its syntax is brackety like tags.
Instead, define it as a variable using `markupsafe.Markup` and insert the variable into the template:

```{literalinclude} ../../examples/usage/static_stringDoctype.py
---
start-after: from viewdom
end-before: def test
---
```
