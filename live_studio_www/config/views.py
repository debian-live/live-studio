from django.shortcuts import get_object_or_404

from live_studio_www.utils import render_response

from .models import Config

def configs(request):
    return render_response(request, 'config/configs.html')

def view(request, config_id):
    c = get_object_or_404(Config, pk=config_id, user=request.user)

    return render_response(request, 'config/view.html', {
        'config': c,
    })
