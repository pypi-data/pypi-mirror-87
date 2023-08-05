# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Body(Component):
    def __init__(
        self,
        *slots,
        onafterprint=None,
        onbeforeprint=None,
        onbeforeunload=None,
        onblur=None,
        onerror=None,
        onfocus=None,
        onhashchange=None,
        onload=None,
        onmessage=None,
        onoffline=None,
        ononline=None,
        onpopstate=None,
        onredo=None,
        onresize=None,
        onstorage=None,
        onundo=None,
        onunload=None
    ):
        self.attr(
            {
                "onafterprint": onafterprint,
                "onbeforeprint": onbeforeprint,
                "onbeforeunload": onbeforeunload,
                "onblur": onblur,
                "onerror": onerror,
                "onfocus": onfocus,
                "onhashchange": onhashchange,
                "onload": onload,
                "onmessage": onmessage,
                "onoffline": onoffline,
                "ononline": ononline,
                "onpopstate": onpopstate,
                "onredo": onredo,
                "onresize": onresize,
                "onstorage": onstorage,
                "onundo": onundo,
                "onunload": onunload,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="body").proxy(self).render()
