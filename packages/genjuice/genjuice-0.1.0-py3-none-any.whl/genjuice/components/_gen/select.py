# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Select(Component):
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
        self.attr(
            {
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

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="select").proxy(self).render()
