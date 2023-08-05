# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Source(Component):
    """
    The HTML <source> element specifies multiple media resources for the <picture>, the <audio> element, or the <video> element. It is an empty element, meaning that it has no content and does not have a closing tag. It is commonly used to offer the same media content in multiple file formats in order to provide compatibility with a broad range of browsers given their differing support for image file formats and media file formats.
    """

    def __init__(
        self, *slots, media=None, sizes=None, src=None, srcset=None, type=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "media": media,
                "sizes": sizes,
                "src": src,
                "srcset": srcset,
                "type": type,
            }
        )

    def render(self):
        return Component(tag_name="source").proxy(self).render()
