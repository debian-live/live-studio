from django import forms

from .models import Config

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Config
        exclude = ('created', 'user')

PAGES = (
    ('base',),
    ('distribution',),
    ('media_type',),
    ('architecture',),
    ('installer',),
    ('locale', 'keyboard_layout'),
)

WIZARD_FORMS = []
for fields in PAGES:
    meta = type('Meta', (), {
        'model': Config,
        'fields': fields,
    })

    WIZARD_FORMS.append(type('', (forms.ModelForm,), {'Meta': meta}))
