# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Audio(Component):
    def __init__(
        self,
        *slots,
        autoplay=None,
        controls=None,
        crossorigin=None,
        anonymous=None,
        use_credentials=None,
        currentTime=None,
        loop=None,
        muted=None,
        preload=None,
        src=None
    ):
        self.attr(
            {
                "autoplay": autoplay,
                "controls": controls,
                "crossorigin": crossorigin,
                "anonymous": anonymous,
                "use-credentials": use_credentials,
                "currentTime": currentTime,
                "loop": loop,
                "muted": muted,
                "preload": preload,
                "src": src,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="audio").proxy(self).render()
