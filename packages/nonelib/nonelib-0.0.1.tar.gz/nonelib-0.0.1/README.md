# Nonelib

Remove None's from data and calls.

### `nonedict()`

```python
>>> from nonelib import nonedict
>>> nonedict(a=1, b=None, c=3)
{'a': 1, 'c':3}
>>> nonedict({'a': 1, 'b': None, 'c':3})
{'a': 1, 'c':3}
```

### `@nonewrap`

```python
>>> from nonelib import nonewrap
>>> @nonewrap
>>> def s(lst, offset=3, limit=3):
...     return lst[offset:offset+limit]
>>> s([1,2,3,4,5,6,7,8,9,10], offset=None, limit=5)  # offset=3 is in effect
[4, 5, 6, 7, 8]
```

### `nonelist()`

```python
>>> from nonelib import nonelist
>>> nonelist([1, None, 3])
[1, 3]
```

### `noneset()`

```python
>>> from nonelib import noneset
>>> noneset({1, None, 3})
{1, 3}
```

### `noneiter()`

```python
>>> from nonelib import noneiter
>>> for x in noneiter([1, None, 3]):
...     print(x)
1
3
```
