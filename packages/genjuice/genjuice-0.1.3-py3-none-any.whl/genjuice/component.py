from typing import Any, Dict, Union


SELF_CLOSING = (
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
)


class Component:
    def __init__(
        self,
        *slots: Union["Component", str],
        tag_name: str = None,
        attrs: Dict[str, Any] = None,
        inner_html: str = "",
    ):
        self.slots = slots
        self.tag_name = tag_name
        self.attrs = attrs or {}
        self.inner_html = inner_html

    def __repr__(self):
        return f"<Component '{self.__class__.__name__}' attrs={self.attrs}>"

    def proxy(self, other: "Component") -> "Component":
        self.attr(**other.attrs)
        self.inner_html += other.inner_html

        return self

    def attr(self, **attrs) -> "Component":
        self.attrs.update({k: v for k, v in attrs.items() if v})

        return self

    def render(self) -> str:
        if not self.tag_name and self.inner_html:
            return self.inner_html

        if not self.tag_name:
            self.tag_name = "div"

        attrs = ""

        if self.attrs:
            attrs = " " + " ".join(
                ['{}="{}"'.format(k, v) for k, v in self.attrs.items()]
            )

        if self.tag_name in SELF_CLOSING:
            return f"<{self.tag_name}{attrs}>"
        else:
            for slot in self.slots:
                if isinstance(slot, Component):
                    self.inner_html += slot.render()
                else:
                    self.inner_html += slot

            return f"<{self.tag_name}{attrs}>{self.inner_html}</{self.tag_name}>"
