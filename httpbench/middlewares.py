from django.contrib import auth

from .header import get_username_wsgi_env_key


class HeaderAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        username = request.META.get(get_username_wsgi_env_key())
        user = auth.authenticate(request, username=username)
        if user:
            request.user = user
            auth.login(request, user)
        return self.get_response(request)
