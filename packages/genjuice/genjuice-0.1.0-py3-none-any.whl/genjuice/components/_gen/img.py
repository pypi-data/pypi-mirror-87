# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Img(Component):
    def __init__(
        self,
        *slots,
        alt=None,
        crossorigin=None,
        anonymous=None,
        use_credentials=None,
        decoding=None,
        sync=None,
        async_=None,
        auto=None,
        height=None,
        ismap=None,
        loading=None,
        sizes=None,
        src=None,
        srcset=None,
        width=None,
        usemap=None
    ):
        self.attr(
            {
                "alt": alt,
                "crossorigin": crossorigin,
                "anonymous": anonymous,
                "use-credentials": use_credentials,
                "decoding": decoding,
                "sync": sync,
                "async": async_,
                "auto": auto,
                "height": height,
                "ismap": ismap,
                "loading": loading,
                "sizes": sizes,
                "src": src,
                "srcset": srcset,
                "width": width,
                "usemap": usemap,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="img").proxy(self).render()
