from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from live_studio_www.utils import render_response

from .forms import ConfigForm
from .models import Config

def configs(request):
    return render_response(request, 'config/configs.html')

def view(request, config_id):
    c = get_object_or_404(Config, pk=config_id, user=request.user)

    return render_response(request, 'config/view.html', {
        'config': c,
    })

def edit(request, config_id):
    config = get_object_or_404(Config, pk=config_id, user=request.user)

    if request.method == 'POST':
        form = ConfigForm(request.POST, instance=config)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(config.get_absolute_url())
    else:
        form = ConfigForm(instance=config)

    return render_response(request, 'config/edit.html', {
        'form': form,
        'config': config,
    })
