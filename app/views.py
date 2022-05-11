from django.http import HttpResponse

def ping(request):
    return HttpResponse('PONG', status=200)

def not_found():
    return HttpResponseNotFound()