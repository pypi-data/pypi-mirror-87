import bleach
from typing import Any, Dict
from .util import style_to_dict, dict_to_style


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
        *slots: "Component",
        tag_name: str = None,
        attrs: Dict[str, Any] = None,
        inner_html: str = "",
    ):
        self.styles = {}
        self.slots = slots

        self.tag_name = tag_name
        self.attrs = attrs or {}
        self.inner_html = inner_html

    def __repr__(self) -> str:
        return f"<Component '{self.__class__.__name__}'>"

    def proxy(self, other: "Component") -> "Component":
        self.style(**other.styles)
        self.attr(**other.attrs)
        self.inner_html += other.inner_html

        return self

    def style(self, **styles) -> "Component":
        self.styles.update({k: v for k, v in styles if v})

        return self

    def attr(self, **attrs) -> "Component":
        self.attrs.update({k: v for k, v in attrs if v})

        return self

    def safe_insert(self, insert: str) -> "Component":
        self.inner_html += bleach.clean(insert)

        return self

    def render(self) -> str:
        if not self.tag_name and self.inner_html:
            return self.inner_html

        if not self.tag_name:
            self.tag_name = "div"

        attrs = ""
        styles = {}
        style_attr = {}

        if self.styles or self.attrs.get("styles"):
            styles = {**self.styles, **style_to_dict(self.attrs.get("style"))}
            style_attr = {"style": dict_to_style(styles)}

        if self.attrs or self.styles:
            attrs = " " + " ".join(
                [
                    '{}="{}"'.format(k, v)
                    for k, v in {**self.attrs, **style_attr}.items()
                ]
            )

        if self.tag_name in SELF_CLOSING:
            return f"<{self.tag_name}{attrs}>"
        else:
            self.inner_html += "".join([c.render() for c in self.slots])

            return f"<{self.tag_name}{attrs}>{self.inner_html}</{self.tag_name}>"
