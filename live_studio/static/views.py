from django.conf import settings
from django.http import HttpResponseRedirect

from live_studio.utils import render_response
from live_studio.auth.decorators import login_not_required

@login_not_required
def welcome(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render_response(request, 'static/welcome.html', {})

@login_not_required
def faq(request):
    return render_response(request, 'static/faq.html', {})
