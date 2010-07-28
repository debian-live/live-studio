from django.conf import settings
from django.http import HttpResponseRedirect

class RequireLoginMiddleware(object):
    ALLOW = (
        '/admin/',
        '/media/',
        '/__debug__/',
    )

    def process_view(self, request, fn, *args, **kwargs):
        if request.user.is_authenticated():
            return

        if hasattr(fn, 'login_not_required'):
            return

        for prefix in self.ALLOW:
            if request.path.startswith(prefix):
                return

        return HttpResponseRedirect(settings.LOGIN_URL)
