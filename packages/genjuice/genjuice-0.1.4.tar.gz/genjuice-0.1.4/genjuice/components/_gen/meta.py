# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Meta(Component):
    """
    The HTML <meta> element represents metadata that cannot be represented by other HTML meta-related elements, like <base>, <link>, <script>, <style> or <title>.
    """

    def __init__(self, *slots, charset=None, content=None, http_equiv=None, name=None):
        super().__init__(*slots)

        self.attr(
            **{
                "charset": charset,
                "content": content,
                "http-equiv": http_equiv,
                "name": name,
            }
        )

    def render(self):
        return Component(tag_name="meta").proxy(self).render()
