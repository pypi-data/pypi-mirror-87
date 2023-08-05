# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Meta(Component):
    def __init__(self, *slots, charset=None, content=None, http_equiv=None, name=None):
        self.attr(
            {
                "charset": charset,
                "content": content,
                "http-equiv": http_equiv,
                "name": name,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="meta").proxy(self).render()
