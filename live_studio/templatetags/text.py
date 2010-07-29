from .library import register

@register.filter
def command_line_options(options):
    out = ""

    for option in options:
        if ' ' in option:
            out += ' "%s"' % option
        else:
            out += ' %s' % option

    return out.strip()
