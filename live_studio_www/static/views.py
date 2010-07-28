from live_studio_www.utils import render_response
from live_studio_www.auth.decorators import login_not_required

@login_not_required
def welcome(request):
    return render_response(request, 'static/welcome.html', {})
