from django.contrib import admin

from .models import Config

class ConfigAdmin(admin.ModelAdmin):
    exclude = ('created',)

admin.site.register(Config, ConfigAdmin)
