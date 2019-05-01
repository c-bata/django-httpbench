from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin

from .header import get_username_wsgi_env_key


class HeaderAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        username = request.META.get(get_username_wsgi_env_key())
        user = auth.authenticate(request, username=username)
        if user:
            request.user = user
            auth.login(request, user)
