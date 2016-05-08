from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
import json


@csrf_exempt
def new_url(request):
    if request.method == 'POST':
        if not request.POST.get('url'):
            return error('404', 'No URL supplied to shorten')
        original_url = request.POST['url']
        url = models.Url.create_url(original_url)
        data = json.dumps({'original_url': url.original_url,
                           'short_url': url.short_url})
        return HttpResponse(data, content_type='application/json')


@csrf_exempt
def visit(request, visit_url):
    url = get_object_or_404(models.Url, short_url=visit_url)
    if request.META.get('HTTP_REFERER'):
        referrer = request.META.get('HTTP_REFERER')
    else:
        referrer = 'none'
    url.analytics.add_visit(referrer)
    to_direct = url.original_url
    if not to_direct.startswith('http://'):
        to_direct = 'http://' + to_direct

    return redirect(to_direct)


def error(code, message):
    data = json.dumps({'status': code,
                       'message': message})
    return HttpResponse(data, content_type='application/json')
