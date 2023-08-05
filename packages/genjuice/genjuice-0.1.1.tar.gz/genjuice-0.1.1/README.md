# GenJuice

<p align="center">
    <img src="https://img.shields.io/pypi/l/genjuice?style=for-the-badge">
    <img src="https://img.shields.io/pypi/pyversions/genjuice?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/docyx/genjuice?style=for-the-badge">
    <img src="https://img.shields.io/github/issues-raw/docyx/genjuice?style=for-the-badge">
</p>


A lightweight, component-based HTML builder.

```py
from genjuice import Component
from genjuice.components import Button

class FancyButton(Component):
    def render(self):
        return Button("Hello, world!").attr(onclick="alert(1)").render()
```

```py
>>> FancyButton().render()
"""
<button onclick="alert(1)">Hello, world!</button>
"""
```

## Installation

GenJuice isn't quite ready for production yet. Feel free to mess around with it:

```
pip install genjuice
```

## Why GenJuice?

- The core functionality (`Component.render()`) is less than 30 lines long
- On average, it's 2.2x faster than its counterparts (HTML builders/template engines such as Jinja)
- You write your UI code in 100% Python (including CSS!)
- A modern, intuitive API
- ...and much more to come!

## License

[MIT](./LICENSE)
