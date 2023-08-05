# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Object(Component):
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
        self.attr(
            {
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

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="object").proxy(self).render()
