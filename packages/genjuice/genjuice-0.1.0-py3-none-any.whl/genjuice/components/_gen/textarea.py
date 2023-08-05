# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Textarea(Component):
    def __init__(
        self,
        *slots,
        autocomplete=None,
        autofocus=None,
        cols=None,
        disabled=None,
        form=None,
        maxlength=None,
        minlength=None,
        name=None,
        placeholder=None,
        readonly=None,
        required=None,
        rows=None,
        spellcheck=None,
        wrap=None
    ):
        self.attr(
            {
                "autocomplete": autocomplete,
                "autofocus": autofocus,
                "cols": cols,
                "disabled": disabled,
                "form": form,
                "maxlength": maxlength,
                "minlength": minlength,
                "name": name,
                "placeholder": placeholder,
                "readonly": readonly,
                "required": required,
                "rows": rows,
                "spellcheck": spellcheck,
                "wrap": wrap,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="textarea").proxy(self).render()
