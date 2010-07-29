from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Entry

@require_POST
def enqueue(request, config_id):
    config = get_object_or_404(request.user.configs, pk=config_id)

    Entry.objects.create(config=config)

    return HttpResponseRedirect(config.get_absolute_url())
