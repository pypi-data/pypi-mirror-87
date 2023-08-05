# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Track(Component):
    """
    The HTML <track> element is used as a child of the media elements, <audio> and <video>. It lets you specify timed text tracks (or time-based data), for example to automatically handle subtitles. The tracks are formatted in WebVTT format (.vtt files) — Web Video Text Tracks.
    """

    def __init__(
        self, *slots, default=None, kind=None, label=None, src=None, srclang=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "default": default,
                "kind": kind,
                "label": label,
                "src": src,
                "srclang": srclang,
            }
        )

    def render(self):
        return Component(tag_name="track").proxy(self).render()
