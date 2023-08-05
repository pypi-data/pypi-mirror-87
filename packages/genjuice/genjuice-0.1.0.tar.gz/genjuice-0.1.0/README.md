# GenJuice

A lightweight, component-based HTML builder

```py
from genjuice import Component
from genjuice.components import Button


class FancyButton(Component):
    def render(self):
        return Button(
            "Hello, world!"
        ).render()
```
