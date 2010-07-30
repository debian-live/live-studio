from django.conf import settings
from django.http import HttpResponseRedirect

class RequireLoginMiddleware(object):
    ALLOW = (
        '/admin/',
        '/media/',
        '/accounts/',
        '/__debug__/',
        '/favicon.ico',
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

class SetRemoteAddrFromForwardedFor(object):
    """
    Middleware that sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, if the
    latter is set. This is useful if you're sitting behind a reverse proxy that
    causes each request's REMOTE_ADDR to be set to 127.0.0.1.

    Note that this does NOT validate HTTP_X_FORWARDED_FOR. If you're not behind
    a reverse proxy that sets HTTP_X_FORWARDED_FOR automatically, do not use
    this middleware. Anybody can spoof the value of HTTP_X_FORWARDED_FOR, and
    because this sets REMOTE_ADDR based on HTTP_X_FORWARDED_FOR, that means
    anybody can "fake" their IP address. Only use this when you can absolutely
    trust the value of HTTP_X_FORWARDED_FOR.
    """
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            return None
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs. The
            # client's IP will be the first one.
            real_ip = real_ip.split(",")[0].strip()
            request.META['REMOTE_ADDR'] = real_ip
