# Insert Variables

Inserting a variable into a template mimics what you would expect from a Python f-string.

## Simple Scope

For example, in this case there is only one scope, the global one:

```{literalinclude} ../../examples/usage/variables.py
---
start-at: from viewdom
end-before: def test
---
```

## Local Scope

In this case, the template is in a function, and `name` comes from that scope:

```{literalinclude} ../../examples/usage/variablesA.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 4-4
---
```

## Symbol from `import`

In this third case, `name` is imported from another module:

```{literalinclude} ../../examples/usage/variablesB.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 1-1
---
```

## Symbol from Argument

Of course, the function could get the symbol as an argument.
This style is known as "props":

```{literalinclude} ../../examples/usage/variablesC.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 3-3
---
```

## Prop Defaults

The function could make passing the argument optional by providing a default:

```{literalinclude} ../../examples/usage/variablesD.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 3-3, 8-8
---
```

With this, the calling template doesn't have to provide that prop.

## Conclusion

What's the moral of the story?
No new template rules for variables and scope, just stuff you would expect from Python.
