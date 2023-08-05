# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Video(Component):
    """
    The HTML Video element (<video>) embeds a media player which supports video playback into the document. You can use <video> for audio content as well, but the <audio> element may provide a more appropriate user experience.
    """

    def __init__(
        self,
        *slots,
        autoplay=None,
        buffered=None,
        controls=None,
        crossorigin=None,
        anonymous=None,
        use_credentials=None,
        currentTime=None,
        height=None,
        loop=None,
        muted=None,
        playsinline=None,
        poster=None,
        preload=None,
        src=None,
        width=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "autoplay": autoplay,
                "buffered": buffered,
                "controls": controls,
                "crossorigin": crossorigin,
                "anonymous": anonymous,
                "use-credentials": use_credentials,
                "currentTime": currentTime,
                "height": height,
                "loop": loop,
                "muted": muted,
                "playsinline": playsinline,
                "poster": poster,
                "preload": preload,
                "src": src,
                "width": width,
            }
        )

    def render(self):
        return Component(tag_name="video").proxy(self).render()
