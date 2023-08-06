# Expressions in Templates

In Python f-strings, the curly brackets can take not just variable names, but also Python "expressions".

Same is true in `viewdom`.

## Simple Expression

Let's use an expression which adds two numbers together:

```{literalinclude} ../../examples/usage/expressions.py
---
end-before: def test
---
```

## Python Expression

The expression can do a bit more. For example, call a method on a string to uppercase it:

```{literalinclude} ../../examples/usage/expressionsA.py
---
start-after: from viewdom
end-before: def test
emphasize-lines: 3-3
---
```

## Call a Function from Expression

But it's Python and f-strings-ish, so you can do even more.
For example, call an in-scope function with an argument, which does some work, and insert the result:

```{literalinclude} ../../examples/usage/expressionsB.py
---
start-after: from viewdom
end-before: def test
---
```
