# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Object(Component):
    """
    The HTML <object> element represents an external resource, which can be treated as an image, a nested browsing context, or a resource to be handled by a plugin.
    """

    def __init__(
        self,
        *slots,
        data=None,
        form=None,
        height=None,
        name=None,
        type=None,
        typemustmatch=None,
        usemap=None,
        width=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "data": data,
                "form": form,
                "height": height,
                "name": name,
                "type": type,
                "typemustmatch": typemustmatch,
                "usemap": usemap,
                "width": width,
            }
        )

    def render(self):
        return Component(tag_name="object").proxy(self).render()
