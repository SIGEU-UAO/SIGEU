from django.http import JsonResponse
from django.middleware.csrf import get_token

def get_csrf_token(request):
    response = JsonResponse({'csrfToken': get_token(request)})
    response.set_cookie('csrftoken', get_token(request))
    return response
