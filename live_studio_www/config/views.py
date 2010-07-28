from django.shortcuts import render_to_response

def configs(request):
    return render_to_response('config/configs.html', {
        'configs': request.user.configs.all(),
    })
