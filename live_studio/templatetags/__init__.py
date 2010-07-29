from django.template import add_to_builtins

from .library import register

import media

add_to_builtins('live_studio.templatetags')
