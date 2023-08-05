# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Script(Component):
    """
    The HTML <script> element is used to embed executable code or data; this is typically used to embed or refer to JavaScript code. The <script> element can also be used with other languages, such as WebGL's GLSL shader programming language and JSON.
    """

    def __init__(
        self,
        *slots,
        async_=None,
        crossorigin=None,
        defer=None,
        integrity=None,
        nomodule=None,
        nonce=None,
        referrerpolicy=None,
        src=None,
        type=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "async": async_,
                "crossorigin": crossorigin,
                "defer": defer,
                "integrity": integrity,
                "nomodule": nomodule,
                "nonce": nonce,
                "referrerpolicy": referrerpolicy,
                "src": src,
                "type": type,
            }
        )

    def render(self):
        return Component(tag_name="script").proxy(self).render()
