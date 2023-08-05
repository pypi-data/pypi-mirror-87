# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Select(Component):
    """
    The HTML <select> element represents a control that provides a menu of options:
    """

    def __init__(
        self,
        *slots,
        autocomplete=None,
        autofocus=None,
        disabled=None,
        form=None,
        multiple=None,
        name=None,
        required=None,
        size=None
    ):
        super().__init__(*slots)

        self.attr(
            **{
                "autocomplete": autocomplete,
                "autofocus": autofocus,
                "disabled": disabled,
                "form": form,
                "multiple": multiple,
                "name": name,
                "required": required,
                "size": size,
            }
        )

    def render(self):
        return Component(tag_name="select").proxy(self).render()
