# TODO: Make this all a class instead (`from_dict`, `from_str`, ...)?


def style_to_dict(style: str) -> dict:
    if not style:
        return {}

    dict_ = {}
    styles = [s for s in style.split(";") if s != ""]

    for style in styles:
        k, v = style.split(":")

        dict_[k.strip()] = v.strip()

    return dict_


def dict_to_style(dict_: dict) -> str:
    style = ""
    safe = lambda s: s.replace("_", "-")

    for k, v in dict_.items():
        style += f"{safe(k)}:{safe(v)};"

    return style
