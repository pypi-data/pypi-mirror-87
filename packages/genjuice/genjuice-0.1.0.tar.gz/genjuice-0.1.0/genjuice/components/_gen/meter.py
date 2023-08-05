# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Meter(Component):
    def __init__(
        self,
        *slots,
        value=None,
        min=None,
        max=None,
        low=None,
        high=None,
        optimum=None,
        form=None
    ):
        self.attr(
            {
                "value": value,
                "min": min,
                "max": max,
                "low": low,
                "high": high,
                "optimum": optimum,
                "form": form,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="meter").proxy(self).render()
