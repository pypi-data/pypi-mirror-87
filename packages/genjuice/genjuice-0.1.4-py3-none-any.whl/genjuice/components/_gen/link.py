# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Link(Component):
    """
    The HTML External Resource Link element (<link>) specifies relationships between the current document and an external resource. This element is most commonly used to link to stylesheets, but is also used to establish site icons (both "favicon" style icons and icons for the home screen and apps on mobile devices) among other things.
    """

    def __init__(
        self,
        *slots,
        as_=None,
        crossorigin=None,
        anonymous=None,
        use_credentials=None,
        disabled=None,
        href=None,
        hreflang=None,
        imagesizes=None,
        imagesrcset=None,
        media=None,
        rel=None,
        sizes=None,
        title=None,
        type=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "as": as_,
                "crossorigin": crossorigin,
                "anonymous": anonymous,
                "use-credentials": use_credentials,
                "disabled": disabled,
                "href": href,
                "hreflang": hreflang,
                "imagesizes": imagesizes,
                "imagesrcset": imagesrcset,
                "media": media,
                "rel": rel,
                "sizes": sizes,
                "title": title,
                "type": type,
            }
        )

    def render(self):
        return Component(tag_name="link").proxy(self).render()
