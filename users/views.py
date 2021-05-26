from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.decorators import api_view
from .serializer import UserSerializer
import os
import jwt
import datetime

# Create your views here.


JWT_SECRET = os.environ.get('JWT_SECRET')


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        user = serializer.data

        payload = {
            'id': user['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'success': True,
            'token': token
        }

        return response


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'success': True,
            'token': token
        }

        return response


@api_view(['GET'])
def UserView(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise NotAuthenticated('Unauthenticated')

    try:
        payload = jwt.decode(token, JWT_SECRET, ['HS256'])
    except jwt.ExpiredSignatureError:
        raise NotAuthenticated('Unauthenticated')

    user = User.objects.get(id=payload['id'])

    serializer = UserSerializer(user)

    return Response(serializer.data)


@api_view(['GET'])
def LogoutView(request):
    response = Response()

    response.delete_cookie('jwt')

    response.data = {
        'success': True
    }

    return response
