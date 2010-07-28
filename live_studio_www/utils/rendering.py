from django.template import RequestContext
from django.shortcuts import render_to_response

def render_response(request, template, context=None, mimetype='text/html'):
    return render_to_response(
        template,
        context or {},
        context_instance=RequestContext(request),
        mimetype=mimetype,
    )
