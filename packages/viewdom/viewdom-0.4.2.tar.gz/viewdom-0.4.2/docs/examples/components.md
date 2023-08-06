# Components

You often have a snippet of templating that you'd like to re-use.
Many existing templating systems have "macros" for this: units of templating that can be re-used and called from other templates.

The whole mechanism, though, is quite magical:

- Where do the macros come from?
  Multiple layers of context magic and specially-named directories provide the answer.

- What macros are avaiable at the cursor position I'm at in a template?
  It's hard for an editor or IDE to predict and provide autocomplete.

- What are the macros arguments and what is this template's special syntax for providing them?
  And can my editor help on autocomplete or telling me when I got it wrong (or the macro changed its signature)?

- How does my current scope interact with the macro's scope, and where does it get other parts of its scope from?

`viewdom`, courtesy of `htm.py`, makes this more Pythonic through the use of "components".
Instead of some sorta-callable, a component is a normal Python callable -- e.g. a function -- with normal Python arguments and return values.

## Simple Heading

Here is a callable -- a function -- which returns a VDOM:

```{literalinclude} ../../examples/usage/components.py
---
start-at: from viewdom
end-before: def test
---
```

## Component in VDOM

The VDOM now has something special in it: a callable as the "tag", rather than a string such as ``<div>``.

```{literalinclude} ../../examples/usage/components_vdom.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 8-8
---
```

## Simple Props

As expected, components can have props, passed as what looks like HTML attributes.
Here we pass a `title` as an argument to `Heading`, using a simple HTML attribute string value:

```{literalinclude} ../../examples/usage/componentsB.py
---
start-after: from viewdom
end-before: def test
---
```


## Children As Props

If your template has children inside that tag, your component can ask for them as an argument, then place them as a variable:

```{literalinclude} ../../examples/usage/componentsA.py
---
start-after: from viewdom
end-before: def test
---
```

`children` is a keyword argument that is available to components.
Note how the component closes with `<//>` when it contains nested children, as opposed to the self-closing form in the first example.

## Expressions as Prop Values

The "prop" can also be a Python symbol, using curly braces as the attribute value:

```{literalinclude} ../../examples/usage/componentsC.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 8-8
---
```

## Prop Values from Scope Variables

That prop value can also be an in-scope variable:

```{literalinclude} ../../examples/usage/componentsD.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 8-8
---
```

## Optional Props

Since this is typical function-argument stuff, you can have optional props through argument defaults:

```{literalinclude} ../../examples/usage/componentsE.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 3-3
---
```

## Spread Props

Sometimes you just want to pass everything in a dict as props.
In JS, this is known as the "spread operator" and is supported:

```{literalinclude} ../../examples/usage/spread.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 8-8
---
```

## Pass Component as Prop

Here's a useful pattern: you can pass a component as a "prop" to another component.
This lets the caller -- in this case, the `result` line -- do the driving:

```{literalinclude} ../../examples/usage/componentsPassComponent.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 14-14
---
```

## Default Component for Prop

As a variation, let the caller do the driving but make the prop default to a default component if none was provided:

```{literalinclude} ../../examples/usage/componentsPassComponentB.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 11-11
---
```

## Conditional Default

One final variation: move the "default or passed-in" decision into the template itself:

```{literalinclude} ../../examples/usage/componentsPassComponentC.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 12-12
---
```

## Children as Prop

You can combine different props and arguments.
In this case, `title` is a prop.
`children` is another argument, but is provided automatically by `render`.

```{literalinclude} ../../examples/usage/componentsF.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 3-3
---
```

## Generators as Components

You can also have components that act as generators.
For example, imagine you have a todo list.
There might be a lot of todos, so you want to generate them in a memory-efficient way:

```{literalinclude} ../../examples/usage/componentsG.py
---
start-after: from viewdom
end-before: def test
---
```

## Subcomponents

Subcomponents are also feasible.
They make up part of both the VDOM and the rendering:

```{literalinclude} ../../examples/usage/componentsH.py
---
start-after: from viewdom
end-before: def test
---
```

## Architectural Note

Components and subcomponents are a useful feature to users of some UI layer, as well as creators of that layer.
They are also, though, an interesting architectural plug point.

As `render` walks through a VDOM, a usage of a component pops up with the props and children.
But it isn't yet the *rendered* component.
The callable...hasn't been called.

It's the job of `render` to do so.
If you look at the code for `render` and the utilities it uses, it's not a lot of code.
It's reasonable to write your own, which is what some of the integrations have done.

This becomes an interesting place to experiment with your own component policies.
Want a cache layer?
Want to log each call?
Maybe type validation?
Want to (like the `wired` integration) write a custom DI system that gets argument values from special locations (e.g. database queries)?

Lots of possibilities, especially since the surface area is small enough and easy enough to play around.
