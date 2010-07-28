from .library import register

@register.simple_tag
def static(suffix):
    # This will eventually based on a settings variable
    return "/media/%s" % suffix
