from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.formtools.wizard import FormWizard

from live_studio_www.utils import render_response

from .forms import ConfigForm, WIZARD_FORMS
from .models import Config

def configs(request):
    return render_response(request, 'config/configs.html')

def view(request, config_id):
    config = get_object_or_404(request.user.configs, pk=config_id)

    return render_response(request, 'config/view.html', {
        'config': config,
    })

def edit(request, config_id):
    config = get_object_or_404(request.user.configs, pk=config_id)

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

class NewConfigWizard(FormWizard):
    def done(self, request, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        config = Config(user=request.user, **data)
        config.save()

        return HttpResponseRedirect(config.get_absolute_url())

    def get_template(self, step):
        return 'config/add_%s.html' % step

add = NewConfigWizard(WIZARD_FORMS)
