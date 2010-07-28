from django.shortcuts import render_to_response

from live_studio_www.auth.decorators import login_not_required

@login_not_required
def welcome(request):
    return render_to_response('static/welcome.html', {})
