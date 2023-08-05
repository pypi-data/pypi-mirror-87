# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Script(Component):
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
        self.attr(
            {
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

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="script").proxy(self).render()
