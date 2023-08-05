# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Audio(Component):
    """
    The HTML <audio> element is used to embed sound content in documents. It may contain one or more audio sources, represented using the src attribute or the <source> element: the browser will choose the most suitable one. It can also be the destination for streamed media, using a MediaStream.
    """

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
        super().__init__(*slots)

        self.attr(
            **{
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

    def render(self):
        return Component(tag_name="audio").proxy(self).render()
