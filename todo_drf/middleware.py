from rest_framework.exceptions import NotAuthenticated
from django.contrib.auth.models import User
import jwt
import os

JWT_SECRET = os.environ.get('JWT_SECRET')

# Don't make this a global middleware in settings.py as it works on specific routes only


class JWTDecodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response

    # process_view is called before the view is called

    def process_view(self, request, view_func, view_args, view_kwargs):

        token = request.COOKIES.get('jwt')

        if not token:
            raise NotAuthenticated('Unauthenticated')

        try:
            payload = jwt.decode(token, JWT_SECRET, ['HS256'])
        except jwt.ExpiredSignatureError:
            raise NotAuthenticated('Unauthenticated')

        user = User.objects.get(pk=payload['id'])

        request.user = user  # setting user object

        # If None is returned the request flow proceeds to the view
        return None
