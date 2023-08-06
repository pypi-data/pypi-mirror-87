# pear

> A utility for generating variations source code for docmentation.

In documentation you might want to show the growth of a file over time. However, if you want to keep only one copy of the source code. Consider the following file:

```python
class Foo:
    def __init__(self, name):
        self.name = name

    def reverse_name(self):
        return self.name.reverse()
```

If we can to incrementally build the file, we might write the constructor first and `reverse_name` second. That means we would want two versions of the file:

```python
class Foo:
    def __init__(self, name):
        self.name = name
```

```python
class Foo:
    # constructor

    def reverse_name(self):
        return self.name.reverse()
```

Using `pear` you can accomplush this.

## Usage

Include a `pear.json` file in your root directory with the necessary configurations. For our above example, we would have:

```json
{
    "out": "out",
    "files": [
        {
            "path": "foo.py",
            "tag": "without_reverse_name",
            "layers": [
                {
                    "type": "remove",
                    "start": 4,
                    "end": 6
                }
            ]
        },
        {
            "path": "foo.py",
            "tag": "constructor_comment",
            "layers": [
                {
                    "type": "replace",
                    "start": 2,
                    "end": 3,
                    "replacement": [
                        "    # constructor"
                    ]
                }
            ]
        }
    ]
}
```

Then call `pear` from the same directory. This will generate `foo.py_without_reverse_name` and `foo.py_constructor_comment` files in `out/`.
