from django.contrib import admin

from .models import Build

class BuildAdmin(admin.ModelAdmin):
    pass

admin.site.register(Build, BuildAdmin)
