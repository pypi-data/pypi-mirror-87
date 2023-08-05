# NOTE: This is a generated file. Found a bug? Fix it in
# `scripts/generate_html_component`.
from ...component import Component


class Input(Component):
    def __init__(
        self,
        *slots,
        accept=None,
        alt=None,
        autocomplete=None,
        autofocus=None,
        capture=None,
        checked=None,
        dirname=None,
        disabled=None,
        form=None,
        formaction=None,
        formenctype=None,
        formmethod=None,
        formnovalidate=None,
        formtarget=None,
        height=None,
        id=None,
        inputmode=None,
        list=None,
        max=None,
        maxlength=None,
        min=None,
        minlength=None,
        multiple=None,
        name=None,
        pattern=None,
        placeholder=None,
        readonly=None,
        required=None,
        size=None,
        src=None,
        step=None,
        tabindex=None,
        title=None,
        type=None,
        value=None,
        width=None
    ):
        self.attr(
            {
                "accept": accept,
                "alt": alt,
                "autocomplete": autocomplete,
                "autofocus": autofocus,
                "capture": capture,
                "checked": checked,
                "dirname": dirname,
                "disabled": disabled,
                "form": form,
                "formaction": formaction,
                "formenctype": formenctype,
                "formmethod": formmethod,
                "formnovalidate": formnovalidate,
                "formtarget": formtarget,
                "height": height,
                "id": id,
                "inputmode": inputmode,
                "list": list,
                "max": max,
                "maxlength": maxlength,
                "min": min,
                "minlength": minlength,
                "multiple": multiple,
                "name": name,
                "pattern": pattern,
                "placeholder": placeholder,
                "readonly": readonly,
                "required": required,
                "size": size,
                "src": src,
                "step": step,
                "tabindex": tabindex,
                "title": title,
                "type": type,
                "value": value,
                "width": width,
            }
        )

        super().__init__(*slots)

    def render(self):
        return Component(tag_name="input").proxy(self).render()
