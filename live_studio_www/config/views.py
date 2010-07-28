from live_studio_www.utils import render_response

def configs(request):
    return render_response(request, 'config/configs.html')
